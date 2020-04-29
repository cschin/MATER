# import sys
# import os
import numpy as np
import mmap
from collections import namedtuple
from ._shimmer4py import ffi as shimmer_ffi
from ._shimmer4py import lib as shimmer4py
from collections import Counter
# from ._ksw4py import ffi as ksw4py_ffi

rmap = dict(list(zip(b"ACGT", b"TGCA")))


def rc(seq):
    return bytes([rmap[c] for c in seq[::-1]])


MMER = namedtuple("MMER", "mmer span rid, pos_end, direction")


def mmer2tuple(mmer):
    x = mmer.x
    y = mmer.y
    span = x & 0xFF
    mmer = x >> 8
    rid = y >> 32
    pos_end = ((y & 0xFFFFFFFF) >> 1) + 1
    direction = y & 0x1
    return MMER(mmer, span, rid, pos_end, direction)


class Shimmer(object):
    def __init__(self):
        self.mmers = shimmer_ffi.new("mm128_v *")

    def __len__(self):
        return self.mmers.n

    def __getitem__(self, i):
        assert i < self.mmers.n
        return mmer2tuple(self.mmers.a[i])

    def __del__(self):
        shimmer4py.free(self.mmers.a)
        shimmer_ffi.release(self.mmers)


def get_shimmers_from_seq(seq, rid=0,
                          levels=2, reduction_factor=3,
                          k=16, w=80):
    assert levels <= 2
    c_null = shimmer_ffi.NULL
    mmers_L0 = Shimmer()
    shimmer4py.mm_sketch(c_null, seq, len(seq), w, k, rid, 0, mmers_L0.mmers)
    if levels == 0:
        return mmers_L0
    elif levels == 1:
        mmers_L1 = Shimmer()
        shimmer4py.mm_reduce(mmers_L0.mmers, mmers_L1.mmers, reduction_factor)
        del mmers_L0
        return mmers_L1
    elif levels == 2:
        mmers_L1 = Shimmer()
        mmers_L2 = Shimmer()
        shimmer4py.mm_reduce(mmers_L0.mmers, mmers_L1.mmers, reduction_factor)
        shimmer4py.mm_reduce(mmers_L1.mmers, mmers_L2.mmers, reduction_factor)
        del mmers_L1
        del mmers_L0
        return mmers_L2



SeqIndexData = namedtuple("SeqIndexData", "rname length offset")


class SequenceDatabase(object):
    def __init__(self, index_path="", seqdb_path=""):
        self.basemap = {0: b"N", 1: b"A", 2: b"C", 4: b"G", 8: b"T"}
        self.index_path = index_path
        self.seqdb_path = seqdb_path
        self.name2rid = {}
        self.index_data = {}
        self._load_index()
        self._f = open(seqdb_path, "rb")
        self.seqdb = mmap.mmap(self._f.fileno(), 0,
                               flags=mmap.MAP_SHARED,
                               prot=mmap.PROT_READ)

    def _load_index(self):
        with open(self.index_path) as f:
            for row in f:
                row = row.strip().split()
                rid, rname, rlen, offset = row
                rid = int(rid)
                rlen = int(rlen)
                offset = int(offset)
                self.index_data.setdefault(rid, {})
                self.name2rid[rname] = rid
                self.index_data[rid] = SeqIndexData(rname=rname,
                                                    length=rlen,
                                                    offset=offset)

    def get_subseq_by_rid(self, rid, start=-1, end=-1, direction=0):
        if start == -1 and end == -1:
            start = 0
            end = self.index_data[rid].length
        offset = self.index_data[rid].offset
        s = offset + start
        e = offset + end
        if direction == 1:
            seq = b"".join([self.basemap[(c & 0xF0) >> 4]
                            for c in self.seqdb[s:e]])
        else:
            seq = b"".join([self.basemap[c & 0x0F] for c in self.seqdb[s:e]])
        return seq

    def get_subseq_by_name(self, rname, start=-1, end=-1, direction=0):
        rid = self.name2rid[rname]
        return self.get_subseq_by_rid(rid, start, end, direction=direction)

    def get_seq_index_by_name(self, rname):
        return self.index_data[self.name2rid[rname]]

    def __del__(self):
        self.seqdb.close()
        self._f.close()



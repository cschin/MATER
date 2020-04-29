import mater.utils
from mater.utils import SequenceDatabase
from mater.utils import get_shimmers_from_seq
import pickle

kmer_size = 24
w_size = 12

HLAIDMap = {}
with open("hla_nuc_seq_id_map") as f:
    for row in f:
        row = row.strip().split()
        if len(row[1].split("*")[0]) != 1:
            continue
        HLAIDMap[row[0]] = row[1]


hla_sdb = SequenceDatabase("nuc.idx", "nuc.seqdb")

seqs = []

for i in hla_sdb.index_data:
    seq_name = hla_sdb.index_data[i].rname
    if seq_name not in HLAIDMap:
        continue
    seq = hla_sdb.get_subseq_by_rid(i)
    mmers = get_shimmers_from_seq(seq, levels=1, reduction_factor=1, 
                                       w=w_size, k=kmer_size)
    mmers = [mmers[_].mmer for _ in range(len(mmers))]
    
    seqs.append( (HLAIDMap[seq_name],
                  seq_name,
                  seq,
                  mmers) )


mer2HLAtype = {}
for t, sn, s, m in seqs:
    for mm in m:
        mer2HLAtype.setdefault(mm, set())
        mer2HLAtype[mm].add(":".join(t.split(":")[:2]))


f=open("mmer2HLAtype.pickle", "wb")
pickle.dump(mer2HLAtype, f)
f.close()


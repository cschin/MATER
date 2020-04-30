import os
import sys
import pickle
from docopt import docopt
from collections import Counter
import mater.utils
from mater.utils import SequenceDatabase
from mater.utils import get_shimmers_from_seq

__version__ = mater.__version__

__doc__ = """
MATER - Minimizer RNAseq HLA TyER

==================================================================
MATER is a minimier base HLA typer for RNAseq read dataset. In a 
typical RNAseq dataset, the reads sampled from HLA genes are less 
uniform and may miss regions that makes assembly or variant calling 
base methods for HLA typing more challenge. Here we adopt a slight 
different approach. We try to assign each reads to possible HLA types 
by using minimizers. Namely, we will generate dense minimer for 
each reads and compare to those from the HLA type seqeunces. We 
annotate each each reads to possible HLA serotype or 4 digit 
type sequence according the minimizer matches. Some reads may be 
able to assign to single HLA type-sequence, some other may be more 
ambiguous. We derive a simple score to summarize the results from all 
reads that are mapped to HLA-type sequences for each HLA allele.

While this method may not generate more rigious HLA-typing results, 
it is fast and can be use for upstream process for generate HLA-typing
with assembly or variant call approach for RNAseq dataset.


Usage:
  run_mater.py <reads.fasta> <output_directory>
  run_mater.py (-h | --help)
  run_mater.py --verison

Options:
  -h --help                   Show this help
  --version                   Show version

"""

if __name__ == "__main__":

    args = docopt(__doc__, version=__version__)
    reads_fn = args["<reads.fasta>"]
    output_dir = args["<output_directory>"]
    os.makedirs(f"{output_dir}",  exist_ok=True)
    os.system("echo {} > {}/reads.lst".format(reads_fn, output_dir))
    os.system(f"shmr_mkseqdb -d {output_dir}/reads.lst -p {output_dir}/reads >> /dev/null")

    read_sdb = SequenceDatabase(f"{output_dir}/reads.idx", 
                                f"{output_dir}/reads.seqdb")

    kmer_size = 24
    w_size = 12

    mer2HLAtype = pickle.load(open("/opt/data/mmer2HLAtype.pickle", "rb"))
    read_sdb = SequenceDatabase(f"{output_dir}/reads.idx", f"{output_dir}/reads.seqdb")


    allele_weight = {}
    allele_count = {}
    allele_weight2 = {}
    allele_count2 = {}
    allele2reads = {}

    seq_hashes = set()
    for i in read_sdb.index_data:

        HLAtype_set=[]
        if read_sdb.index_data[i].length < 80:
            continue
        seq = read_sdb.get_subseq_by_rid(i)
        if hash(seq) in seq_hashes:
            continue
        seq_hashes.add(hash(seq))
        seq_name = read_sdb.index_data[i].rname

        mmers = get_shimmers_from_seq(seq, levels=1, 
                                      reduction_factor=1, 
                                      w=w_size, 
                                      k=kmer_size)

        mmers = [mmers[_].mmer for _ in range(len(mmers))]
        
        sets = []

        for mm in mmers:
            if mm not in mer2HLAtype:
                continue
            sets.append(set(mer2HLAtype[mm]))
       
        if len(sets) > 0:
            s = sets[0]
            for ss in sets[1:]:
                s &= ss
            HLAtype_set.extend(list(s))
     
        if len(HLAtype_set) > 0:
            c0 = Counter([_.split("*")[0] for _ in HLAtype_set])
            if len(c0) > 1:
                continue

            allele = c0.most_common(1)[0][0]
            allele2reads.setdefault(allele, set())
            allele2reads[allele].add(i)

            c1 = set([":".join(_.split(":")[:1]) 
                for _ in HLAtype_set if _.split("*")[0] == allele])
            c1 = sorted(list(c1)) 
            n = len(c1)
            for serotype in c1:
                allele_weight.setdefault(allele, {})
                allele_weight[allele].setdefault(serotype, 0)
                allele_weight[allele][serotype] += 1.0/n
                
                allele_count.setdefault(allele, {})
                allele_count[allele].setdefault(serotype, 0)
                allele_count[allele][serotype] += 1

                c2 = set([":".join(_.split(":")[:2]) 
                    for _ in HLAtype_set if _.split(":")[0] == serotype])
                c2 = sorted(list(c2))
                n2 = len(c2)
                for t in c2:  #make the result determinsitic
                    allele_weight2.setdefault(serotype, {})
                    allele_weight2[serotype].setdefault(t, 0)
                    allele_weight2[serotype][t] += 1.0/n2

                    allele_count2.setdefault(serotype, {})
                    allele_count2[serotype].setdefault(t, 0)
                    allele_count2[serotype][t] += 1
                # print(i, c1, serotype, c2, read_sdb.index_data[i].rname, 
                #       read_sdb.get_subseq_by_rid(i).decode())

    out_f = open(f"{output_dir}/allele_weight.txt", "w")

    for allele in sorted(allele_weight.keys()):
        c = list(allele_weight[allele].items())
        c.sort(key=lambda _:-_[1])
        print("#", allele, len(allele2reads[allele]), file=out_f)
        for t, w in c[:10]:
            #print(allele2reads[t])
            c = list(allele_weight2[t].items())
            c.sort(key=lambda _:-_[1])
            t2, w2 =  c[0]
            print(allele, t, "%0.2f" % w, allele_count[allele][t], t2, file=out_f)
        print("#", file=out_f)

    for allele in ("A", "B", "C"):
        f = open("{}/reads_{}.fa".format(output_dir, allele),"w")
        for i in allele2reads.get(allele,[]):
            print(">{}".format(read_sdb.index_data[i].rname), file=f)
            print(read_sdb.get_subseq_by_rid(i).decode(), file=f)
        f.close()

    os.remove(f"{output_dir}/reads.idx")
    os.remove(f"{output_dir}/reads.seqdb")
    os.remove(f"{output_dir}/reads.lst")

[![Actions Status](https://github.com/cschin/MATER/workflows/test-docker-build/badge.svg)](https://github.com/cschin/MATER/actions)

## MATER - Minimizer RNAseq HLA TyER

MATER is a minimier base HLA typer for RNAseq read dataset. In a typical RNAseq dataset,
the reads sampled from HLA genes are less uniform and may miss regions that makes assembly
or variant calling base methods for HLA typing more challenge. Here we adopt a slight
different approach. We try to assign each reads to possible HLA types by using minimizers.
Namely, we will generate dense minimer for each reads and compare to those from the HLA
type seqeunces. We annotate each each reads to possible HLA serotype or 4 digit type sequence
according the minimizer matches. Some reads may be able to assign to single HLA type-sequence,
some other may be more ambiguous. We derive a simple score to summarize the results from
all reads that are mapped to HLA-type sequences for each HLA allele.

While this method may not generate more rigious HLA-typing results, it is fast and can be
use for upstream process for generate HLA-typing with assembly or variant call approach
for RNAseq dataset.


### Install

TODO

--Jason Chin
Apr. 28, 2020    

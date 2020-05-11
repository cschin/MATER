[![Actions Status](https://github.com/cschin/MATER/workflows/build-and-push-docker-image/badge.svg)](https://github.com/cschin/MATER/actions)

## MATER - Minimizer RNAseq HLA TypER

MATER is a minimizer based HLA typer for RNAseq read dataset. In a typical RNAseq dataset,
the reads sampled from HLA genes are less uniform and may miss regions that makes assembly
or variant calling base methods for HLA typing more challenge. Here we adopt a slightly
different approach. We try to assign each reads to possible HLA types by using minimizers.
Namely, we will generate a dense minimer for each read and compare to those from the HLA
type sequences. We annotate each each read with possible HLA serotypes or 4 digit type sequences
according the minimizer matches. We may be able to assign some reads to a single HLA type-sequence,
while some other may be more ambiguous. We derive a simple score to summarize the results from
all reads that are mapped to HLA-type sequences for each HLA allele.

While this method may not generate the most rigorous HLA-typing results, it is fast and can be
used as an upstream process for generating HLA-typing with assembly or variant call approaches
for RNAseq datasets.


### Install

see `install_with_conda.sh`. You will need to have permission to access `/opt/` in your 
system or you can modify the source code to point to a location for the data file.


### Test run with built docker image

see an example below

```
$ git clone https://github.com/cschin/MATER
Cloning into 'MATER'...
remote: Enumerating objects: 146, done.
remote: Counting objects: 100% (146/146), done.
remote: Compressing objects: 100% (94/94), done.
remote: Total 146 (delta 46), reused 115 (delta 25), pack-reused 0
Receiving objects: 100% (146/146), 10.41 MiB | 9.69 MiB/s, done.
Resolving deltas: 100% (46/46), done.

$ cd MATER/test/

$ cat run.sh
#!/bin/bash
docker run -v $PWD:$PWD cschin/mater $PWD/test.fa $PWD/out

$ bash run.sh
MATER(0+untagged.18.gb4f1468)

$ cat out/allele_weight.txt | head -38
# A 141
A A*24 36.23 86 A*24:02
A A*01 19.50 66 A*01:12
A A*23 16.79 53 A*23:10
A A*11 14.88 62 A*11:271
A A*02 11.04 48 A*02:804
A A*25 8.69 43 A*25:59
A A*03 7.62 40 A*03:18
A A*36 7.18 30 A*36:04
A A*33 6.51 31 A*33:19
A A*30 3.42 17 A*30:02
#
# B 145
B B*15 34.87 85 B*15:01
B B*57 15.97 57 B*57:01
B B*48 11.49 64 B*48:13
B B*81 8.90 47 B*81:02
B B*07 7.88 47 B*07:209
B B*35 7.79 51 B*35:208
B B*40 7.03 55 B*40:26
B B*58 5.55 32 B*58:36
B B*27 5.33 45 B*27:125
B B*13 4.74 30 B*13:04
#
# C 108
C C*04 16.73 55 C*04:360
C C*06 16.06 68 C*06:274
C C*08 15.90 59 C*08:10
C C*07 14.07 45 C*07:41
C C*05 9.17 53 C*05:79
C C*03 6.40 44 C*03:251
C C*12 5.79 44 C*12:02
C C*15 5.56 42 C*15:05
C C*02 5.51 31 C*02:02
C C*01 4.29 37 C*01:04
#
# E 107
E E*01 107.00 107 E*01:12
```

--Jason Chin
Apr. 28, 2020    

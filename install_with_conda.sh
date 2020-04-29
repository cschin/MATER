#!/bin/bash
export CONDAROOT=/opt/conda/
. $CONDAROOT/bin/activate
conda create -n mater -y python=3.7

conda activate mater

pushd src
make all
make install
popd

pushd py
python setup.py install
popd

mkdir /opt/data/
cp data/mmer2HLAtype.pickle /opt/data/


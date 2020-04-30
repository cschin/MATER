#!/bin/bash
docker run -it -v $PWD:$PWD cschin/mater $PWD/test.fa $PWD/out

#!/bin/bash
docker run -v $PWD:$PWD cschin/mater $PWD/test.fa $PWD/out

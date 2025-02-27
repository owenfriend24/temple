#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: ashs_test.sh subject"

    exit 1
fi

corr=$1

cp -R $SCRATCH/ashs/bin $CORR/ashs/
cp $SCRATCH/ashs/*.txt $CORR/ashs/
cp -R $SCRATCH/ashs/ext $CORR/ashs/
cp -R $SCRATCH/ashs/src $CORR/ashs/
cp -R $SCRATCH/ashs/test_atlas $CORR/ashs/
cp $SCRATCH/ashs/*.md $CORR/ashs/
cp -R $SCRATCH/ashs/submodules $CORR/ashs/
cp $SCRATCH/ashs/LICENSE $CORR/ashs

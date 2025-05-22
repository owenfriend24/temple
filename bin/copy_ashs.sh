#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: ashs_test.sh subject"

    exit 1
fi

sub=$1

mkdir -p $CORR/ashs/masks/sub-${sub}

cp -R $SCRATCH/ashs/new_test/sub-${sub}/final $CORR/ashs/masks/sub-${sub}/
cp -R $SCRATCH/ashs/new_test/sub-${sub}/subfield_masks $CORR/ashs/masks/sub-${sub}/



#cp -R $SCRATCH/ashs/bin $CORR/ashs/
#cp $SCRATCH/ashs/*.txt $CORR/ashs/
#cp -R $SCRATCH/ashs/ext $CORR/ashs/
#cp -R $SCRATCH/ashs/src $CORR/ashs/
#cp -R $SCRATCH/ashs/test_atlas $CORR/ashs/
#cp $SCRATCH/ashs/*.md $CORR/ashs/
#cp -R $SCRATCH/ashs/submodules $CORR/ashs/
#cp $SCRATCH/ashs/LICENSE $CORR/ashs

#!/bin/env bash
#
# batch create post-learning correlation distance dataframes for multi-dimensional scaling analyses
if [[ $# -lt 1 ]]; then
    echo "Usage: batch_mds_sub.sh sub"
    exit 1
fi

sub=$1

source home/09123/ofriend/analysis/temple/profile


# this is for adults
sl_masks_to_func.sh ${sub} $FM AB adult_PHC_AB_mask
sl_masks_to_func.sh ${sub} $FM AB adult_hip_AB_mask
sl_masks_to_func.sh ${sub} $FM AB adult_IFG_AB_mask
sl_masks_to_func.sh ${sub} $FM AC adult_IFG_AC_mask
sl_masks_to_func.sh ${sub} $FM ABC adult_IFG_ABC_mask

mds_sub.py $FM ${sub} $FM/sub-${sub}/transforms/adult_IFG_AB_mask.nii.gz adult_PHC_AB
mds_sub.py $FM ${sub} $FM/sub-${sub}/transforms/adult_IFG_AB_mask.nii.gz adult_hip_AB
mds_sub.py $FM ${sub} $FM/sub-${sub}/transforms/adult_IFG_AB_mask.nii.gz adult_IFG_AB
mds_sub.py $FM ${sub} $FM/sub-${sub}/transforms/adult_IFG_AC_mask.nii.gz adult_IFG_AC
mds_sub.py $FM ${sub} $FM/sub-${sub}/transforms/adult_IFG_ABC_mask.nii.gz adult_IFG_ABC
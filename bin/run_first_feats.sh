#!/bin/bash
#
# use feat to run first level analyses and transform into mni space


if [[ $# -lt 4 ]]; then
    echo "Usage: run_first_levels.sh fmriprep_dir subject corral_dir type (boundary, ppi, ppi_inverse) roi (if ppi)"
    exit 1
fi

fmriprep_dir=$1
subject=$2
corral=$3
type=$4
roi=$5


if [ "$type" == "boundary" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/
    roi_tag=""
elif [ "$type" == "ppi" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/ppi/
    roi_tag="_${roi}"
elif [ "$type" == "ppi_inverse" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/ppi_inverse/
    roi_tag="_${roi}"
fi

fsf_file=${base}/sub-${subject}-univ-${type}${roi_tag}_first_run-0${run}.fsf

for run in 1 2 3 4; do
    echo "running first level analysis for sub ${subject}..."
    feat "$fsf_file"
    chmod 775 -R "${corral}/sub-${subject}/transforms"
    
    echo "saving first level output to native directory"
    mkdir "${base}/out_run${run}${roi_tag}.feat/native"
    cp -r "${base}/out_run${run}${roi_tag}.feat/stats/"* "${base}/out_run${run}${roi_tag}.feat/native"
    cp "${base}/out_run${run}${roi_tag}.feat/example_func.nii.gz" "${base}/out_run${run}${roi_tag}.feat/native/example_func.nii.gz"
    cp "${base}/out_run${run}${roi_tag}.feat/mean_func.nii.gz" "${base}/out_run${run}${roi_tag}.feat/native/mean_func.nii.gz"
    cp "${base}/out_run${run}${roi_tag}.feat/mask.nii.gz" "${base}/out_run${run}${roi_tag}.feat/native/mask.nii.gz"
    
    # cope images
    echo "transforming cope images"
    track=1
    for cope in ${base}/"out_run${run}${roi_tag}.feat"/native/cope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${base}/"out_run${run}${roi_tag}.feat"/stats/cope${track}.nii.gz \
    -n NearestNeighbor -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt"  # \
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"

    ((track=track+1))
    done
    
    # cope images
    echo "transforming varcope images"
    track=1
    for cope in ${base}/"out_run${run}${roi_tag}.feat"/native/varcope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${base}/"out_run${run}${roi_tag}.feat"/stats/varcope${track}.nii.gz \
    -n NearestNeighbor -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt"   # \
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    ((track=track+1))
    done
    
    
    # func data
    echo "transforming func data"
    
    fslreorient2std "${base}/out_run${run}${roi_tag}.feat/native/example_func.nii.gz" 
    antsApplyTransforms -d 3 -i "${base}/out_run${run}${roi_tag}.feat/native/example_func.nii.gz" \
    -o "${base}/out_run${run}${roi_tag}.feat/example_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    fslreorient2std "${base}/out_run${run}${roi_tag}.feat/native/mean_func.nii.gz"
    antsApplyTransforms -d 3 -i "${base}/out_run${run}${roi_tag}.feat/native/mean_func.nii.gz" \
    -o "${base}/out_run${run}${roi_tag}.feat/mean_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"


    # mask
    echo "transforming mask"
    fslreorient2std "${base}/out_run${run}${roi_tag}.feat/mask.nii.gz"
    antsApplyTransforms -d 3 -i "${base}/out_run${run}${roi_tag}.feat/native/mask.nii.gz"\
     -o "${base}/out_run${run}${roi_tag}.feat/mask.nii.gz" \
     -n NearestNeighbor \
     -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
     -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
     -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#     -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    echo "formatting reg folder"
    # set up reg folder
    mkdir "${base}/out_run${run}${roi_tag}.feat/reg"
    cp /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    "${base}/out_run${run}${roi_tag}.feat/reg/standard.nii.gz"

    cp "${corral}/sub-${subject}/anat/sub-${subject}_MNI_ss.nii.gz" \
    "${base}/out_run${run}${roi_tag}.feat/reg/highres.nii.gz"

    cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" \
    "${base}/out_run${run}${roi_tag}.feat/reg/example_func2standard.mat"

    updatefeatreg "${base}/out_run${run}${roi_tag}.feat" -pngs
done
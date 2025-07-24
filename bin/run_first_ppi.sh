#!/bin/bash
#
# use feat to run first level analyses

if [[ $# -lt 2 ]]; then
    echo "Usage: run_first_ppi.sh fmriprep_dir subject corral"
    exit 1
fi

fmriprep_dir=$1
subject=$2
corral=$3

out_dir="${fmriprep_dir}/ppi/sub-${subject}/ppi/"

mkdir -p "${out_dir}"

for run in 1 2 3 4; do
    echo "running first level analysis for sub ${subject}..."
#    feat "${out_dir}/sub-${subject}-ppi_first_run-0${run}.fsf"
#
    echo "saving first level output to native directory"
    mkdir "${out_dir}/out_run${run}.feat/native"
    cp -r "${out_dir}/out_run${run}.feat/stats/"* "${out_dir}/out_run${run}.feat/native"
    cp "${out_dir}/out_run${run}.feat/example_func.nii.gz" "${out_dir}/out_run${run}.feat/native/example_func.nii.gz"
    cp "${out_dir}/out_run${run}.feat/mean_func.nii.gz" "${out_dir}/out_run${run}.feat/native/mean_func.nii.gz"
    cp "${out_dir}/out_run${run}.feat/mask.nii.gz" "${out_dir}/out_run${run}.feat/native/mask.nii.gz"
    
    # cope images
    echo "transforming cope images"
    track=1
    for cope in ${out_dir}/"out_run${run}.feat"/native/cope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${out_dir}/"out_run${run}.feat"/stats/cope${track}.nii.gz \
    -n NearestNeighbor \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" \
    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    ((track=track+1))
    done
    
    # cope images
    echo "transforming varcope images"
    track=1
    for cope in ${out_dir}/"out_run${run}.feat"/native/varcope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${out_dir}/"out_run${run}.feat"/stats/varcope${track}.nii.gz \
    -n NearestNeighbor \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" \
    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    ((track=track+1))
    done
    

    # func data
    echo "transforming func data"
    
    fslreorient2std "${out_dir}/out_run${run}.feat/native/example_func.nii.gz" 
    antsApplyTransforms -d 3 -i "${out_dir}/out_run${run}.feat/native/example_func.nii.gz" \
    -o "${out_dir}/out_run${run}.feat/example_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" \
    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    fslreorient2std "${out_dir}/out_run${run}.feat/native/mean_func.nii.gz"
    antsApplyTransforms -d 3 -i "${out_dir}/out_run${run}.feat/native/mean_func.nii.gz" \
    -o "${out_dir}/out_run${run}.feat/mean_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" \
    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"


    # mask
    echo "transforming mask"
    fslreorient2std "${out_dir}/out_run${run}.feat/mask.nii.gz"
    antsApplyTransforms -d 3 -i "${out_dir}/out_run${run}.feat/native/mask.nii.gz" \
    -o "${out_dir}/out_run${run}.feat/mask.nii.gz" \
    -n NearestNeighbor \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" \
    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    echo "formatting reg folder"
    # set up reg folder
    mkdir "${out_dir}/out_run${run}.feat/reg"
    cp /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz "${out_dir}/out_run${run}.feat/reg/standard.nii.gz"

    cp "${corral}/sub-${subject}/anat/sub-${subject}_MNI_ss.nii.gz" "${out_dir}/out_run${run}.feat/reg/highres.nii.gz"

    cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" "${out_dir}/out_run${run}.feat/reg/example_func2standard.mat"

    updatefeatreg "${out_dir}/out_run${run}.feat" -pngs
done


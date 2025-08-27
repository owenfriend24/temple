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
    fsf_base=${corral}/sub-${subject}/univ/
    roi_tag=""
elif [ "$type" == "boundary_inverse" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/univ_inverse/
    fsf_base=${corral}/sub-${subject}/univ/
    roi_tag="inverse"
elif [ "$type" == "ppi" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/ppi/
    fsf_base=${corral}/sub-${subject}/univ/ppi/
    roi_tag="${roi}_"
elif [ "$type" == "ppi_inverse" ]; then
    base=${fmriprep_dir}/sub-${subject}/univ/ppi_inverse/
    fsf_base=${corral}/sub-${subject}/univ/ppi_inverse/
    roi_tag="${roi}_"
fi



mkdir -p ${base}

rm -R "${base}/2ndlevel_ppi_sl-univ_hip.gfeat"


for run in 1 2 3 4; do
  # to try out new boundary ...
    rm -R "${base}/sl-univ_hip_out_run${run}.feat"
    #rm -R "${base}/${roi_tag}out_run${run}.feat"
    #rm -R "${base}/2ndlevel_inverse_boundary.gfeat"

    echo "running first level analysis for sub ${subject} run ${run}..."

    fsf_file=${fsf_base}/sub-${subject}-univ-${type}_${roi_tag}first_run-0${run}.fsf
    #fsf_file=${fsf_base}/sub-${subject}-univ-${type}_first_run-0${run}.fsf
    feat "$fsf_file"
    chmod 775 -R "${corral}/sub-${subject}/transforms"


    
    echo "saving first level output to native directory"
    mkdir "${base}/${roi_tag}out_run${run}.feat/native"
    cp -r "${base}/${roi_tag}out_run${run}.feat/stats/"* "${base}/${roi_tag}out_run${run}.feat/native"
    cp "${base}/${roi_tag}out_run${run}.feat/example_func.nii.gz" "${base}/${roi_tag}out_run${run}.feat/native/example_func.nii.gz"
    cp "${base}/${roi_tag}out_run${run}.feat/mean_func.nii.gz" "${base}/${roi_tag}out_run${run}.feat/native/mean_func.nii.gz"
    cp "${base}/${roi_tag}out_run${run}.feat/mask.nii.gz" "${base}/${roi_tag}out_run${run}.feat/native/mask.nii.gz"
    
    # cope images
    echo "transforming cope images"
    track=1
    for cope in ${base}/"${roi_tag}out_run${run}.feat"/native/cope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${base}/"${roi_tag}out_run${run}.feat"/stats/cope${track}.nii.gz \
    -n NearestNeighbor -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt"  # \
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"

    ((track=track+1))
    done
    
    # cope images
    echo "transforming varcope images"
    track=1
    for cope in ${base}/"${roi_tag}out_run${run}.feat"/native/varcope*; do
    fslreorient2std ${cope}
    antsApplyTransforms -d 3 -i "${cope}" \
    -o ${base}/"${roi_tag}out_run${run}.feat"/stats/varcope${track}.nii.gz \
    -n NearestNeighbor -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt"   # \
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    ((track=track+1))
    done
    
    
    # func data
    echo "transforming func data"
    
    fslreorient2std "${base}/${roi_tag}out_run${run}.feat/native/example_func.nii.gz" 
    antsApplyTransforms -d 3 -i "${base}/${roi_tag}out_run${run}.feat/native/example_func.nii.gz" \
    -o "${base}/${roi_tag}out_run${run}.feat/example_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    fslreorient2std "${base}/${roi_tag}out_run${run}.feat/native/mean_func.nii.gz"
    antsApplyTransforms -d 3 -i "${base}/${roi_tag}out_run${run}.feat/native/mean_func.nii.gz" \
    -o "${base}/${roi_tag}out_run${run}.feat/mean_func.nii.gz" \
    -n BSpline \
    -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
    -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#    -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"


    # mask
    echo "transforming mask"
    fslreorient2std "${base}/${roi_tag}out_run${run}.feat/mask.nii.gz"
    antsApplyTransforms -d 3 -i "${base}/${roi_tag}out_run${run}.feat/native/mask.nii.gz"\
     -o "${base}/${roi_tag}out_run${run}.feat/mask.nii.gz" \
     -n NearestNeighbor \
     -r /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
     -t "${corral}/sub-${subject}/transforms/native_to_MNI_Warp.nii.gz" \
     -t "${corral}/sub-${subject}/transforms/native_to_MNI_Affine.txt" #\
#     -t "${corral}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt"
    
    echo "formatting reg folder"
    # set up reg folder
    mkdir "${base}/${roi_tag}out_run${run}.feat/reg"
    cp /home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz \
    "${base}/${roi_tag}out_run${run}.feat/reg/standard.nii.gz"

    cp "${corral}/sub-${subject}/anat/sub-${subject}_MNI_ss.nii.gz" \
    "${base}/${roi_tag}out_run${run}.feat/reg/highres.nii.gz"

    cp "/home1/09123/ofriend/analysis/temple/univ/identity.mat" \
    "${base}/${roi_tag}out_run${run}.feat/reg/example_func2standard.mat"

    updatefeatreg "${base}/${roi_tag}out_run${run}.feat" -pngs
done

feat "${corral}/sub-${subject}/univ/ppi/sub-${subject}-univ-ppi_sl-univ_hip_second_level.fsf"
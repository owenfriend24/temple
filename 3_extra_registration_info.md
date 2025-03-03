# Image Registration:
Notes:
* need to use idev or jobs for ants transformation, too much memory to do on login nodes
* see mni_transforms.sh,, prep_func_data.sh, and run_first_levels.sh for examples of transformations between three spaces in action

## Components:
* T1w anatomical image path (e.g. sub-temple057_desc-preproc_T1w.nii.gz)
* Data to transform
  * BOLD data in T1 space (e.g. sub-temple057_task-collector_run-01_space-T1w_boldref.nii.gz)
  *   e.g., Z-stat map from 1st level analyses
* MNI 1mm structural brain (/work/03206/mortonne/software/apps/fsl-5.0.11/data/standard/MNI152_T1_1mm_brain.nii.gz)

## Types of interpolation:
* nearest-neighbor: for binary data (e.g., masks) - for each voxel in an ROI, looks at nearby voxels to see if it's included or not
* B-spline: for functional data - uses histogram for nearby voxels, smoother data

## Load needed modules
```
source $HOME/analysis/temple/.profile_onesubject
module load fsl
module load ants
```

## Skullstripping T1 image
```
fslmaths {T1w anatomical image path} -mas {gray matter mask} {outpath}
```
* -mas flag defines next input as mask
  
example: 
```
fslmaths sub-temple057_dec-preproc_T1w.nii.gz -mas sub-temple057_desc-brain_mask.nii.gz sub-temple057_desc-preproc_T1w_ss.nii.gz
```

## Create warp images and affine files for anatomical/functional and functional/MNI transformations (both directions)
### Anatomical/functional
```
ANTS 3 -m MI[ {fixed image (space we're registering to)}, {moving image (image we're moving into fixed image's space)},1,32] -o {outpath} --rigid-affine true -i 0
```
* 3 refers to dimensions of image
* 1,32
  * 1 = bins used in histogram for mutual information calculation, 32 = smoothing factor
  * rigid affine = no scaling or shearing
  * -i 0 = 0 iterations; no extra iterations needed for optimization since we know what space we're registering to
    
example:
```
ANTS 3 -m MI[ ./func/sub-temple057_task-collector_run-01_space-T1w_boldref.nii.gz, ./anat/sub-temple057_desc-preproc_T1w_ss.nii.gz,1,32] -o ./affines/brain2refvolunwarp_ --rigid-affine true -i 0
```
### Anatomical/MNI
```
ANTS 3 -m PR[ {fixed image (path to MNI 1mm brain)}, {moving image (skull-stripped T1 anatomical)}, 1,4] -t SyN[0.25] -r Gauss[3,0] -o {outpath} -i 30x90x20 --use-Histogram-Matching
```
example:
```
ANTS 3 -m PR[ /corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz, ./anat/sub-temple058_desc-preproc_T1w_ss.nii.gz , 1,4] -t SyN[0.25] -r Gauss[3,0] -o ./affines/brain2MNI_ -i 30x90x20 --use-Histogram-Matching
```

## Use warp images and affine files to move between anatomical, functional, and MNI space
```
WarpImageMultiTransform 3 {image to be moved} {outpath for new image} -R {MNI 1mm image} {warp image} {space to move image to (e.g. MNI 1mm brain)} --use-BSpline
```
### Anatomical to MNI
example:
```
WarpImageMultiTransform 3 ./anat/sub-temple058_desc-preproc_T1w_ss.nii.gz ./anat/sub-temple058_desc-preproc_T1w_MNI.nii.gz -R /corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz ./affines/brain2MNI_Warp.nii.gz ./affines/brain2MNI_Affine.txt --use-BSpline
```

## Functional space (i.e. BOLD data, z stat map) to MNI
```
WarpImageMultiTransform 3 ./func/sub-temple058_task-collector_run-01_space-T1w_boldref.nii.gz ./func/sub-temple058_task-collector_run-01_space-T1w_boldref_toMNI.nii.gz -R /corral-repl/utexas/prestonlab/xmaze/batch/templates/MNI152_T1_1mm_brain.nii.gz ./affines/brain2MNI_Warp.nii.gz ./affines/brain2MNI_Affine.txt --use-BSpline
```



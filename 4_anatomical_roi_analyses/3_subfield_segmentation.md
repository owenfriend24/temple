### implementing Automated Segmentation of Hippocampal Subfields (ASHS)
* using custom developmental atlas
  * CA2, CA3, DG are not differentiated due to difficulty segmenting in fMRI scans of this resolution
  * four subfields: CA1, CA23DG, subiculum, posthipp

1. prepare T1w image for processing
  * T1w image will be created while post-processing functional data (within prep_func_data.sh)
  * use skullstripped image: sub-{subject}_T1w_ss.nii.gz
2. prepare T2w image for processing
  * fmriPrep does minimal processing to the T2w image but does transform it to T1w coordinate space - this is a problem as ASHS expects coordinates as formatted in the original image (i.e., z-coordinate has lowest resolution; x,y,z = 384, 384, 60)
  * thus, we need to prepare the raw T2w image while maintaining it's dimensions
    * run N4BiasFieldCorrection and bet brain extraction, moving the final image into the ASHS directory 
```
prep_coronal.sh {subject}
```
3. run ashs - using 2016 version to maintain functionality with our custom atlas (Yushkevich et al., 2015b)
```
run_ashs_test.sh {subject}
```
4. save out subfield masks in both anatomical (T1w) and functional space
```
subfield_masks.sh {subject} {ashs_dir}
```
4b. will need to update these scripts to save final information in corral, currently between scratch and work due to disk issues

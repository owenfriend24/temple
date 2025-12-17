### identifying group-level clusters using FSL's randomise

1. concatenate subject z-maps in MNI space
* adds each subject image as a 'timepoint' (i.e., 4th dimension)
```
fslmerge -t group_z.nii.gz sub-temple*
```
2. create design matrices using Feat's GLM tool
* primary modulators will be performance and age
 * these will obviously covary but may still diverge somewhat, particularly for younger participants
 * parametric modulators must be demeaned so that 0 reflects baseline age/performance

3. run randomise using parametric regressors as well as one-sample to look for shared representation
```
randomise_new.sh $fmriprep_dir $comp
randomise_new.sh $FM AC
```

4. extract cluster maps and info
```
cluster -i GROUP_IMAGE -t 0.99 --minextent=THRESHOLD --oindex=OUT_NAME
```
for within hip, need to run on a masked image:
```
fslmaths GROUP_IMAGE -mas $HOME/analysis/temple/bin/templates/b_hip_func.nii.gz HIP_IMAGE
cluster -i HIP_IMAGE -t 0.99 --minextent=THRESHOLD --oindex=OUT_NAME
```

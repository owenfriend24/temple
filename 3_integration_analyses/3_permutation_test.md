### identifying group-level clusters using FSL's randomise

1. concatenate subject z-maps in MNI space
* adds each subject image as a 'timepoint' (i.e., 4th dimension)
```
fslmerge -t group_z.nii.gz sub-temple*
```

2. create design matrices using Feat's GLM tool
* to identify developmental differences, perform permutation testing with age as parametric modulator
 * parametric modulators must be demeaned so that 0 reflects baseline age/performance
* contrasts can be weighted as +1 (integration increasing w/ age) or with -1 (integration decreasing w/age)

3. run randomise using parametric regressors; additionally run one-sample test to look for shared (i.e., age-invariant) representation
```
randomise.sh b_hip AB
randomise.sh b_gray_func AC
```

4. extract cluster maps and info
```
cluster -i GROUP_IMAGE -t 0.99 --minextent=THRESHOLD --oindex=OUT_NAME
```

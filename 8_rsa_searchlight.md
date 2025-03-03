## Whole brain searchlight for within-triad similarity and AC similarity
## to-do; write out the exact logic of the searchlight function, make sure all paths are absolute for parallel processing (no cd commands)

### 1. activate rsa profile
```
source $HOME/analysis/temple/rsa/bin/activate
```
### 2. Searchlight 
* calls temple_function_prepost.py function
```
temple_sl_prepost.py temple071 whole_brain
```

### 3. whole brain / FS hippocampus RSA
* calls prepost_roi.py
* to pull values for statistical analyses
  
```
mni_hip_masks.sh $FM temple071
ac_rs_values.py temple071 sl AC
```

* some commented out code related to residuals in betaseries_est.py - pretty sure don't need that anymore because I have pull_resid.py function but left just in case it comes up later

### cluster
cluster -i {input} -t 0.99 --minextent= ### --oindex = {output mask}


### MDS within extracted SL ROI masks - didn't really pan out with first try but can come back to later
sl_masks_to_func.sh temple016 $FM AC adult_IFG_AC_mask
mds_sub.py $FM temple016 $FM/sub-temple016/transforms/adult_IFG_AC_mask.nii.gz adult_IFG_AC
batch_mds_subs.sh $adults



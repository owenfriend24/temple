## Whole brain searchlight for pre-post representational similarity change

### 1. activate rsa profile
```
source $HOME/analysis/temple/rsa/bin/activate
```
### 2a. Run RSA searchlight
* parameters:
  * subject (e.g., 'temple016')
  * comparison
    * AB - compares similarity change for 1st and 2nd item in triplet to 1st and 2nd items from different triplets
      * BC - same thing for 2nd/3rd item, though generally less strong changes
    * AC - compares similarity change for 1st and 3rd item in triplet to 1st and 2nd, 2nd and 3rd items from different triplets
      * does NOT compare against 1st and 3rd item from different triplets because they can be directly observed in sequence (i.e. abC-Abc), while within triplet cannot (AbC)
    * AC_weak - compares similarity change for 1st and 3rd item in triplet to 1st and 3rd items from different triplets which can sometimes be observed directly together (weak pairs) (Schapiro et al., 2012)
    * AC_differentiation - compares similarity change for 1st and 3rd item from different triplets to 1st/2nd or 2nd/3rd items from different triplets
      * returns z-map for AC_across < AB/BC_across, (i.e., less similar after learning to emphasize unpredictable relaitonship; differentiation)
  * masktype
    * gm - subject-specific gray matter mask derived from freesurfer parcellations
    * hip - lateral?
  * --drop_run
    * choose a run (1-6) to drop if necessary due to excessive motion. searchlight will not include functional data from that run 

```
temple_sl_prepost.py temple001 AB gm
temple_sl_prepost.py temple002 AC_differentiation hip --drop_run=6
```
### 2b. Batch run RSA searchlight
* running subjects in parallel generally results in more failed searchlights than running iteratively
* can also transform to MNI space directly after running, but will throw errors if SL fails, need to double-check each subject
```
batch_sl.sh AC_weak gm
```

### 3. extract RS values from specific clusters or ROI's
1. extracts RS values for each comparison from each subject within ROI
2. merge/format RS values in subject-level CSV
3. aggregate across subjects for master CSV file
* parameters:
  * measure
    * prepost, symmetry, both
  * master_dir
    * where subject-level csv's are stored (e.g., $CORR/integration_prepost)
  * comparison
    * AB, BC, AC
  * mask
    * b_hip_subregions, lat_hip_subregions, hip_subfields, b_hip_subfields, searchlight
      * if extracting from searchlight regions, use sl_masks_to_func.sh to back project searchlight clusters into subject-level functional space
  * --agg_file
    * True = write the aggregated file out to master_dir, default = False (just run for each subject)
  

### 4. to-do: integrate jupyter notebooks/R code
* analysis/**integration_prepost**/clean_data.ipynb
* 
### old: MDS within extracted SL ROI masks - didn't really pan out with first try but can come back to later; these functions pull out run-level similarity/distances between the 12 items, jupyter notebook does the actual multidimensional scaling 
* need to make sure to transform to fisher's Z before averaging
sl_masks_to_func.sh temple016 $FM AC adult_IFG_AC_mask
mds_sub.py $FM temple016 $FM/sub-temple016/transforms/adult_IFG_AC_mask.nii.gz adult_IFG_AC
batch_mds_subs.sh $adults



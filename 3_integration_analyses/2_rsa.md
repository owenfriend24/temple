## Whole brain searchlight for pre-post representational similarity change
* In this searchlight analysis, local multivoxel patterns are split into pre- and post-learning phases, and representational similarity matrices are computed separately for each phase using a pairwise similarity metric. Integration is quantified as the change in similarity from pre to post (Fisher-z transformed), specifically contrasting increases for within-triad item pairs against across-triad pairs while controlling for run effects. A permutation test within each searchlight sphere estimates a normalized statistic indicating where local representations become more integrated over learning

### 1. activate rsa profile
```
source $HOME/analysis/temple/rsa/bin/activate
```
### 2. Run RSA searchlight
* parameters:
  * subject (e.g., 'temple016')
  * comparison
    * AB - compares similarity change for 1st and 2nd item in triplet to 1st and 2nd items from different triplets
      * BC - same thing for 2nd/3rd item, though generally less strong changes
    * AC_weak - compares similarity change for 1st and 3rd item in triplet to 1st and 3rd items from different triplets which can sometimes be observed directly together (weak pairs); this is the most similar test to Schapiro et al., 2012 and what is reported in the manuscript
    * AC_differentiation - compares similarity change for 1st and 3rd item from different triplets to 1st/2nd or 2nd/3rd items from different triplets
      * returns z-map for AC_across < AB/BC_across, (i.e., less similar after learning to emphasize unpredictable relaitonship; differentiation)
    * AC - compares similarity change for 1st and 3rd item in triplet to 1st and 2nd, 2nd and 3rd items from different triplets
      * does NOT compare against 1st and 3rd item from different triplets because they can be directly observed in sequence (i.e. abC-Abc), while within triplet cannot (AbC)
  * masktype
    * gm - subject-specific gray matter mask derived from freesurfer parcellations
    * hippocampus - runs in both lateral and bilateral anatomical hippocampal masks
  * --drop_run
    * choose a run (1-6) to drop if necessary due to excessive motion. searchlight will not include functional data from that run 

e.g., 
```
temple_sl_prepost.py temple001 AB gm
temple_sl_prepost.py temple002 AC_differentiation hippocampus --drop_run=6
```

### 3. extract RS values from specific clusters or a priori ROI's
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
  




## functions to extract integration/symmetry values from a priori regions of interest

### 1. extract pre-post representational change for AC pairs compared with same logic as searchlight analyses
* these functions will automatically deal with dropped runs as long as they are correctly inputted in the dictionary and beta images have correctly excluded the necessary runs
```
integration_prepost_values.py subject comparison mask
integration_prepost_values.py temple016 AC b_hip_subregions
```
### 1.1. concatenate all comparison values for a subset of masks within a formatted csv file
```
merge_integration.py temple016 $CORR/integration_prepost AB b_hip_subregions
```

### 2. extract ApreBpost, ApostBpre, etc. for additional measure of integration and representational symmetry
```
symmetry_prepost_values.py subject comparison mask
symmetry_prepost_values.py temple016 AC b_hip_subregions
symmetry_prepost_values.py temple016 CA b_hip_subregions
```
### 2.1. concatenate all comparison values for a subset of masks within a formatted csv file
```
merge_asymm.py subject master_dir comparison mask
```

### 3. aggregate prepost or symmetry data from all subjects for comparisons (in progress)
* will automatically run the above functions for each subject
* arguments:
  * measure: prepost, symmetry, or both
  * master_dir: folders containing .txt files for each comparison are stored (e.g., $CORR/integration_prepost)
  * comparison: AB, BC, AC
  * mask:  b_hip_subregions, ifg_subregions, b_hip_subfields
  * --agg_file (optional flag): type=bool, default=False; write out an aggregated subject file or not (if not, just creates for the individual subjects)
example call (untested):
```
aggregate_integration.py both $CORR/integration_prepost AC b_hip_subregions --agg_file=True
```

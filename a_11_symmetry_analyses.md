## Quantifying symmetry of memory representations based on Schapiro et al., 2012 (Current Bio)
* Goal is to quantify integration as ApostBpre and ApostCpre and then compare to ApreBpost and ApreCpost
* If Item A evokes Item B, that's evidence of integration in one direction.
* If Item B also evokes Item A, we have a symmetrical memory representation indicative of integration in both directions.
* If Item A evokes Item B but Item B does not evoke Item A, we have an asymmetrical memory representation


* one option - run a searchlight (haven't done for full group at this point)
  * same approach as a typical searchlight when going from subject to group level
   ```
   sl_symmetry.py temple016 whole_brain AB
   ```
* current approach (as in Schapiro et al., 2012)
  * pull ApostBpre, ApostCpre, ApreBpost, ApreCpost values from anatomical ROI's
    *  current ROI's are hippocampus and its subregions, eventually will want to add other MTL structures as well as hippocampal subregions
1. ApostBpre and ApostCpre
```
sl_symmetry_values.py SUBJECT MASK COMPARISON
```
e.g., 
```
sl_symmetry_values.py temple016 sl_hip AB
sl_symmetry_values.py temple016 sl_hip AC
sl_symmetry_values.py temple016 sl_hip BC
```
1b. ApostBpre and ApostCpre for subjects with a pre- or post-exposure run excluded due to motion
```
sl_symmetry_values_droprun.py SUBJECT MASK COMPARISON DROPPED_RUN
```
e.g., 
```
sl_symmetry_values_droprun.py temple023 sl_hip AC 6
```

2. ApreBpost and ApreCpost
* kind of hard-coded right now for whether it's AB or AC, can go back and make code nicer later on
```
sl_symmetry_values_BA.py SUBJECT MASK COMPARISON
sl_symmetry_values_CA.py SUBJECT MASK COMPARISON
sl_symmetry_values_BC.py temple016 sl_hip AC
```
* these also all call the same function (sl_symm_values_function_BA.py) but use the different beta directories to do the correct comparisons, can go back and code more efficiently later
e.g.,
```
sl_symmetry_values_BA.py temple016 sl_hip AB
sl_symmetry_values_CA.py temple016 sl_hip AC
```
2b. ApreBpost and ApreCpost for subjects with a pre- or post-exposure run excluded due to motion (same logic as 1b.)
```
sl_symmetry_values_BA.py temple023 sl_hip AB 6
sl_symmetry_values_CA.py temple070 sl_hip AC 3
```


3. Download relevant .txt files via CyberDuck, aggregate for analysis in R in [Jupyter Notebook](http://localhost:8888/notebooks/Documents/temple_local/analysis/searchlight/symmetry_analyses.ipynb?)
  

5. Analyze in R - /Users/owenfriend/Document/temple_local/analysis/searchlight/asymmetry_analyses.R
    * Note; I'm an idiot and spelled asymmetry wrong in the current aggregated file. Fixed in Jupyter Notebook but will need to fix in R after generating new aggregated file






## new versions (need to update md files)
```
integration_prepost_values.py subject comparison mask
integration_prepost_values.py temple016 AC b_hip_subregions
symmetry_prepost_values.py subject comparison mask
symmetry_prepost_values.py temple016 AC b_hip_subregions
symmetry_prepost_values.py temple016 CA b_hip_subregions
merge_asymm.py subject master_dir comparison mask
merge_integration.py temple016 $CORR/integration_prepost AB b_hip_subregions
```



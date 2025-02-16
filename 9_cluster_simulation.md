1. pull noise derived from residuals of GLM's used to model searchlight data
```
pull_resid.py $FS $FM temple_069
```
2. pull autocorrelation function parameters
```
temple_acf.sh $FM temple_069
```
3. create group mask
```
group_masks.py $FS $FM adult
```
4. cluster simulation - run in both whole brain and hippocampus (i.e., small volume correction)
   * pull average acf coefficient values by age group from http://localhost:8888/notebooks/Documents/temple_local/analysis/extract_acf.ipynb?
```
clust_sim.sh $FM

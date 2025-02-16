1. create design matrices using Feat's GLM tool
* open virtual desktop using tap.https://tap.tacc.utexas.edu/
* Feat &
* Glm tool
* for current results -
  * by group: two binary columns (child and adult)
    * contrasts: group mean (1, 1), child mean (1, 0), adult mean (0, 1), child over (1, -1), adult over (-1, 1) 

```
cluster -i GROUP_IMAGE -t 0.99 --minextent=THRESHOLD --oindex=OUT_NAME
```
for within hip, need to run on a masked image:
```
fslmaths GROUP_IMAGE -mas $HOME/analysis/temple/bin/templates/b_hip_func.nii.gz OUT
```

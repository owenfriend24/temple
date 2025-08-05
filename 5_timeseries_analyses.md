# Time series analyses
  * funcitons assume neural and behavioral data are post-processed (see markdown's 2-4)
### Univariate - sensitivity to triplet boundaries
1. create formatted .txt files for statistical learning runs
  * parameters:
    * subject (e.g. temple001)
    * file_type (motion, collector, both)
```
boundary_univ_txt_files.py temple001 both
```
2. create first-level .fsf file based on template to run univariate analysis using Feat
  * parameters:
    * subject (e.g., temple001)
    * file_type (boundary)
```
edit_first_fsf.sh temple001 boundary
```
3. run first-level models and transform output to MNI 1.7mm functional space
  * parameters
    * fmriprep_dir - output directory, should generally use scratch ($FM) due to size of outputted directories
    * subject (e.g., temple001)
    * corral - path to temple directory on corral for transformation warp images/affines
    * file_type (boundary)
```
run_first_feats.sh $FM temple001 $CORR boundary
```
4. create second-level .fsf file based on template to compare runs
  * template includes average across four runs, run 1 > run 4 contrast, and run 4 > run 1 contrast
  * subjects with runs excluded for motion point to alternate templates
  * parameters:
    * subject (e.g., temple001)
    * file_type (boundary)
```
edit_second_fsf.sh temple001 boundary
```
5. run second level analyses using feat
```
slaunch -J run_2nd "feat $CORR/sub-{}/univ/sub-{}-univ-boundary_second_level.fsf" $SUBS -N 1 -n 90 -r 02:00:00 -p development
```
6. run third level analysis using feat
   


### Psychophysiological interaction (PPI) - enhanced or decreased connectivity at triplet boundaries
1. extract .txt timeseries of eigenvalue (first principal component) from selected region of interest
  * assumes subject's mask for selected ROI has already been created in native functional space
  * .txt file will be saved in sub/univ/ppi and is formatted for use in either enhanced (ppi) or decreased (ppi_inverse) connectivity analyses
  * parameters:
    * subject (e.g. temple001)
    * roi (b_hip, sl, etc.)
```
ppi_extract_eigen.sh temple001 b_hip
```
2. create formatted .txt files for statistical learning runs, separate contrasts for enhanced vs decreased connectivity
  * will create enhanced connectivity files in sub/univ/ppi and decreased connectivity files in sub/univ/ppi_inverse
    * shared files (i.e., motion) will be sub/univ/ppi 
  * parameters:
    * subject (e.g. temple001)
    * file_type (motion, collector, both)
```
ppi_txt_behav.py temple001 both
```
3. create first-level .fsf file based on template to run univariate analysis using Feat
  * parameters:
    * subject (e.g., temple001)
    * file_type (ppi, ppi_inverse)
    * roi (b_hip, sl)
```
edit_first_fsf.sh temple001 ppi b_hip
```
4. run first-level models and transform output to MNI 1.7mm functional space
  * parameters
    * fmriprep_dir - output directory, should generally use scratch ($FM) due to size of outputted directories
    * subject (e.g., temple001)
    * corral - path to temple directory on corral for transformation warp images/affines
    * file_type (ppi, ppi_inverse)
    * roi (b_hip, sl)
```
run_first_feats.sh $FM temple001 $CORR ppi_inverse sl
```
5. create second-level .fsf file based on template to compare runs
  * template includes average across four runs, run 1 > run 4 contrast, and run 4 > run 1 contrast
  * subjects with runs excluded for motion point to alternate templates
  * parameters:
    * subject (e.g., temple001)
    * file_type (ppi, ppi_inverse)
    * roi (b_hip, sl)
```
edit_second_fsf.sh temple001 ppi b_hip
```
6. run second level analyses using feat
```
slaunch -J run_2nd "feat $CORR/sub-{}/univ/sub-{}-univ-ppi_b_hip_second_level.fsf" $SUBS -N 1 -n 90 -r 02:00:00 -p development
```
7. run third level analysis using feat


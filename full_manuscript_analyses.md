# Hippocampal representations of temporal regularities increase in scale and symmetry across development
Analyses are reported below in the same order that they appear in the main manuscript (see Results, STAR Methods, Supplement for extended descriptions analysis logic and details). Pre-processing and many initial analysis stages are written to be implemented in high-performance computing environments, while final inferential statistics and subsequent figure generation are primarily carried out in linked Jupyter and R Notebooks. Analyses are described in greater detail within linked folders, all of which include their own step-by-step markdowns. Example calls to functions also provided, including example launch commands for SLURM jobs and recommended parameters for parallel (multi-subject) or more computationally intensive processing when necessary.


## 1. Pre- and post-process raw fMRI and behavioral data using fMRIprep ([extended protocol](https://github.com/owenfriend24/temple/tree/main/1_process_raw_data))
1.1. Source project profile to set paths
```
source /home1/09123/ofriend/analysis/temple/profile
```

1.2. Convert raw [DICOM](https://github.com/owenfriend24/temple/blob/main/1_process_raw_data/2_extra_preprocessing_info.md) data to BIDS
```
temple_heudiconv.sh $subject $raw_data_dir $heuristic_file $fmriprep_dir
```
```
slaunch -J heudiconv "temple_heudiconv {} $raw_data_dir $heuristic_file $fmriprep_dir" $subject(s) -N 1 -n $num_subjects -r 00:20:00 -p development
```
1.3. Update metadata to assign fieldmaps to corresponding functional scans
```
temple_bids_post.py $bids_dir
```
1.4. Run fMRIPrep
```
temple_fmriprep.sh $bids_dir $subject
```
```
slaunch -J fmriprep "temple_fmriprep.sh $bids_dir {}" $subject(s) -N 1 -n $num_subjects -r 08:00:00 -p normal
```

1.5. Post-process functional data to skullstrip, generate transformaitons to template space, smooth
```
prep_func_data.sh $freesurfer_dir $fmriprep_dir $subject
```
```
slaunch -J prep "prep_func_data.sh $freesurfer_dir $fmriprep_dir {}" $subject(s) -N 1 -n $num_subjects -r 02:00:00 -p development
```

1.5.1 Copy data from scratch to permanent directory - this will depend on cluster setup, but I pre- and post-process all fMRI data in scratch (temporary storage) to save space, and copy all relevant files to permanent storage afterwards
* procedural note: this means that bids_dir above this point refers to BIDS-formatted temporary storage where preliminary processing is hpapning, while bids_dir below this point refers to BIDS-formatted permanent storage where all subsequent analyses happen

1.6. Generate custom gray-matter mask in native space for each subject from freesurfer output
```
create_gm_mask.sh $subject
```
1.7. Generate custom hippocampal masks in native space for each subject by reverse-normalizing custom template
```
create_hip_masks.sh $subject $bids_dir $task
```
* task = temple, I use the same function and hippocampal masks for multiple studies which is why the task argument is built in
---

## 2. Assess behavioral differences in statistical learning
2.1. Aggregate performance on memory task, download to local machine (I use CyberDuck)
```
clean_remember.py --by_subject AGGREGATE $bids_dir
```
2.2. Add subject-level info (age, sex) [jupyter_notebook]()
2.3. Analyze developmental differences in behavioral perfomance [R notebook]()


---


## 3. Implement searchlight analyses to identify regions in which sequence representations are integrated
3.1. Estimate item-level activity patterns (neural representations) for each stimulus, concatenate by experimental phase [analysis logic]()
```
batch_betaseries.sh $subject
```
3.2. Activate RSA virtual environment (separate from primary analysis environment to maintain functionality for adapted PyMVPA2 package)
```
rsa
```
3.3. Run searchlight analyses by comparison and region of interest, transform to template space for group comparison
```
temple_sl_prepost.py ???
sl_to_mni.sh
```
3.4. Generate probablistic (> 50% of subjects w/ active voxels) group-level anatomical mask for cluster simulation
```
CODE?
```

3.5. Simulate null by calculating smoothness (autocorrelation) of GLM residuals within group-level anatomical mask and cluster size expected by chance
```

```

3.6. Permutation test to ...(more logic here)
```
```
3.7. Identify continuous clusters from voxelwise permutation test and compare to null threshold derived above
*

3.8. Extract integration values (representational similarity change) within searchlight-defined regions of interest
```
aggregate_integration.py ...
```
**3.9. [manuscript_integration_analyses](https://github.com/owenfriend24/temple/blob/main/R_mds/2_integration.md)**


---


## 4. Quantify representational symmetry in anatomical regions of interest
4.1. Extract and aggregate symmetry values across subjects by comparison, region(s)
```
aggregate_integration.py ???
```
4.2. Download master CSV to local; clean and inspect for analysis
{jupyter nb}
4.3. Analyze and plot developmental differences in representationl symmetry


---


## 5. Time-series analyses to capture neural sensitivity to temporal structure











# Hippocampal representations of temporal regularities increase in scale and symmetry across development
Analyses are reported below in the same order that they appear in the main manuscript (see Results, STAR Methods, Supplement for extended descriptions analysis logic and details). 

Pre-processing and many initial analysis stages are written to be implemented in high-performance computing environments, while final inferential statistics and subsequent figure generation are primarily carried out in linked Jupyter and R Notebooks. 

Some analyses are described in greater detail within linked folders, all of which include their own step-by-step markdowns. Example calls to functions also provided, including example launch commands for SLURM jobs and recommended parameters for parallel (multi-subject) or more computationally intensive processing when necessary.


## 1. Pre- and post-process raw fMRI and behavioral data using fMRIprep 
([extended protocol](https://github.com/owenfriend24/temple/tree/main/1_process_raw_data))

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
2.1.1 Aggregate performance on memory task, download to local machine (I use CyberDuck)
```
clean_remember.py --by_subject AGGREGATE $bids_dir
```

2.1.2 Add subject-level age (years and months) and sex from master participant demographics (omitted here for anonymity)

2.2. Analyze developmental differences in behavioral perfomance: **[manuscript behavioral analyses](https://github.com/owenfriend24/temple/blob/main/R_mds/1_behavior.md)**

---

## 3. Implement searchlight analyses to identify regions in which sequence representations are integrated at different temporal scales
3.1. Estimate item-level activity patterns (neural representations) for each stimulus, concatenate by experimental phase [analysis logic](https://github.com/owenfriend24/temple/blob/main/3_integration_analyses/1_betaseries_estimation.md)
```
batch_betaseries.sh $subject
```

3.2. Activate RSA virtual environment (this environment is kept separate from primary analysis environment to maintain functionality for lab-native adapted PyMVPA2 packages)

3.3. Run searchlight analyses by comparison and region of interest, transform to template space for group comparison ([extended protocol](https://github.com/owenfriend24/temple/blob/main/3_integration_analyses/2_rsa.md))
* comparison: **AB** (adjacent) or **AC** (extended)
* rois: **hippocampus** (subject-specific hippocampal masks back-projected into nativve space; includes bilateral, left, and right) or **gm** (subject-specific gray matter mask in native space)
* --drop_run - optional flag for subjects with any missing or excluded runs
* the adapted packages we use for searchlight analyses do not always save out properly when parallelizing subjects; I recommend running one subject at a time and comparison code is vectorized to make this as efficient as possible (~2 minutes per subject)
```
temple_sl_prepost.py AB hippocampus
sl_to_mni.sh $bids_dir AB b_hip
```

3.4. Generate probablistic (> 50% of subjects w/ active voxels) group-level anatomical mask for cluster simulation
* warps all native masks to template space, binarizes, and averages
* can be done for all subs (age_group='all') or separately for 'child' or 'adult'
```
group_masks.py $freesurfer_dir $bids_dir all
```

3.5. Simulate null by calculating smoothness (autocorrelation) of GLM residuals within group-level anatomical mask and cluster size expected by chance
* this step is set up to pull residuals and assess autocorrelation in same temporary storage where pre-processing is implemented (fmriprep_dir)
* ACF coefficients outputted from temple_acf.sh should be averaged and added to clust_sim.sh for each ROI
* clust_sim.sh will output matrices for different pairs of voxelwise/cluster thresholds. we use 2D 2nd nearest neighbor clustering with voxelwise threshold p < .01 and cluster threshold p < .05
```
pull_resid.py $freesurfer_dir $bids_dir $sub
temple_acf.sh $bids_dir $subject $fmriprep_dir $roi
clust_sim.sh $bids_dir
```

3.6. Implement nonparametric permutation-testing with repeated label shuffling to assess voxelwise statistical significance ([extended_protocol](https://github.com/owenfriend24/temple/blob/main/3_integration_analyses/3_permutation_test.md))
* first, create .mat and .con files using FSL gui with age (de-meaned) as parametric modulator
* next, concatenate z-maps in template space from above step into single 4D group image (in SAME ORDER as parametric modulator matrix)
```
randomise.sh $roi $comparison
randomise.sh b_hip AB
```

3.7. Identify continuous clusters from voxelwise permutation test and compare to null threshold derived above 
* randomise outputs (1-p) maps, so threshold of 0.99 corresponds to voxelwise significance < .01
```
cluster -i randomise_output.nii.gz -t 0.99 --minextent=$threshold --oindex=$integration_map.nii.gz
```
* save out significant clusters as binary masks
```
fslmaths integration_map.nii.gz -thr $cluster_index -uthr $cluster_index -bin cluster.nii.gz
```

3.8. Extract integration values (representational similarity change) within searchlight-defined regions of interest
```
aggregate_integration.py $measure $integration_data_dir $comparison $mask_type
aggregate_integration.py prepost $bids_dir/integration_prepost AB searchlight
```
**3.9. Confirm age differences in representational scale identified via nonparametric permutation testing above, assess consequent effect on behavior: [manuscript_integration_analyses](https://github.com/owenfriend24/temple/blob/main/R_mds/2_integration.md)**

---


## 4. Quantify representational symmetry in anatomical regions of interest
4.1. Extract and aggregate symmetry values across subjects by comparison, region(s)
* this is the same function we use above to quantify pre-post integration, but with a differently specified comparison
* because symmetry is a subtraction (see Schapiro et al., 2012), we cannot use a searchlight approach, and instead have to use a more conservative approach in which values are averaged across full anatomical ROIs
```
aggregate_integration.py **symmetry**  $bids_dir/integration_prepost AB lat_hip_subregions
```
4.2. Download master CSV to local; clean and inspect for analysis: [jupyter notebook](https://github.com/owenfriend24/temple/blob/main/jupyter/clean_roi_data.ipynb)

4.3. Analyze and plot developmental differences in representationl symmetry: **[manuscript_symmetry_analyses](https://github.com/owenfriend24/temple/blob/main/R_mds/3_symmetry.md)**

4.4 Based on adult literature, we can also compute symmetry in hippocampal subfields, identified in subject-specific masks derived from semi-automated hippocampal segmentation with custom developmental atlas; see manuscript supplement ([extended logic](https://github.com/owenfriend24/temple/blob/main/4_anatomical_roi_analyses/3_subfield_segmentation.md))

---


## 5. Time-series analyses to capture neural sensitivity to temporal structure











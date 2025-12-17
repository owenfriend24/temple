# Hippocampal representations of temporal regularities increase in scale and symmetry across development
Analyses are reported below in the same order that they appear in the main manuscript (see Results, STAR Methods, Supplement for extended descriptions analysis logic and details). Pre-processing and many initial analysis stages are written to be implemented in high-performance computing environments, while final inferential statistics primarily carried out in linked Jupyter and R Notebooks. Analyses are described in greater detail within linked folders, all of which include step-by-step markdowns


## 1. Pre- and post-process raw fMRI and behavioral data ([extended protocol](https://github.com/owenfriend24/temple/tree/main/1_process_raw_data))

1.1. Convert raw [DICOM](https://github.com/owenfriend24/temple/blob/main/1_process_raw_data/2_extra_preprocessing_info.md) data to BIDS
```
slaunch -J heudiconv "temple_heudiconv.sh {} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/temple_heuristic.py $SCRATCH/temple/new_prepro" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```
1.2. Update metadata to map fieldmaps to functional scans
```
temple_bids_post.py $SCRATCH/temple/prisma_prepro
```
1.3. Run fMRIPrep
```
slaunch -J fmriprep “temple_fmriprep.sh $SCRATCH/temple/prepro_data {}" $BIDIDS -N 1 -n 1 -r 08:00:00 -p normal
```
1.4. Post-process functional data to skullstrip, generate transformaitons to template space, smooth
```
prep_func_data.sh freesurfer_dir fmriprep_dir subject
```
1.5. Generate custom gray-matter mask in native space for each subject from freesurfer output
```
CODE?
```
1.6. Generate custom hippocampal masks in native space for each subject by reverse-normalizing custom template
```
CODE?
```

---

## 2. Assess behavioral differences in statistical learning
2.1. Aggregate performance on recognition task, download to local machine
```
clean_remember ...
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



---


## 4. Quantify representational symmetry in anatomical regions of interest

## 5. Time-series analyses to capture neural sensitivity to temporal structure











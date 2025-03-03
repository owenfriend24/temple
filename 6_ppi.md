### benchmark analysis - whole hippocampus as seed, test for connectivity differences during boundary trials for early vs. later learning

1 (old). create bilateral hippocampus mask based on freesurfer output, extract eigenvariate value for each TR and format as .txt file
```
ppi_hpc_mean.sh freesurfer_dir fmriprep_dir subject task
```
1. (new). use custom MNI hippocampus mask reverse-normalized into participant space, extract eigenvalue and save out
* need to create the hippocampal masks first (mni_hip_masks.sh $FM $sub $CORR
```
ppi_hip_new.sh $FM temple016 collector $CORR
```
3. create 2 .txt files for participant's behavior, including contrast of interest and trials to include
```
ppi_txt_behav.py fmriprep_dir both subject out_dir/
```
3. create first level .fsf file based on template, run with Feat
``` 
edit_first_ppi.sh ppi_first_template.fsf out_path subject fmriprep_dir
edit_first_ppi.sh /home1/09123/ofriend/analysis/temple/univ/ppi_first_template.fsf $FM/sub-temple016/univ/ppi/ temple016 $FM
run_first_ppi.sh fmriprep_dir subject
```
4. create second level .fsf file based on template, run with Feat
```
edit_second_ppi.sh 2nd_level_ppi_template.fsf out_path subject fmriprep_dir
run_second_ppis.sh fmriprep_dir subject
```
5. run third level ppi to average across subjects
```
run_third_feat.sh fmriprep_dir ppi
```

### whole hippocampus as seed, test for connectivity differences during boundary trials for early vs. later learning

1. use custom MNI hippocampus mask reverse-normalized into participant space, extract eigenvalue (first principle component) and save out
* need to create the hippocampal masks first (create_hip_masks.sh)
```
ppi_hip_new.sh data_dir subject task
ppi_hip_new.sh $CORR temple016 collector
```
2. create event and confound .txt files   
```
ppi_txt_behav.py data_dir file_type (motion/collector/both) subject out_dir
ppi_txt_behav.py $CORR both temple016 $FM/temple016/univ/ppi/
```
3. create first level .fsf file based on template, run with Feat
   * need path to corral for transformation files
``` 
edit_first_ppi.sh ppi_first_template.fsf out_path subject data_dir
edit_first_ppi.sh /home1/09123/ofriend/analysis/temple/univ/ppi_first_template.fsf (or ppi_first_inverse) $FM/sub-temple016/univ/ppi/ temple016 $FM
run_first_ppi.sh data_dir subject corral
run_first_ppi_inverse.sh $FM/ temple016 $CORR
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

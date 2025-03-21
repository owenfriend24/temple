# Pre-Processing:
Notes:
* When new fmriprep image works, re-run all preprocessing and output into one directory; copy to corral
* current preprocessing commands written below, still work in progress
* behavioral data in $WORK/temple/sourcebehav/sourcebehav, will need to fix double nesting
* slaunch is for multiple subjects at once, just use launch to run a normal job (slaunch for just one sub won't work unless you define subject variable in advance)

## 1. Source relevant profile
* activates virtual environment with relevant packages, sets some paths
```
cd $HOME/analysis/temple
source profile
```

## 2. Convert source DICOM data to BIDS formatting
* DICOM data comes off the scanner with slightly different file structures for the Prisma and the Skyra; different scripts and heuristic files needed depending on subject
* 53 and below = Skyra, 56+ = Prisma
* for subjects off the Prisma with CMRR functional runs terminated before finishing, will create a bold1 and bold2 image (bold1 is the one to use, bold2 is just the partial final/terminated TR)
* change heuristic file to "skyra_heuristic_anat_only.py" or "prisma_heuristic_anat_only.py" for only anatomical images if needed for ashs or to re-run freesurfer
* PRISMA
```
slaunch -J heudiconv "temple_heudiconv.sh {} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/temple_heuristic.py $SCRATCH/temple/new_prepro" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```
* SKYRA
```
slaunch -J heudiconv "skyra_heudiconv.sh {} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/skyra_heuristic.py $SCRATCH/temple/new_prepro" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```

## 3. Add fieldmap information to BIDS formatted raw data
* does not run on subjects that have already been run once it's been run on them once; assigns 'post_processed' to group in participants.tsv
* commented out some .json cleaning that Tony had included as those fields are not generated by these scan sequences

```
temple_bids_post.py $SCRATCH/temple/prisma_prepro
```
### 3.1 Quick process raw data
* to run heudiconv (prisma version) and post-processing for a newly collected subject (steps 2 and 3 above)
* also compresses raw data into tar.nii.gz (stored in sourcedata2) for Box backups
```
slaunch -J quick "quick_heu.sh {}" $subject -N 1 -n 1 -r 01:00:00 -p development
```
  
## 4. Run fmriprep (~ 8 hours)
* note - if re-running a previously processed subject, may need to change location of the input BIDS directory; otherwise, fmriprep will think this subject has already been run and won't re-process
* runs via Singularity/Apptainer image in $WORK; currently testing to make sure it works. Still points to Neal's freesurfer license I believe
* temple_fmriprep.sh includes command line that specifies some parameters including:
   * participant label - passed in with job launch; temple_### denotes raw data, temple### denotes data converted to BIDS (BIDS does not allow underscores)
   * std. dvars threshold = 1.5
   * framewise displacement threshold = 0.5
   * high-pass filter = 128
   * output spaces = MNI
   * omp-nthreads = 12
   * num_threads = 18
   * mem_mb = 60000
   * skip_bids_validation (make sure BIDS compliant when running heudiconv)
```
slaunch -J fmriprep “temple_fmriprep.sh $SCRATCH/temple/prepro_data {}" $BIDIDS -N 1 -n 1 -r 08:00:00 -p normal
```
* run_freesurfer.sh subject image_dir to re-run freesurfer if necessary
  * currently testing on temple_022 (only sub in which freesurfer didn't work correctly)
## 5. Post-process functional data
* runs the three sub-commands below (which can be run separately)
* skullstrips functional runs, creates transformation files between functional, anatomical, and MNI space, and smooths functional data
```
prep_func_data.sh freesurfer_dir fmriprep_dir subject
```

### 5.1. Create mask based on freesurfer parcellations and skullstrip functional runs (< 5 min. on dev node)
* fmriprep doesn't skullstrip the functional data, so we create a brainmask here using the freesurfer output and use it to skullstrip all functional runs
```
prep_func_data.py freesurfer_dir fmriprep_dir subject
```

## 5.2. Skullstrip anatomical image and create transform images/affine files for registration between functional, anatomical, and MNI space (~ 10 min. on dev. node)
* Now skullstrip the anatomical image and create all files necessary to transform between different spaces
```
mni_transforms.sh fmriprep_dir subject
```
## 5.3. Smooth functional data with 4mm kernel (~20 min.)
```
temple_smooth.sh fmriprep_dir freesurfer_dir subject task
temple_smooth.sh $FM $FS temple100 arrow
```



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
* PRISMA
```
slaunch -J heudiconv "temple_heudiconv.sh {} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/temple_heuristic.py $SCRATCH/temple/prepro_data" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```
* SKYRA
```
slaunch -J heudiconv "skyra_heudiconv.sh {} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/skyra_heuristic.py $SCRATCH/temple/prepro_data" $SUBIDS -N 1 -n 1 -r 00:30:00 -p development
```

## 3. Add fieldmap information to BIDS formatted raw data
* should not run on subjects that have already been run once it's been run on them once; assigns 'post_processed' to group in participants.tsv
* need to figure out whether the .json cleaning is necessary, test on group once group heudiconv goes through

```
temple_bids_post.py $SCRATCH/temple/prisma_prepro
```  
## 4. Run fmriprep (~ 8 hours)
* note - if re-running a previously processed subject, need to change location of the input BIDS directory; otherwise, fmriprep will think this subject has already been run and won't re-process
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

## 5. Create mask based on freesurfer parcellations and skullstrip functional runs (~ 10 min. on development node)
* fmriprep doesn't skullstrip the functional data, so we create a brainmask here using the freesurfer output and use it to skullstrip all functional runs
```
prep_func_data.sh freesurfer_dir fmriprep_dir subject task num_runs
```

## 6. Skullstrip anatomical image and create transform images/affine files for registration between functional, anatomical, and MNI space (~ 10 min. on dev. node; issue with final WarpImageMultiTransform call at end)
* Now skullstrip the anatomical image and create all files necessary to transform between different spaces
```
mni_transforms.sh fmriprep_dir subject
```
## 7. Smooth functional data with 4mm kernel (~20 min.)
* set up to smooth four runs right now, will need to edit for arrow
* also will want to incorporate some of the 'clean_scratch' code here to make sure the files we're working with stay in BIDS format
```
temple_smooth.sh fmriprep_dir freesurfer_dir subject task
```



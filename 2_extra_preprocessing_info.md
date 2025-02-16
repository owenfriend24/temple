## Remote desktop via TACC
```
sbatch /share/doc/slurm/job.dcv
touch dcvserver.out ; tail -f dcvserver.out
```
* job needs to be running before touch command works
* to quit job:
```
  scancel JOBID
```
* use '&' to open software within session
```
fsleyes &
```
* Ctrl + c in terminal to get back to normal TACC after running job commands

## Plotting motion using fmriprep confound files
* fmriprep outputs some but I don't like their formatting, this script gives better ones including reports of mean, sd, and %/# over threshold for FD and DVARS
* pull motion files to local machine:
  ```
  cd /Users/owenfriend/Documents/temple_local/motion_files
  ./pull_behav.sh ofriend@ls6.tacc.utexas.edu:/scratch/09123/ofriend/temple/prisma_prepro/derivatives/fmriprep ./ temple060
  ```
* plot motion by run for subject
  ```
  cd /Users/owenfriend/Documents/temple_local/motion_files
  python plot_motion.py
  ```

## Working between TACC and local machine
* It's annoying to re-clone github repo in TACC every time I make a change, so I'm making changes on local machine and using CyberDuck to upload
*   need to chmod 755 on new .py and .sh scripts to let me run them
* To pull behavioral data from cluster onto local machine (e.g., to check motion):
*   From local machine terminal:
```
cd /Users/owenfriend/Documents/temple_local/analysis
./temple_behav_data.sh ofriend@ls6.tacc.utexas.edu:/scratch/09123/ofriend/temple/rawdata2/derivatives/fmriprep-23.0.2 /Users/owenfriend/Documents/temple_local/motion_files
```

## using idev
* should check on how often i should be using, need to use either idev or jobs for registration via ants

## betaseries-bids fields
* example call, below each bulleted field is working example (not sure if all work)
```
betaseries-bids [OPTIONS] data_dir fmriprep_dir out_dir subject task run space mask_name mask_file events_field
```
* data_dir – path to BIDS-compliant dataset with task events
  `$SCRATCH/temple/rawdata2`
*	fmriprep_dir
  `$SCRATCH/temple/rawdata2/derivatives/fmriprep-20.2.1/fmriprep/`
*	out_dir
  `$SCRATCH/temple/output`
*	subject
  `temple019`
*	task
  `arrow`
*	run
  `1`
*	space
 `MNI152NLin2009cAsym`
*	mask_name
  `GM`
*	mask_file
  `$SCRATCH/temple/rawdata/derivatives/fmriprep-20.2.1/fmriprep/sub-temple019/anat/sub-temple019_space-MNI152NLin2009cAsym_label-GM_probseg.nii.gz`
*	events_field – column of events file to use to indicate individual explanatory variable
  `object`

* [OPTIONS]
--high-pass FLOAT (highpass filter in Hz)
--smooth FLOAT (smoothing kernel FWHM)
--confound-measures TEXT (colon-separated list of confound measures (see below)


## Confound list for betaseries-bids script
```
csf:csf_derivative1:white_matter:white_matter_derivative1:trans_x:trans_x_derivative1:trans_y:trans_y_derivative1:trans_z:trans_z_derivative1:rot_x:rot_x_derivative1:rot_y:rot_y_derivative1:rot_z:rot_z_derivative1
```

## Different data types/formats
1. DICOM (Digital Imaging and Communications in Medicine)
*  File format when images are pulled off of scanner
*  Contains:
    * Image data: pixel data of images representing actual visual content such as grayscale or color values that make up the images in binary format
    * Metadata: information about image and its acquisition (i.e. patient info., scan type, orientation, etc.)
    *	Extension = .dcm
2. NIfTI (Neuroimaging Informatics Technology Initiative)
*	Stores MRI or fMRI data using three-dimensional arrays of image intensities representing voxel values of brain volume
*	File structure:
    * Header containing metadata about image
    * Actual image data storing voxel intensity values
*	Supports extensions allowing for additional info to be stored alongside image data (i.e. ROI’s, anatomical atlases, etc.)
*	Extension = .nii or .nii.gz when compressed (.gz refers to Gzip file compression)
    *	Pre-processed images stores as .nii.gz files
3. BIDS (Brain Imaging Data Structure)
*	Folder structure/hierarchy
    *	Top-level directory contains entire dataset with subdirectories representing different subjects/sessions/runs
    * File naming convention: each file contains specific elements such as sub ID, session, modality, task info.
    * Metadata: typically stored in sidecar JSON files accompanying imaging files containing key-value pairs describing acquisition parameters, processing steps, and other important info about imaging data
        * Essentially arrays/dictionaries with values for important parameters (e.g. SUBID: 001)
    * Also allows for inclusion of derived data (e.g. processed or analyzed data)
* helpful renaming function for local:
  ```
  for file in temple055*; do
  mv "$file" "$(echo $file | sed 's/temple055/temple056a/')"
  done
  ```
* running heudiconv without a heuristic to see scan names:
  ```
  heudiconv -d './fix_56/{subject}/*' -s 'sub-temple056a' -f convertall -c none -o ./fix_56/output
  ```
  ```
  heudiconv -d '../wr_local/{subject}/*' -s 'wr_000' -f convertall -c none -o ./output   
  ```
### change file end to match bids specification after skullstripping and smoothing ###
```
find . -type f -name '*bold_ss_4mm.nii.gz' -exec bash -c 'mv "$1" "${1/bold_ss_4mm/bold}"' _ {} \;
```

### setting up singularity image on tacc
https://www.nipreps.org/apps/singularity/
https://containers-at-tacc.readthedocs.io/en/latest/singularity/01.singularity_basics.html

```
idev
module load tacc-apptainer
apptainer pull docker://nipreps/fmriprep:23.1.3
```

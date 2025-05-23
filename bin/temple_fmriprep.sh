#!/bin/bash
#
# Run fMRIprep for one subject.

if [[ $# -lt 2 ]]; then
    echo "Usage: temple_fmriprep.sh bids_dir subject"
    exit 1
fi

BIDS_DIR=$1
subject=$2

echo " Starting at $(date)"
start=$(date +%s)

DERIVS_DIR=derivatives/fmriprep

# Prepare some writeable bind-mount points.
TEMPLATEFLOW_HOST_HOME=${WORK}/.cache/templateflow
FMRIPREP_HOST_CACHE=${WORK}/.cache/fmriprep
mkdir -p "${TEMPLATEFLOW_HOST_HOME}"
mkdir -p "${FMRIPREP_HOST_CACHE}"

# Prepare derivatives folder
mkdir -p "${BIDS_DIR}/${DERIVS_DIR}"

# Make sure FS_LICENSE is defined in the container.
# export SINGULARITYENV_FS_LICENSE=${HOME}/.freesurfer.txt
export SINGULARITYENV_FS_LICENSE=/work/03206/mortonne/software/apps/freesurfer-6.0.0/license.txt

# Designate a templateflow bind-mount point
export SINGULARITYENV_TEMPLATEFLOW_HOME=/templateflow

# Load singularity module (can only be loaded on compute nodes)
module load tacc-apptainer
WORKDIR=${SCRATCH}/fmriprep/${SLURM_JOB_ID}.${subject}
mkdir -p "${WORKDIR}"

# Set singularity command and mount points
SINGULARITY_CMD="apptainer run \
    --cleanenv \
    -B ${BIDS_DIR}:/data \
    -B ${TEMPLATEFLOW_HOST_HOME}:${SINGULARITYENV_TEMPLATEFLOW_HOME} \
    -B ${WORKDIR}:/workdir \
    /work/09123/ofriend/ls6/fmriprep_23.1.3.sif"

# Compose the command line
cmd="${SINGULARITY_CMD} \
    ${BIDS_DIR} \
    ${BIDS_DIR}/${DERIVS_DIR} \
    participant \
    --participant-label ${subject} \
    -w /workdir/ \
    --fd-spike-threshold 0.5 \
    --dvars-spike-threshold 1.5 \
    --output-spaces fsaverage:den-164k anat:res-native \
    -v \
    --omp-nthreads 12 \
    --nthreads 18 \
    --mem_mb 60000 \
    --skip_bids_validation
    "

# # Compose the command line
# cmd="${SINGULARITY_CMD} \
#     /data/rawdata \
#     /data/${DERIVS_DIR} \
#     participant \
#     --participant-label ${subject} \
#     -w /workdir/ \
#     --fd-spike-threshold 0.5 \
#     --dvars-spike-threshold 1.5 \
#     --output-spaces MNI152NLin2009cAsym:res-native fsaverage:den-164k anat:res-native \
#     -v \
#     --omp-nthreads 12 \
#     --nthreads 18 \
#     --mem_mb 60000
#     "

# Setup done, run the command
log_dir=${BATCHDIR}/fmriprep/${SLURM_JOB_ID}
mkdir -p "${log_dir}"
echo "Running task ${SLURM_JOB_ID}-${subject}"
echo "Commandline: ${cmd}"
eval $cmd 1> "$log_dir/sub-${subject}.out" 2> "${log_dir}/sub-${subject}.err"
exitcode=$?

# Output results to a table
echo -e "sub-${subject}\t${exitcode}" >> "${log_dir}/results.tsv"
echo "Finished job ${SLURM_JOB_ID}-${subject} with exit code $exitcode"

echo " "
echo " Job complete at $(date)"
echo " "
finish=$(date +%s)
printf "Job duration: %02d:%02d:%02d (%d s)
" $(((finish-start)/3600)) $(((finish-start)%3600/60)) $(((finish-start)%60)) $((finish-start))


exit "$exitcode"

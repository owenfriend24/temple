#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "batch_uni_first.sh $FM SUB"
    exit 1
fi

fmriprep_dir=$1
sub=$2

sub_dir=${fmriprep_dir}/ppi/sub-${sub}/
corr=/corral-repl/utexas/prestonlab/temple

source $HOME/analysis/temple/profile

# create behavioral files for both analyses
ppi_hip_new.sh ${fmriprep_dir}/ppi/ ${sub} collector
ppi_txt_behav.py ${corr} both ${sub} ${sub_dir}/ppi/

# rename any previous analyses (should generally go in and delete to save space)
for dir in ppi ppi_inverse; do
    base="${fmriprep_dir}/ppi/sub-${sub}/${dir}"
    [ -d "${base}/2nd_level_out.gfeat" ] && mv "${base}/2nd_level_out.gfeat" "${base}/old_2nd_level_out.gfeat"
    for run in {1..4}; do
        [ -d "${base}/out_run${run}.feat" ] && mv "${base}/out_run${run}.feat" "${base}/old_out_run${run}.feat"
    done
done

# create .fsf files for increased connectivity at triplet boundaries
edit_first_ppi.sh /home1/09123/ofriend/analysis/temple/univ/ppi_first_template.fsf ${sub_dir}/ppi/ ${sub} ${corr}
edit_second_ppi.sh 2nd_level_ppi_template.fsf ${sub_dir}/ppi/ ${sub} ppi
run_second_ppis.sh ${fmriprep_dir}/ppi/ ${sub} ppi

# create .fsf files for DECREASED connectivity at triplet boundaries
edit_first_ppi.sh /home1/09123/ofriend/analysis/temple/univ/ppi_first_inverse.fsf ${sub_dir}/ppi_inverse/ ${sub} ${corr}
edit_second_ppi.sh 2nd_level_ppi_inverse.fsf ${sub_dir}/ppi_inverse/ ${sub} inverse
run_second_ppis.sh ${fmriprep_dir}/ppi/ ${sub} inverse



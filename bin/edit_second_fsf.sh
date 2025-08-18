#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: edit_second_fsf.sh subject type (boundary, ppi, ppi_inverse)"
    exit 1
fi

subject=$1
type=$2
roi=$3

excl_tag=""

if [ "$subject" == "temple999" ]; then #114
    excl_tag="_drop1"
#elif [ "$subject" == "temple107" ] | [ "$subject" == "temple060" ]; then
#    excl_tag="_drop2"
#elif [ "$subject" == "temple064" ]; then
#    excl_tag="_drop3"
#elif [ "$subject" == "temple130" ]; then
#    excl_tag="_drop1and4"
else
    excl_tag="_allruns"
fi

if [ "$type" == "boundary" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary${excl_tag}.fsf"
    out_path=/corral-repl/utexas/prestonlab/temple/sub-${subject}/univ/
elif [ "$type" == "ppi" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_ppi${excl_tag}.fsf"
    out_path=/corral-repl/utexas/prestonlab/temple/sub-${subject}/univ/ppi/
elif [ "$type" == "ppi_inverse" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_ppi_inverse${excl_tag}.fsf"
    out_path=/corral-repl/utexas/prestonlab/temple/sub-${subject}/univ/ppi_inverse
fi

python /home1/09123/ofriend/analysis/temple/bin/edit_first_fsf.py $template $out_path $subject 5 222 222 $type $roi


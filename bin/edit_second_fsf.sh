#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: edit_second_fsf.sh subject type (boundary, ppi, ppi_inverse)"
    exit 1
fi

subject=$1
type=$2
roi=$3

excl_tag=""

if [ "$subject" == "temple114" ]; then
    excl_tag="_drop1"
elif [ "$subject" == "temple107" ]; then
    excl_tag="_drop2"
elif [ "$subject" == "temple064" ]; then
    excl_tag="_drop3"
else
    excl_tag="_allruns"
fi

if [ "$type" == "boundary" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary${excl_tag}.fsf"
elif [ "$type" == "ppi" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_ppi${excl_tag}_${roi}.fsf"
elif [ "$type" == "ppi_inverse" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_ppi_inverse${excl_tag}_${roi}.fsf"
fi


#
python edit_first_fsf.py $template /corral-repl/utexas/prestonlab/temple/${subject}/univ/ $subject 5 222 222 $roi
#!/usr/bin/env python
#
# edit template .fsf file for other subjects and runs

from pathlib import Path
import os
import argparse


def edit_fsf_file(template, out_path, sub, run, num_vols, num_voxs, analysis_type):
    # Read the content of the original .fsf file
    with open(template, 'r') as f:
        fsf_content = f.read()

        
    # Replace 'sub-temple024' with whatever subject we're modeling
    fsf_content = fsf_content.replace('sub-temple024', f'sub-{sub}')

    
    
    if num_vols == '222':
        if analysis_type == 'inverse':
            out_file = f'{out_path}/sub-{sub}-ppi_inverse_second_level.fsf'
            fsf_content = fsf_content.replace('/ppi/out_run', f'/ppi_inverse/inverse_out_run')
            fsf_content = fsf_content.replace('/ppi/2ndlevelppi_HIP', f'/ppi_inverse/2ndlevelppi_inverse_HIP')
        else:
            out_file = f'{out_path}/sub-{sub}-ppi_second_level.fsf'

    else:
        # Replace 'run-01' with whatever run we're modeling
        fsf_content = fsf_content.replace('run-01', f'run-0{run}')
        fsf_content = fsf_content.replace('run-1', f'run-{run}')
    
        fsf_content = fsf_content.replace('NUM_VOLS', num_vols)
        fsf_content = fsf_content.replace('NUM_VOXELS', num_voxs)

        if 'inverse' in template:

            fsf_content = fsf_content.replace('OUT_RUN', f'inverse_out_run{run}')
            out_file = f'{out_path}/sub-{sub}-ppi_inverse_first_run-0{run}.fsf'
        else:
            fsf_content = fsf_content.replace('OUT_RUN', f'out_run{run}')
            out_file = f'{out_path}/sub-{sub}-ppi_first_run-0{run}.fsf'
        
    # Write the modified content to the new .fsf file
    with open(out_file, 'w') as f:
        f.write(fsf_content)

        
def main(template, out_path, sub, run_num, num_vols, num_voxs, analysis_type):
    edit_fsf_file(template, out_path, sub, run_num, num_vols, num_voxs, analysis_type)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("template", help="path to template .fsf file")
    parser.add_argument("out_path", help="output dir (e.g. .../sub-temple001/univ")
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("run_num", help="run to generate .fsf file for")
    parser.add_argument("num_vols", help="number of functional volumes")
    parser.add_argument("num_voxs", help="number of voxels")
    parser.add_argument("analysis_type", type=str, choices=["ppi", "inverse"], default="ppi",
                        help="ppi or inverse")
    args = parser.parse_args()
    main(args.template, args.out_path, args.sub, args.run_num, args.num_vols, args.num_voxs, args.analysis_type)

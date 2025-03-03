"""Heuristic file for use with heudiconv."""
import pdb


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # define file path format for BIDS
    key_T1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    key_T2w = create_key('sub-{subject}/anat/sub-{subject}_T2w')

    # sort scans into file types
    info = {
        key_T1w: [],
        key_T2w: []
    }

    n_T2 = 0
    n_T1 = 0
    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:
        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        * series_files
        """
        if s.series_description == 'mprage':
            # T1 highres anatomical
            n_T1 += 1
            print(f'INSIDE::{s.series_id}::{n_T1}::{s.series_files}')
            info[key_T1w].append(s.series_id)
            

        elif 'T2' in s.series_description:
            if 'FLAIR' in s.series_description:
                print(f'INSIDE::{s.series_id}::{n_T2}::{s.series_files}')
            else:
                # T2 coronal anatomical
                n_T2 += 1

                # add scan if included
                print(f'INSIDE::{s.series_id}::{n_T2}::{s.series_files}')
                info[key_T2w].append(s.series_id)


    return info

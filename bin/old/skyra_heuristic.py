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
    # find the functional runs that were completed
    include_sbref = []
    include_bold = []
    for i, s in enumerate(seqinfo):
        if s.series_description == 'arrow' or s.series_description == 'collector' or s.series_description == 'movie':
	    # should be more than 15 TRs (estimate for run restart)
            if s.dim4 > 20:
                print('\n\n\n')
                # include this scan and the one before, which is the SBRef
                include_sbref.append(seqinfo[i - 1].series_id)
                include_bold.append(s.series_id)

    # define file path format for BIDS
    key_T1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    key_T2w = create_key('sub-{subject}/anat/sub-{subject}_T2w')
    key_magnitude = create_key('sub-{subject}/fmap/sub-{subject}_run-{item:02d}_magnitude')
    key_phasediff = create_key('sub-{subject}/fmap/sub-{subject}_run-{item:02d}_phasediff')
    key_fmap = create_key('sub-{subject}/fmap/sub-{subject}_run-{item:02d}_fmap')
    key_arrow = create_key('sub-{subject}/func/sub-{subject}_task-arrow_run-{item:02d}_bold')
    key_arrow_sbref = create_key('sub-{subject}/func/sub-{subject}_task-arrow_run-{item:02d}_sbref')
    key_collector = create_key('sub-{subject}/func/sub-{subject}_task-collector_run-{item:02d}_bold')
    key_collector_sbref = create_key('sub-{subject}/func/sub-{subject}_task-collector_run-{item:02d}_sbref')
    key_movie = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_bold')
    key_movie_sbref = create_key('sub-{subject}/func/sub-{subject}_task-movie_run-{item:02d}_sbref')

    # sort scans into file types
    info = {
        key_T1w: [],
        key_T2w: [],
        key_magnitude: [],
        key_phasediff: [],
        key_fmap: [],
        key_arrow_sbref: [],
        key_arrow: [],
        key_collector_sbref: [],
        key_collector: [],
        key_movie_sbref: [],
        key_movie:[]
    }
    n_fieldmap = 0
    n_phase = 0
    n_magnitude = 0
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

        elif s.series_description == 'fieldmap':
            # fieldmaps to estimate susceptibility distortion
            n_fieldmap += 1

            # add to either magnitude or phase difference image set
            #pdb.set_trace()
            #print(f'OUTSIDE::{s.series_id}::{n_phase}::{n_fieldmap}::{s.series_files}')
            if s.series_files > 130:
            # if n_fieldmap % 2 == 1:
                n_magnitude += 1
                if n_magnitude % 2 == 1:
                    print(f'INSIDE::{s.series_id}::{n_magnitude}::{n_fieldmap}::{s.series_files}')
                    info[key_magnitude].append(s.series_id)
                else:
                    continue
            else:
                n_phase += 1
                print(f'INSIDE::{s.series_id}::{n_phase}:{n_fieldmap}:{s.series_files}')
                info[key_phasediff].append(s.series_id)

        # single-band image from a functional scan
        elif s.series_description == 'arrow_SBRef':
            if s.series_id in include_sbref:
                info[key_arrow_sbref].append(s.series_id)

        elif s.series_description == 'collector_SBRef':
            if s.series_id in include_sbref:
                info[key_collector_sbref].append(s.series_id)

        elif s.series_description == 'movie_SBRef':
            if s.series_id in include_sbref:    
                info[key_movie_sbref].append(s.series_id)

        # functional scans
        elif s.series_description == 'arrow':
            if s.series_id in include_bold:
                info[key_arrow].append(s.series_id)

        elif s.series_description == 'collector': 
            if s.series_id in include_bold:
                info[key_collector].append(s.series_id)

        elif s.series_description == 'movie':
            if s.series_id in include_bold:
                info[key_movie].append(s.series_id)
    return info

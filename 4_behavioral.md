## 1. Convert behavioral data into BIDS format within BIDS formatted subject directories
* arrow and collector go into func directory, remember goes to beh
* can either run for a single subject or for all subject's at once
```
events_bids.py $WORK/temple/sourcebehav/ $FM 19
events_bids.py $WORK/temple/sourcebehav/ $FM ALL
```
 * to run all at once, make sure subject number listed in tasks.py to run
```
vim $WORK/tempenv/lib/python3.9/site-packages/temple/tasks.py
```
 * resulting output needs additional formatting to denote triads and positions
 * triads are determined based on remember which labels each item 1-12 based on triad and position
   * same item values are used in arrow after runnning fix_arrow.py
   * collector are denoted by triad (1-4) and position (1-3) which correspond to same item values
     * e.g., item 9 in arrow/remember can also be denoted as triad 3 item 3

### 2. Fix collector task output
* adds and fixes triad (1-4) and position (1-3) values
```
fix_collector.py fmriprep_dir subject
```

### 3 Fix arrow task output 
* adds/fixes triad (1-4) and position (1-3) values
* outputs events files directly back into func directory, while also creating an 'orig_events' directory within func and copying original events files
```
fix_arrow.py fmriprep_dir subject
```
### 4. Clean and save out memory test data
* optional flags to pull aggregated data by subject (i.e., one accuracy score per subject) or by triad (i.e., four values per subject)
```
clean_remember.py --by_subject --by_triad AGGREGATE $CORR
clean_remember.py temple016 $CORR
clean_remember.py ALL $CORR
```

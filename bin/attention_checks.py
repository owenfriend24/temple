#!/usr/bin/env python
#
# fix arrow runs to correctly reflect triads and objects

from pathlib import Path
import pandas as pd
import numpy as np
import argparse


def main(corr, sub):
    out_file = Path(corr) / "beh" / "attention_checks_by_run_new.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if out_file.exists():
        master = pd.read_csv(out_file)
    else:
        master = pd.DataFrame(columns=['subject', 'task', 'run', 'acc', 'rt'])

    func_dir = Path(corr) / f'sub-{sub}' / 'func'

    for arr_run in range(1, 7):
        data = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-0{arr_run}_events.tsv')
        acc = np.mean(data['acc'])
        rt = np.mean(data['response_time'])
        master.loc[len(master)] = [sub, 'arrow', arr_run, acc, rt]

    for coll_run in range(1, 5):
        data = pd.read_table(func_dir / f'sub-{sub}_task-collector_run-0{coll_run}_events.tsv')
        # 2 where no attention check, 1 where there is
        resp_data = data[data['odd'] == 1]
        acc = np.mean(resp_data['acc'])
        rt = np.mean(resp_data['response_time'])
        master.loc[len(master)] = [sub, 'collector', coll_run, acc, rt]

    master.to_csv(out_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("corr", help="corral directory")
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.corr, args.sub)

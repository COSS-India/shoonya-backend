import csv

import pandas as pd


def dump_to_local_fs(sentences_list: list[str]) -> None:
    df = pd.DataFrame(sentences_list, columns=['garo_raw'])
    df.to_csv('garo_dump.csv', index=False, quoting=csv.QUOTE_ALL)

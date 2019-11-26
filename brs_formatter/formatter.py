#!/usr/bin/env python3

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='add brs file path to beautified')
args = parser.parse_args()


def parser():
    if isinstance(args.file, str):
        file_path = Path(args.file)



if __name__ == '__main__':
    parser()
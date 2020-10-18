import argparse
import json
import sys

from ctrunner.parser import convert_list, convert_election_data


def register(subparsers: argparse.ArgumentParser):
    parse_parser = subparsers.add_parser("parse")
    parse_parser.add_argument(
        "-d", "--data-type", choices=["election-data", "election-list"]
    )


def main(args):
    if args.data_type == "election-list":
        input_str = sys.stdin.read()
        input_obj = json.loads(input_str)
        print(convert_list(input_obj))
    if args.data_type == "election-data":
        input_str = sys.stdin.read()
        input_obj = json.loads(input_str)
        print(convert_election_data(input_obj))

import argparse
import json

from ctrunner.downloader import (
    get_election_list,
    get_data_for_all_elections,
    get_data_for_election,
)


def register(subparsers: argparse.ArgumentParser):
    download_parser = subparsers.add_parser("download")
    download_parser.add_argument("-a", "--all", action="store_true")
    download_parser.add_argument("-l", "--election-list", action="store_true")
    download_parser.add_argument("-e", "--election", type=str, metavar="ELECTION_ID")


def main(args):
    if args.all:
        ret = get_data_for_all_elections()
    elif args.election_list:
        ret = get_election_list()
    elif args.election:
        ret = get_data_for_election(args.election)
    print(json.dumps(ret, indent=2))

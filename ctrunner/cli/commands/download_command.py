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
    """Download requested data from API

    Download either a list of elections or election data for a specific
    election. Prints data as JSON to stdout.
    """
    if args.all:
        ret = get_data_for_all_elections()
    elif args.election_list:
        ret = get_election_list()
    elif args.election:
        ret = get_data_for_election(args.election)
    print(json.dumps(ret, indent=2))

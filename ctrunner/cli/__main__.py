import argparse
import json

import sys

from ctrunner.downloader import (
    get_election_list,
    get_data_for_election,
    get_data_for_all_elections,
)
from ctrunner.parser import convert_list, convert_election_data

from .commands import archive_command, parse_command, download_command


def main():
    parser = argparse.ArgumentParser("ctrunner - Connecticut election data runner")

    subparsers = parser.add_subparsers(help="commands", dest="command")

    archive_command.register(subparsers)
    parse_command.register(subparsers)
    download_command.register(subparsers)

    args = parser.parse_args()

    if args.command == "archive":
        archive_command.main(args)
    elif args.command == "parse":
        parse_command.main(args)
    elif args.command == "download":
        download_command.main(args)


if __name__ == "__main__":
    main()
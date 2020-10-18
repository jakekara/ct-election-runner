import argparse
import json
import os
from ctrunner.downloader import get_data_for_election
from ctrunner.parser import convert_election_data


def register(subparsers: argparse.ArgumentParser):
    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("-s", "--dest", type=str, help="Archive directory")
    archive_parser.add_argument("-e", "--election", type=str, metavar="ELECTION_ID")


def main(args):
    election_id = args.election
    if not os.path.exists(args.dest):
        os.makedirs(args.dest)
    election = get_data_for_election(election_id)

    election_dir = os.path.join(args.dest, election_id)
    if not os.path.exists(election_dir):
        os.makedirs(election_dir)

    version_dir = os.path.join(election_dir, str(election["version"]))
    if not os.path.exists(version_dir):
        os.makedirs(version_dir)

    csv = convert_election_data(election)

    open(os.path.join(version_dir, "raw.json"), "w").write(
        json.dumps(election, indent=2)
    )
    open(os.path.join(version_dir, "results.csv"), "w").write(csv)

    # write a copy to the election dir as "latest"
    open(os.path.join(election_dir, "raw-latest.json"), "w").write(
        json.dumps(election, indent=2)
    )
    open(os.path.join(election_dir, "results.csv"), "w").write(csv)

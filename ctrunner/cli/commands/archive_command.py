"""Functionality for the archive subcommand"""

import argparse
import json
import os
from ctrunner.downloader import get_data_for_election, get_election_list
from ctrunner.parser import convert_election_data


def register(subparsers: argparse.ArgumentParser):
    archive_parser = subparsers.add_parser("archive")
    archive_parser.add_argument("-s", "--dest", type=str, help="Archive directory")
    archive_parser.add_argument("-e", "--election", type=str, metavar="ELECTION_ID", default="ALL")

def archive_an_election(dest, election_id):

    """Archive an election

    Download data for a given election and store in a given folder. The folder
    structure is: {destination folder}/ {election id}/ raw.json - latest raw
    file from API results.csv - summary of statewide and town-level results
    {version no}/ raw.json - latest raw file from API results.csv - summary of
    statewide and town-level results

    The election folder stores the latest raw.json and results.csv, and the
    version subfolders are used to keep track of past versions of the data.

    """
    election_id = election_id
    if not os.path.exists(dest):
        os.makedirs(dest)

    election = get_data_for_election(election_id)

    election_dir = os.path.join(dest, election_id)
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
    open(os.path.join(election_dir, "raw.json"), "w").write(
        json.dumps(election, indent=2)
    )
    open(os.path.join(election_dir, "results.csv"), "w").write(csv)

def main(args):

    election_id = args.election
    dest = args.dest

    if election_id != "ALL":
        archive_an_election(dest, election_id)

    if election_id == "ALL":
        election_list = get_election_list()
        
        open(os.path.join(dest, "index.json"),"w").write(json.dumps(election_list, indent=2))

        for election in election_list:
            print(f"Fetching data for election {election['ID']}: {election['Name']}")
            archive_an_election(dest, election["ID"])




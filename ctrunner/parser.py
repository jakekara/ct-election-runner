"""Parse raw data from API into CSV strings
"""

import csv
from io import StringIO

from .parse_tools import unwrap_object


def convert_list(election_list: object):
    """
    Convert election list data to a csv string
    """

    f = StringIO()
    fieldnames = ["ID", "Name", "DefaultElection"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for e in election_list:
        writer.writerow(e)
    return f.getvalue()


def get_town_name(lookup_data: object, town_id: str):
    """Get the name of a town"""
    return lookup_data["townIds"][town_id]


def get_office_name(lookup_data: object, office_id: str):
    """Get the name of an office"""
    office_list = list(map(unwrap_object, lookup_data["officeList"]))

    office_match = list(filter(lambda x: x["ID"] == office_id, office_list))

    # TODO - There can be multitple listings of offices with different districts
    # but the office name should be the same. This is fine for quick demo
    # assert len(office_match) == 1

    return office_match[0]["NM"]


def get_candidate_name(lookup_data: object, candidate_id: str):
    """Get the name of a given candidate"""
    return lookup_data["candidateIds"][candidate_id]["NM"]


def get_candidate_party(lookup_data: object, candidate_id: str, field: str = "CD"):
    """Get the party of a candidate.

    Set field to 'NM' to get the display name of the party"""
    party_id = lookup_data["candidateIds"][candidate_id]["P"]
    return lookup_data["partyIds"][party_id][field]


def convert_election_data(data):
    """
    Convert election data to a csv string

    return list<{
        office: string
        locale: {town name} | "state"
        candidate: string
        party: string,
        voteCount: number
        votePercent: string
    }>
    """

    election_data = data["ElectionData"]
    lookup_data = data["LookupData"]

    rows = []

    # TODO - This is really gross nested for loop, but it was the easiest way to
    # do this quickly.
    for town_id in ["state"] + list(lookup_data["townIds"].keys()):
        if town_id == "state":
            town_name = "statewide"
            votes = election_data["stateVotes"]
        else:
            town_name = get_town_name(lookup_data, town_id)
            try:
                votes = election_data["townVotes"][town_id]
            except:
                # print(f"No election data found for {town_name}. Skipping")
                continue

        town_base_row = {"town": town_name}
        for office_id in votes:
            office_base_row = dict(town_base_row)
            office_base_row["office"] = get_office_name(lookup_data, office_id)
            for result in votes[office_id]:
                candidate_row = dict(office_base_row)
                candidate_id = list(result.keys())[0]
                try:
                    candidate_row["candidate"] = get_candidate_name(
                        lookup_data, candidate_id
                    )
                    candidate_row["party"] = get_candidate_party(
                        lookup_data, candidate_id
                    )
                    candidate_row["votes"] = result[candidate_id]["V"]
                    candidate_row["vote_percent"] = result[candidate_id]["TO"]
                    rows.append(candidate_row)
                except Exception as e:
                    pass

    f = StringIO()
    fieldnames = ["office", "town", "candidate", "party", "votes", "vote_percent"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for result in rows:
        writer.writerow(result)
    ret = f.getvalue()

    return ret

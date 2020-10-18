import csv
from io import StringIO
import json
import sys


def convert_list(election_list):
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


def unwrap_object(obj, force_key=None):
    """
    'Unwrap' this weird format a lot of this data is in, where there's
    an object containing one key, with a value that is the actual object
    you want. The key is usually the same as an ID field in the inner object
    """
    keys = obj.keys()
    assert len(list(keys)) == 1, "Wrapped object must only have one key"
    obj_key = list(keys)[0]

    inner_obj = obj[obj_key]
    if inner_obj["ID"] == obj_key:
        return inner_obj
    else:
        if force_key:
            inner_obj[force_key] = obj_key
            return inner_obj
        raise Exception("Inner object has no ID field:\n" + json.dumps(obj, indent=2))


def get_town_name(lookup_data, town_id):
    return lookup_data["townIds"][town_id]


def get_office_name(lookup_data, office_id):
    office_list = list(map(unwrap_object, lookup_data["officeList"]))

    office_match = list(filter(lambda x: x["ID"] == office_id, office_list))

    # TODO - There can be multitple listings of offices with different districts
    # but the office name should be the same. This is fine for quick demo
    # assert len(office_match) == 1

    return office_match[0]["NM"]
    

def get_candidate_name(lookup_data, candidate_id):
    return lookup_data["candidateIds"][candidate_id]["NM"]


def get_candidate_party(lookup_data, candidate_id, field="CD"):
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

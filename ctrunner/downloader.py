"""
ctrunner.py - Pull  data on from CT elections system
author: jake kara <jake@jakekara.com>
"""

from .download_tools import get_json


def get_election_list():
    """
    Get a list of elections
    """

    return get_json("https://ctemspublic.pcctg.net/ng-app/data/Elections.json")


def get_version(election_id: int):
    """
    Get the latest version number of an election
    """

    version_dict = get_json(
        f"https://ctemspublic.pcctg.net/ng-app/data/election/{election_id}/Version.json"
    )
    return version_dict["Version"]


def get_electiondata(election_id: int, version_id: int = None):
    """
    Get Electiondata.json for a given election id
    """

    if version_id is None:
        version_id = get_version(election_id)
    return get_json(
        f"https://ctemspublic.pcctg.net/ng-app/data/election/{election_id}/{version_id}/Electiondata.json"
    )


def get_lookupdata(election_id: int, version_id: int = None):
    """
    Get Lookupdata.json for a given election_id
    """

    if version_id is None:
        version_id = get_version(election_id)
    return get_json(
        f"https://ctemspublic.pcctg.net/ng-app/data/election/{election_id}/{version_id}/Lookupdata.json"
    )


def get_data_for_election(election_id):
    version = get_version(election_id)
    electiondata = get_electiondata(election_id, version_id=version)
    lookupdata = get_lookupdata(election_id, version_id=version)
    return {"version": version, "ElectionData": electiondata, "LookupData": lookupdata}


def get_data_for_all_elections():

    ret = {"election_list": get_election_list(), "elections": {}}

    for e in ret["election_list"]:
        ret["elections"][e["ID"]] = {"data": get_data_for_election(e["ID"])}

    return ret

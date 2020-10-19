"""Get raw JSON files from election night reporting system API
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
    """
    Helper function to get the version, election data and lookup data in a
    single function call.
    """
    version = get_version(election_id)
    electiondata = get_electiondata(election_id, version_id=version)
    lookupdata = get_lookupdata(election_id, version_id=version)
    return {"version": version, "ElectionData": electiondata, "LookupData": lookupdata}


def get_data_for_all_elections():
    """
    Helper function to call get_data_for_election for all elections. This should
    not be used too often because old elections are never changed.
    """
    ret = {"election_list": get_election_list(), "elections": {}}

    for e in ret["election_list"]:
        ret["elections"][e["ID"]] = {"data": get_data_for_election(e["ID"])}

    return ret

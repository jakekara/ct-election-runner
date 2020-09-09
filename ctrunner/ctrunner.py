"""
ctrunner.py - a module for pulling data on CT elections
author: jake kara <jake@jakekara.com>
"""

from .download_tools import get_json

def get_elections():
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

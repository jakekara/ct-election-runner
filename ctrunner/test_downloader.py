from ctrunner import downloader
from random import sample, choice


def test_can_get_elections_list():
    elections = downloader.get_election_list()
    assert isinstance(elections, list)
    assert len(elections) > 4


def test_can_get_version():
    elections = downloader.get_election_list()
    for election in sample(elections, 3):
        version = downloader.get_version(election["ID"])
        assert isinstance(version, int)


def test_can_get_electiondata():
    elections = downloader.get_election_list()
    election = choice(elections)
    election_id = election["ID"]
    version = downloader.get_version(election_id)
    electiondata = downloader.get_electiondata(election_id, version)
    assert isinstance(electiondata, dict)


def test_can_get_electiondata_without_version():
    elections = downloader.get_election_list()
    election = choice(elections)
    election_id = election["ID"]
    electiondata = downloader.get_electiondata(election_id)
    assert isinstance(electiondata, dict)


def test_can_get_lookupdata():
    elections = downloader.get_election_list()
    election = choice(elections)
    election_id = election["ID"]
    version = downloader.get_version(election_id)
    lookupdata = downloader.get_lookupdata(election_id, version)
    assert isinstance(lookupdata, dict)


def test_can_get_lookupdata_without_version():
    elections = downloader.get_election_list()
    election = choice(elections)
    election_id = election["ID"]
    lookupdata = downloader.get_lookupdata(election_id)
    assert isinstance(lookupdata, dict)

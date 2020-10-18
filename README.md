# CT election runner

> Python library and command line tool to scrape Connecticut's election data
> portal in real time.

## About

Connecticut's election night reporting system has an undocumented API that I
reverse engineered and have used as a data journalist starting in 2016 to build
live results
[portals](https://ctmirror.org/2018/08/14/unofficial-2018-primary-results-roll/) ([code](https://github.com/jakekara/ct-election-frontend-primary-18))
for [The Connecticut Mirror](https://ctmirror.org), where I used to work. I am
currently not working in data journalism as I am wandering around in the world
of digital humanities development, but I've always intended to make this code
public and finally had a few hours to do so.

**Note about code quality:** This is not the exact code I used as a data
journalist. I rewrote it to make it more presentable. It doesn't have proper
test coverage or documentation, or even error handling for that matter. I had
hoped to do more with it, but I don't know when I will be able to revisit it and
I wanted to make it available before the general election.

## CLI tool and library

This package contains a command line tool "ctrunner" and a Python library for
downloading data from the election night reporting system and to convert the raw
data to more useful spreadsheets.

## Install

```bash
pip install git+https://github.com/jakekara/ct-election-runner.git
python -m ctrunner.cli --help
usage: ctrunner - Connecticut election data runner [-h] {archive,parse,download} ...

positional arguments:
  {archive,parse,download}
                        commands

optional arguments:
  -h, --help            show this help message and exit

```

## CLI cookbook

### Get list of elections

This pipes the ctrunner downloader and the ctrunner parser together to download
the data in raw JSON format then convert it to a spreadsheet:

```bash
python -m ctrunner.cli download --election-list | ctrunner parse --data-type=election-list
ID,Name,DefaultElection
54,11/03/2020 -- Presidential Election,Y
55,08/11/2020 -- Democratic Presidential Preference Primary,N
57,08/11/2020 -- Republican Presidential Preference Primary,N
58,08/11/2020 -- Republican Primary,N
59,08/11/2020 -- Democratic Primary,N
50,01/21/2020 -- Special Election 151st Assembly,N
49,01/14/2020 -- Special Election 48th & 132nd Assembly,N
36,11/05/2019 -- November 2019 Municipal Election,N
42,09/10/2019 -- Democratic Primary,N
43,09/10/2019 -- Republican Primary,N
39,05/07/2019 -- Special Election 130th Assembly District,N
38,05/06/2019 -- May 2019 Municipal Elections,N
37,04/16/2019 -- Special Election 19th Assembly District,N
35,"02/26/2019 -- Special Election 3rd, 5th & 6th Senatorial Districts and 39th & ",N
31,11/06/2018 -- November 2018 State Election,N
33,08/14/2018 -- August 2018 Democratic Primary,N
34,08/14/2018 -- August 2018 Republican Primary,N
18,11/07/2017 -- November 2017 Municipal Election,N
24,04/25/2017 -- Special Election Assembly Districts 7th & 68th,N
1,11/08/2016 -- November Presidential Election,N
```

### Archive an election

Download the latest version of an election into a given archive directory.

While the download and parse subcommands use standard input and standard out,
the archive subcommand writes to files on disk in a special folder structure, so
you need to provide a destination folder where you want the archive to be
located.

```bash
python -m ctrunner.cli  archive --dest examples --election 1
```

Check out the examples folder in this repo to see the data that the archive
subcommand generates.

## Library

You can learn more about the library functions just by reading the cli tool
code. Here are the basics.

The downloader is for downloadin raw JSON files from the API. The parser is for
converting these JSON files to CSVs. The JSON files contain a lot more data than
the CSVs, so you might want to create your own tools based around the raw JSON
files.

### ctrunner.downloader

- `get_election_list` - get a list of all elections in the election system
- `get_data_for_election` - get data for a specific election given an ID
  corresponding to IDs from the `get_election_list` return data

There are plenty of other functions in that module, but these should really be
thought of as the main API.

### ctrunner.parser

- `convert_list(election_list_data)` - convert the results from
  `ctrunner.downloader.get_election_list` to a CSV
- `convert_election_data(election_data)` - convert the results from
  `ctrunner.download.get_data_for_election` to a CSV.

To see these in action, check out the CLI tool. The subcommands documented in
the help message are in the cli/commands folder, and those are the scripts that
make use of the library.

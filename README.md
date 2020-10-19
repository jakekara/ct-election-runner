# CT election runner

> Python library and command line tool to pull Connecticut's election data
> in real time.

## About

Connecticut's election night reporting system has an undocumented API that I
reverse engineered and used as a data journalist starting in 2015 to build live
results
[portals](https://ctmirror.org/2018/08/14/unofficial-2018-primary-results-roll/)
([code](https://github.com/jakekara/ct-election-frontend-primary-18)) for [The
Connecticut Mirror](https://ctmirror.org), where I used to work.

I've always intended to make this code public once I had time to clean it up. I
have never had time to really do that, and I doubt I ever will, so I'm just
releasing it as-is.

This repo isn't all that clean, it's not well documented, and it lacks test
coverage and even error handling. However, I felt that putting this out there in
its current state would be better than waiting until I have a lot of time to
spend on this, which will probably never happen. And I really just needed to get
it off my plate and stop kicking myself about not getting to it every time an
election season comes and goes.

## CLI tool and library

This package contains a command line tool "ctrunner" and a Python library for
downloading data from the election night reporting system and to convert the raw
data to more useful spreadsheets.

## Install

```bash
pip install -e git+https://github.com/jakekara/ct-election-runner.git#egg=ct-election-runner
ctrunner --help
```

This will output:

```bash
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
ctrunner download --election-list | ctrunner parse --data-type=election-list
```

This will output:

```bash
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

### Download an election and convert it to CSV

```bash
ctrunner  download --election 1 | ctrunner parse --data-type=election-data > election-1.csv
```

### Archive an election

Download the latest version of an election into a given archive directory.

While the download and parse subcommands use standard input and standard out,
the archive subcommand automates a common use case where you'll want to download
to results into a single output folder containing many elections, and keep past
versions. Keeping past versions was especially important on election night
because I wanted to be prepared to roll back in case a bad version came through
the API. It was also useful to go back and use past versions of the data to
replay how quickly the results of the election came in. That was particularly
important for news coverage when this system came out because it took several
days for all towns to put their results in when participation was not mandatory.

```bash
ctrunner  archive --dest examples --election 1
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

# CT election runner

> Python library and command line tool to scrape election data from
> Connecticut's election data portal live

## About

Connecticut's election night reporting system has an undocumented API that I
have used as a data journalist starting in 2016 to build live results portals
for a news organization where I used to work. I no longer work there, but I've
always intended to make this code public and finally had a few hours to do so.

**Note about code quality:** This is not code I used as a data journalist. I
rewrote it to make it more presentable. It doesn't have proper test coverage or
documentation, or even error handling for that matter. I had hoped to do more with it, but I don't know when I will be
able to revisit it and I wanted to make it available before the general
election.

## CLI tool and library

This package contains a command line tool "ctrunner" and a Python library for
downloading data from the election night reporting system and to convert the raw
data to more useful spreadsheets.

## Install

```bash
$ npm git+https://github.com/jakekara/ct-election-runner.git
$ ctrunner
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
$ ctrunner download --election-list | ctrunner parse --data-type=election-list
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
$ ctrunner archive --dest examples --election 1
```

Check out the examples folder in this repo to see the data that the archive subcommand generates.

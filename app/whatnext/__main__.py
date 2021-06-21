#!/usr/bin/env python
"""
Module load handler for execution via:

python -m whatnext
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import re

import click
import requests

from whatnext.storage import Repository, connect_db

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

__version__ = "0.1"

SOURCE_MARKDOWN_URLS = [
    "https://raw.githubusercontent.com/vinta/awesome-python/master/README.md",
    "https://raw.githubusercontent.com/shahraizali/awesome-django/master/README.md",
    "https://raw.githubusercontent.com/humiaozuzu/awesome-flask/master/README.md",
    "https://raw.githubusercontent.com/uralbash/awesome-pyramid/master/README.md",
    "https://raw.githubusercontent.com/sorrycc/awesome-javascript/master/README.md",
    "https://raw.githubusercontent.com/kozross/awesome-c/master/README.md",
    "https://raw.githubusercontent.com/aleksandar-todorovic/awesome-c/master/README.md",
    "https://raw.githubusercontent.com/uhub/awesome-c/master/README.md",
    "https://raw.githubusercontent.com/mrezak/awesome-python-1/master/README.md",
    "https://raw.githubusercontent.com/sindresorhus/awesome/master/README.md",
    "https://raw.githubusercontent.com/krishnasumanthm/Awesome-Python/master/README.md",
    "https://raw.githubusercontent.com/mahmoud/awesome-python-applications"
    "/master/README.md",
    "https://raw.githubusercontent.com/trananhkma/fucking-awesome-python"
    "/master/README.md",
]

# Organisations or Users who have requested to be excluded from typo fixes
BLACKLISTED_ORGUSERS = {"angvp"}


def obtain_sources():
    """
    Scan source list and return organizations/repositories
    """
    for url in SOURCE_MARKDOWN_URLS:
        for orgrepo in check_url(url):
            orguser = orgrepo.split("/", 1)[0]
            if orguser in BLACKLISTED_ORGUSERS:
                continue
            yield orgrepo


def check_url(url):
    """
    Download and process the url
    """
    results = "\n".join(get_all_markdown_github_links(url))
    return results.splitlines()


def get_all_markdown_github_links(url):
    """
    Obtain and filter markdown links to repositories.
    """
    links = get_all_markdown_links(url)
    for link in links:
        mobj = re.match(
            "https://github.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:/|$)", link
        )
        if mobj:
            yield mobj.group(1)


def get_all_markdown_links(url):
    """
    Obtain all the markdown links in the URL
    """
    data = download_url(url)
    matches = re.findall("[(]([^)]+)[)]", data)
    return matches


def download_url(url):
    """
    Obtain the URL content
    """
    return requests.get(url, timeout=120).text


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctxt):
    """
    Main click group handler
    """
    if ctxt.invoked_subcommand is None:
        run_invocation()


@main.command()
def invoke():
    """
    Primary command handler
    """
    run_invocation()


def run_invocation():
    """
    Execute the invocation
    """
    session = connect_db()
    for source in obtain_sources():
        session.merge(Repository(orgrepo=source))
        print(source)
    session.commit()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:

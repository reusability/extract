import re as regex

import pandas as pd
from attr import dataclass

from src.crawler import crawl_maven_project
from src.utils import Subprocess
from .command import command_git_tag, command_touch

# config
FILENAME_TAGS = "_tags.txt"
FILENAME_TAGS_UNMATCHED = "_tags_unmatched.txt"


def preprocess_github_tags(name, output_directory, github):
    # init
    tags = []
    filename = "{}/{}".format(output_directory, name) + FILENAME_TAGS
    command = command_git_tag(
        name, output_directory, github, FILENAME_TAGS
    )  # todo: fix command_git_tag to use filename

    # git
    Subprocess(command).Run()

    # store tags in variable
    with open(filename, "r") as content:
        # index 0 -> original tag,
        # index 1 -> remove prefix string
        for line in content:
            start_index = regex.search(r"\d", line)
            try:
                start_index = start_index.start()
                tags.append((line.strip(), line[start_index:].strip()))
            except Exception as error:  # noqa : F841
                pass
        tags.reverse()

    # touch unmatched
    Subprocess(command_touch(name, output_directory, FILENAME_TAGS_UNMATCHED)).Run()

    # return
    return tags


def preprocess_match_maven_tags(name, output_directory, releases, tags):
    # init
    matched = []
    filename = "{}/{}".format(output_directory, name) + FILENAME_TAGS_UNMATCHED

    # run
    for index, release in releases.iterrows():
        try:
            gh_tag = [i[1] for i in tags].index(release["release"])
            matched.append(
                Match_Maven_GH(gh_tag=tags[gh_tag][0], maven_release=release["release"])
            )
        except ValueError as error:  # noqa : F841
            with open(filename, "a") as file:
                file.write(release[0])

    # return
    return matched


def preprocess_maven_reuse(name, output_directory, maven):
    # TODO move to Crawler repo
    data = crawl_maven_project(maven)
    # write the data to .csv file
    data_frame = {"release": [], "usage": [], "date": []}
    for key, value in data.items():
        for minor in data[key]["releases"]:
            data_frame["release"].append(minor["release"])
            data_frame["usage"].append(int(minor["usage"].replace(",", "")))
            data_frame["date"].append(minor["date"])

    df = pd.DataFrame(data_frame)
    releases = df.sort_values(by="usage", ascending=False)

    # .csv format: release_number, usage, date
    # todo: maven_reuse should be const in preprocess.py
    releases.to_csv(
        "{}/{}_maven_reuse.csv".format(output_directory, name),
        index=False,
        header=False,
    )

    # return
    return releases


@dataclass
class Match_Maven_GH:
    gh_tag: str
    maven_release: str

import csv
import os
from src.extract import ProjectConfig


def cached_file_count(path):
    if not os.path.isfile(path):
        return 0
    file = open(path, "r")
    csv_reader = csv.reader(file, delimiter=",")
    counter = 0
    for _ in csv_reader:
        counter += 1
    return counter - 1


def cache_file_content(path):
    file = open(path, "r")
    csv_reader = csv.reader(file, delimiter=",")
    projects: {str: ProjectConfig} = {}

    skip = False
    id = None
    for (id, maven, _, github) in csv_reader:
        if not skip:
            skip = True
            continue
        project_config = ProjectConfig(
            name=maven.split("/")[-1],
            maven=maven,
            github=github,
        )

        projects[project_config] = project_config
        id = id

    return projects, int(id)

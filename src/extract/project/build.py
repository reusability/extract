import csv
import os
import time

from src.crawler import MavenCrawler
from src.extract import ProjectConfig
from src.extract.utils import cache

MAVEN_CSV_PATH = "outputs/etc/maven.csv"


def build_projects(count, categories, min_maven_usage, sleep) -> {}:
    # init
    projects: {str: ProjectConfig} = {}

    # open file
    try:
        file = open(MAVEN_CSV_PATH, "a+")
    except:  # noqa: E722
        os.mkdir("outputs/etc/")
        file = open(MAVEN_CSV_PATH, "a+")

    fieldnames = ["id", "maven", "usage", "github"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if cache.cached_file_count(MAVEN_CSV_PATH) > 0:
        projects, counter = cache.cache_file_content(MAVEN_CSV_PATH)
        counter += 1
    else:
        # init
        writer.writeheader()
        counter = 1

    # maven crawler
    maven_crawler = MavenCrawler(sleep=sleep, logger=None)

    # star
    while len(projects) < count:
        projects_maven_url = maven_crawler.list_projects()

        if len(projects_maven_url) == 0:
            break

        for project in projects_maven_url:
            tmp = {
                "id": counter,
                "maven": project["link"],
                "usage": project["usage"],
                "github": "None",
            }

            # get GH link from .pom file
            gh_url = maven_crawler.get_GH_url(project["link"])

            # if GH link is found
            if (
                gh_url != "None"
                and gh_url  # noqa : W503
                and int(project["usage"]) > min_maven_usage  # noqa : W503
            ):
                tmp["github"] = gh_url

                project_config = ProjectConfig(
                    name=project["link"].split("/")[-1],
                    maven=project["link"],
                    github=gh_url,
                )

                if project_config not in projects.keys():
                    projects[project_config] = project_config
                    writer.writerow(tmp)
                    counter += 1

            if len(projects) == count:
                break

            time.sleep(sleep)
    file.close()

    return projects

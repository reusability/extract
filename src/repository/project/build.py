import csv

from src.repository import ProjectConfig
from src.utils import Maven_Crawler
import time


def build_projects(count, categories, min_maven_usage, sleep) -> {}:
    # init
    projects: {str: ProjectConfig} = {}

    # maven crawler
    maven_crawler = Maven_Crawler(sleep=sleep)

    # open file
    file = open("outputs/etc/maven.csv", "a+")

    # init
    fieldnames = ["id", "maven", "usage", "github"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    counter = 1

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

    return

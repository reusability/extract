# __main__.py
# from src.app.helpers import AppBigQueryStorage
import click

from src.app import HelperAppGitHubCK
from src.app import HelperAppGitHubSM


# todos
# pre-mining -- branch: feature/mining
# 1. create yaml with mapped github repositories and associated projects
# 2. utils/yaml.py -- should pull and push data into mining algorithm

# data mining -> data wrangling -- branch: feature/mining
# 1. sql query script to fetch a single project
# 2. remove unwanted files (wrangling) -- keep only .java but should be extendable to more files
# 3. iterate query script to fetch various projects
#
# data processing (metrics analysis) -- branch: feature/runner-ck
# 1. once fetch a project, run CK metrics on the files
# 2. clean output and push to csv file
# 3. iterate multiple projects
#
# data post-processing (aws integration for on-line usage) -- branch: env/cd-github-aws-s3
# 1. push csv data into an S3 object
# 2. /research repository should pull the S3 object
#
# documents
# 1. create sequence diagram for mining
# 2. create sequence diagram for metrics analysis
# 3. update architecture (high-level and classes)
#
# App.Run() -- info below
# while isNotEnd(repository.yaml):
#   fetch item i in yaml file, e.g <organisation_1>/<project_1>
#   mine that repository
#   clean files
#   run ck metrics
#   clean metrics output
#   output to csv
#
# flow -- mining -> refinement -> processing -> post-processing
#
#
# utility functions
# - subprocess - accesing terminal commands like the ck runner
# - yaml - read yaml files
#
# future pipeline goals
# - runner
#   - ck
#   - sourcemeter
#   - MOOD
# - mining
#   - BigQuery
#   - GHArchive
#   - GHTorrent
# - automate yaml config pipeline
#   - fetch projects from maven based on reuse
#
# s = requests.Session()
# cookies = dict(cookies_are='working')
# res = s.get('https://mvnrepository.com/', cookies=cookies)
# print(res)
#
# https://repo.maven.apache.org/maven2/
@click.command()
@click.option("--metrics", default="ck", help="ck metrics or sourcemeter; ck or sm")
@click.option("--count", default=5, help="number of projects to fetch", type=click.INT)
@click.option(
    "--sleep", default=2, help="time to sleep between fetches", type=click.INT
)
@click.option(
    "--mavenusage", default=50, help="minimum maven usage to fetch", type=click.INT
)
@click.option(
    "--versions",
    default=1,
    help="number of releases to be analysed for each project",
    type=click.INT,
)
def main(metrics, count, sleep, mavenusage, versions):
    # init
    categories = [
        "popular",
        "open-source/testing-frameworks",
        "open-source/json-libraries",
        "open-source/mocking",
    ]

    # create
    config = {
        "categories": categories,
        "count": count,
        "sleep": sleep,
        "min_maven_usage": mavenusage,
        "min_version_count": versions,
    }

    app = build_app(metrics, config)

    # preprocess
    app.Pre()

    # run
    app.Run()

    # exit
    app.Stop()


def build_app(metrics, config):
    # todo: clean up
    if metrics == "ck":
        app = HelperAppGitHubCK(config)
    elif metrics == "sm":
        app = HelperAppGitHubSM(config)
    else:
        raise ValueError("the metrics is not found")

    return app


if __name__ == "__main__":
    main()

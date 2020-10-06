# __main__.py
# from src.app.helpers import AppBigQueryStorage
from src.app import HelperAppGitHubCK
from src.app import HelperAppGitHubSM
import click

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


@click.command()
@click.option("--metrics", default="ck", help="ck metrics or sourcemeter; ck or sm")
@click.option("--count", default=5, help="number of projects to fetch", type=click.INT)
@click.option(
    "--sleep", default=2, help="time to sleep between fetches", type=click.INT
)
@click.option(
    "--mavenusage", default=10, help="minimum maven usage to fetch", type=click.INT
)
def main(metrics, count, sleep, mavenusage):
    # init
    categories = [
        "popular",
        "open-source/testing-frameworks",
        "open-source/json-libraries",
        "open-source/mocking",
    ]

    # init
    app = build_app(metrics, count, sleep, categories, mavenusage)

    # run
    app.Run()

    # exit
    app.Stop()


def build_app(metrics, count, sleep, categories, mavenusage):
    # todo: clean up
    if metrics == "ck":
        app = HelperAppGitHubCK(count, sleep, categories, mavenusage)
    elif metrics == "sm":
        app = HelperAppGitHubSM(count, sleep, categories, mavenusage)
    else:
        raise ValueError("the metrics is not found")

    return app


if __name__ == "__main__":
    main()

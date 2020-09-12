# __main__.py
# from src.app.helpers import AppBigQueryStorage
from src.app import HelperAppGitHub
import os
from dotenv import load_dotenv

load_dotenv()

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
# updated todos list
# pre-mining and mining
# 1. manually fetch projects from mvn
#   - find their reference in github
#   - find their associated tags
# 2. mine the repositories
#   - git clone projects[i].github
#   while hasTagsLeft(projects[i]):
#   - git checkout tags/projects[i].tags[j]
#   - mkdir outputs/scala
#   - pipeline management (java files) --- extras; documentation, etc
#       - run ck metrics on that project
#       - output into csv
#       - bundle csv in the format %projects[i]-tags[j]
#           - cp class.csv ../outputs/projects[i]/tags[j]
#           - cp projects.csv ../outputs/projects[i]/tags[j]
#   - append the csv path into an array list
#
# requirements - week 7
#   - P1 - incorporate Matthew's Python script
#   - P1 - tag
#   - P2 - EC2 + S3 object
#   - P3 - source meter documentation


def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../.bigquery.gson"

    # init
    app = HelperAppGitHub()

    # run
    app.Run()

    # exit
    app.Stop()


if __name__ == "__main__":
    main()

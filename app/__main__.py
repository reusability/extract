# __main__.py
from .helpers import AppBigQueryStorage

# todos
# pre-mining
# 1. create yaml with mapped github repositories and associated projects
# 2. utils/yaml.py -- should pull and push data into mining algorithm
#
# data mining -> data wrangling
# 1. sql query script to fetch a single project
# 2. remove unwanted files (wrangling) -- keep only .java but should be extendable to more files
# 3. iterate query script to fetch various projects
#
# data processing (metrics analysis)
# 1. once fetch a project, run CK metrics on the files
# 2. clean output and push to csv file
# 3. iterate multiple projects
#
# data post-processing (aws integration for on-line usage)
# 1. push csv data into an S3 object
# 2. /research repository should pull the S3 object
#
# documents
# 1. create sequence diagram for mining
# 2. create sequence diagram for metrics analysis
# 3. update architecture (high-level and classes)
#
# flow -- mining -> refinement -> processing -> post-processing


def main():
    # init
    app = AppBigQueryStorage()  # noqa: F841

    # run
    # app.Run()


if __name__ == "__main__":
    main()

# __main__.py
from .helpers import AppBigQueryStorage

# todos
# fetch (data mining -> data refinement)
# 1. sql query script to fetch a single project
# 2. iterate query script to fetch various projects
#
# metrics analysis (data processing)
# 1. once fetch a project, run CK metrics on the files
# 2. clean output and push to csv file
# 3. iterate multiple projects
#
# data on aws (data post-processing)
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

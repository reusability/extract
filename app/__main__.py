# __main__.py
from .helpers import AppBigQueryAPI

if __name__ == "__main__":
    # init
    app = AppBigQueryAPI()

    # run
    app.Run()

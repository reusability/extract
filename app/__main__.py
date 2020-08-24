# __main__.py
from .helpers import AppBigQueryStorage


def main():
    # init
    app = AppBigQueryStorage()  # noqa: F841

    # run
    # app.Run()


if __name__ == "__main__":
    main()

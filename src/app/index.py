# src.py
from src.repository import RepositoryEnum
from .config import AppConfig
from .config import AppConfigRepository

from src.utils import Logger

# from src.utils import Zip_Folder, copy_files
# from pathlib import Path


class App:
    def __init__(self, config: AppConfig):
        # config files
        self.config: AppConfig = config

        # logger
        self.logger: Logger = Logger(config.name)
        self.logger.l.info("application started!")

        # metrics
        self.metric = config.metric(config.metric_config)
        self.logger.l.info("metrics init")

    def Run(self):
        pass

    def Stop(self):
        pass


class AppRepositoryBigQuery(App):
    def __init__(self, config: AppConfigRepository):
        # init
        super().__init__(config)

        # setup
        repository = config.repository
        repository_config = config.repository_config

        # init
        self.logger.l.info(
            "creating repository -> db_type: %s",
            RepositoryEnum.to_char(repository_config.dbType),
        )
        self.repository: config = repository(repository_config)
        self.logger.l.info("repository created!")

    def Run(self):
        github_query = """
            SELECT f.repo_name, c.content
            FROM bigquery-public-data.github_repos.files f left join bigquery-public-data.github_repos.contents c
            on f.id = c.id
            where f.path like '%.java' and f.repo_name in ('scala/scala', 'scalatest/scalatest')
            limit 100;
        """

        query_job = self.repository.query(github_query)

        for row in query_job:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        pass


class AppRepositoryGitHub(AppRepositoryBigQuery):
    def __init__(self, config: AppConfigRepository):
        # init
        super().__init__(config)

        # setup projects
        self.repository.build_projects(config.projects_config)

    def Run(self):
        # do stuff
        self.repository.do_stuff(self.metric)

        # TODO: make this as an option
        # Zip_Folder("{}/src/outputs".format(
        #     str(Path().resolve().parent)
        # ))
        #
        # http_dir = '/var/www/html/output'
        # copy_files(source="outputs.zip", target=http_dir)

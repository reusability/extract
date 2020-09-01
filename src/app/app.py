# src.py
from src.repository import RepositoryEnum

from src.app import AppConfig
from src.app import AppConfigRepository

# from src.repository import RepositoryEnum
# from src.repository import RepositoryBigQueryEnum
# from src.repository import CloneConfig

# from src.project import generate_random_query
from src.utils import Logger, make_dir, remove_dir
from pathlib import Path


class App:
    def __init__(self, config: AppConfig):
        # config files
        self.config: AppConfig = config

        # logger
        self.logger: Logger = Logger(config.name)
        self.logger.l.info("application started!")

        # metrics
        self.metric_config = config.metric_config
        self.metric = config.metric
        self.logger.l.info("metrics init", self.metric_config.name)

    def Run(self):
        pass

    def Stop(self):
        pass


class AppRepository(App):
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
        # github_query = """
        #     SELECT f.repo_name, c.content
        #     FROM bigquery-public-data.github_repos.files f left join bigquery-public-data.github_repos.contents c
        #     on f.id = c.id
        #     where f.path like '%.java' and f.repo_name in ('scala/scala', 'scalatest/scalatest')
        #     limit 100;
        # """
        #
        # query_job = self.repository.query(github_query)
        #
        # for row in query_job:
        #     # Row values can be accessed by field name or index.
        #     print("name={}, count={}".format(row[0], row["total_people"]))
        pass

    def Stop(self):
        pass


class AppGitHub(AppRepository):
    def Run(self):
        for repo in self.clone_config:
            new_repo = self.clone(repo)
            new_repo.clone_repo()
            for v in repo.versions:
                new_repo.checkout_version(v)
                make_dir(new_repo.dir + "/{}".format(v))
                self.metric_config = self.metric_config._replace(
                    project_dir="{}/{}".format(
                        new_repo.dir, new_repo.config.project_name
                    ),
                    output_dir="{}/{}".format(new_repo.dir, v),
                )

                m = self.metric(self.metric_config)
                m.Run()
                m.move_output(source=str(Path().resolve().parent) + "/src/")
            remove_dir("{}/{}".format(new_repo.dir, new_repo.config.project_name))

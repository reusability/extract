# src.py
from src.repository import Repository
from src.repository import RepositoryConfig

# from src.repository import RepositoryEnum
# from src.repository import RepositoryBigQueryEnum
# from src.repository import CloneConfig
from src.repository import Clone
from src.matric import CK
from src.matric import MetricConfig

# from src.project import generate_random_query
from typing import NamedTuple
from src.utils import Logger, make_dir, remove_dir
from pathlib import Path


class AppConfig(NamedTuple):
    name: str
    repository: Repository
    repository_config: RepositoryConfig
    clone: Clone
    clone_config: list
    metric_config: MetricConfig
    metric: CK


class App:
    def __init__(self, appConfig: AppConfig):
        # init
        self.logger: Logger = Logger(appConfig.name)
        self.logger.l.info("application started!")

        # setup
        self.clone = appConfig.clone
        self.clone_config = appConfig.clone_config

        self.metric_config = appConfig.metric_config
        self.metric = appConfig.metric

        self.logger.l.info("cloning to github using subprocess")
        # repository = appConfig.repository
        # repository_config = appConfig.repository_config
        # self.logger.l.info(
        #     "creating repository -> db_type: %s, api_type: %s",
        #     RepositoryEnum.to_char(repository_config.dbType),
        #     RepositoryBigQueryEnum.to_char(repository_config.apiType),
        # )
        # self.repository: Repository = repository(repository_config)
        # self.logger.l.info("repository created!")

    def Run(self):
        # generate query
        # github_query = """
        #     SELECT f.repo_name, c.content
        #     FROM bigquery-public-data.github_repos.files f left join bigquery-public-data.github_repos.contents c
        #     on f.id = c.id
        #     where f.path like '%.java' and f.repo_name in ('scala/scala', 'scalatest/scalatest')
        #     limit 100;
        # """

        # job
        # query_job = self.repository.query("None")

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
                m.run_ck()
                m.move_output(source=str(Path().resolve().parent) + "/src/")
            remove_dir("{}/{}".format(new_repo.dir, new_repo.config.project_name))
        # print
        # print("The query data:")
        # counter = 0
        # for row in query_job:
        #     print(row)
        #     if counter > 100000:
        #         break
        #     counter += 1

        # for row in query_job:
        #     # Row values can be accessed by field name or index.
        #     print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        exit()

# app.py
from .repository import RepositoryBigQuery
from .project import generate_random_query

# todo: abstract big query from App


class App:
    def __init__(self):
        self.repository = RepositoryBigQuery()

    def Run(self):
        # generate query
        query = generate_random_query()  # todo: fix

        # job
        query_job = self.repository.query(query)

        # print
        print("The query data:")
        for row in query_job:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        pass

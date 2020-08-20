# __main__.py
# used to the main files in this packageg
from .repository import RepositoryBigQuery, generate_random_query

if __name__ == "__main__":
    # init
    repository: RepositoryBigQuery = RepositoryBigQuery()

    # generate query
    query = generate_random_query()  # todo: fix

    # job
    query_job = repository.query(query)

    # print
    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print("name={}, count={}".format(row[0], row["total_people"]))

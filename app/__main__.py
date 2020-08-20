# __main__.py
# used to the main files in this packageg
from .app import App
from .repository import RepositoryBigQuery

if __name__ == '__main__':
    App.run()

    repository = RepositoryBigQuery()
    query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20
    """
    query_job = repository.query(query)

    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print("name={}, count={}".format(row[0], row["total_people"]))

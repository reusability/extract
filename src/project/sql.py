# sql.py
from jinja2 import Template


# todo: turn this into a class


def generate_random_query():
    count_people_query = """
        SELECT name, SUM(number) as total_people
        FROM `{{ bigquery_repository }}`
        WHERE state = '{{ bigquery_state }}'
        GROUP BY name, state
        ORDER BY total_people DESC
        {% if limit_count %}
        LIMIT {{ limit_count }}
        {% endif %}
        """

    data = {
        "bigquery_repository": "bigquery-public-data.usa_names.usa_1910_2013",
        "bigquery_state": "TX",
        "limit_count": "20",
    }

    return Template(count_people_query).render(data)

from typing import NamedTuple


class MetricConfig(NamedTuple):
    name: str
    project_dir: str
    output_dir: str
    source_code_dir: str

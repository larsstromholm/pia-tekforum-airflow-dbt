import dlt
import dlt.common
import dlt.common.configuration
import dlt.common.destination
import dlt.common.destination.reference
from demo_dlt.extract.rest_api import (
    rest_api_source,
)

nobel_source = rest_api_source(
    {
        "client": {
            "base_url": "https://api.nobelprize.org/2.1/",
            "paginator": {
                "type": "json_response",
                "next_url_path": "paging.next",
            },
        },
        "resources": ["laureates", "nobelPrizes"],
    }
)


def nobel_pipeline(
    destination: dlt.common.destination.reference.DestinationClientConfiguration,
) -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="nobel",
        destination=destination,
        dataset_name="nobel",
        dev_mode=False,
    )

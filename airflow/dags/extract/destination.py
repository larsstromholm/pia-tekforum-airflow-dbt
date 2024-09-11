import dlt
from utils.settings import settings

postgres_destination = dlt.destinations.postgres(settings.postgres_dsn)

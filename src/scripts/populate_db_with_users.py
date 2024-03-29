import os

from dotenv import load_dotenv
from pyspark.sql import SparkSession

from conf import catalog, globals, params, paths

load_dotenv(
    paths.get_path(
        paths.ENV,
        storage=globals.Storage.DOCKER,
    )
)

session = (
    SparkSession.builder.appName("populate-users")
    .config(map=params.Spark.spark_config)
    .getOrCreate()
)

url = f"jdbc:postgresql://{os.getenv('POSTGRES_IP')}:{os.getenv('POSTGRES_PORT')}/app"
properties = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver",
}
table_name = "users"

ext_filepath = paths.get_path(
    paths.DATA_01EXTERNAL,
    catalog.Sources.MOVIELENS,
    catalog.Datasets.RATINGS,
    suffix=catalog.FileFormat.CSV,
    as_string=True,
)
remote_ext_filepath = paths.get_path(
    paths.DATA_01RAW,
    catalog.Sources.MOVIELENS,
    catalog.DatasetType.PRODUCTION,
    catalog.Datasets.RATINGS,
    suffix=catalog.FileFormat.CSV,
    storage=globals.Storage.S3,
    as_string=True,
)

dataset = session.read.load(
    remote_ext_filepath, format=catalog.FileFormat.CSV[1:], header=True, inferSchema=True
)
dataset[["userId"]].distinct().write.jdbc(
    url, table_name, mode="overwrite", properties=properties
)

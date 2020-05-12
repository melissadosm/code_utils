# Importing libraries ---------------------------
import importlib

queries = importlib.import_module('queries')
messages = importlib.import_module('messages')
from datetime import date

# Initialize variables ---------------------------
webhook_url = 'https://hooks.slack.com/services/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'
day = date.today()


# Spark functions ---------------------------
def register_dialect(spark):
    """ Registering connection between spark and BQ"""
    try:
        # Register the connector
        spark._jvm.com.merlin.dataengineering.spark.common.SparkUtils.registerBigqueryDialect()

        # define connector with BQ
        props = {"driver": "com.simba.googlebigquery.jdbc42.Driver"}

        # define BQ project
        project = "merlin-pro"

        # return
        return project, props
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error registering dialect [`extract.register_dialect`] ",
            day,
            False)


def execute_query(spark, query):
    """ Executing query in BQ """
    try:
        # register connector before query
        project, props = register_dialect(spark)

        # return
        return (
            spark.
                read.
                option("queryTimeout", 600).
                option("fetchsize", 20000).
                jdbc(
                url=
                f"jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;ProjectId={project};"
                f"Timeout=600;OAuthType=3;EnableHighThroughPutAPI=1",
                table=f"({query}) AS T",
                properties=props
            )
        )
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error executing query [`extract.execute_query`] ",
            day,
            False)


def extract_bq(tables, spark):
    """
    Extracting tables from BQ
    """
    try:
        for table in tables:
            query_name = 'query_' + table

            globals()[table] = execute_query(
                spark,
                getattr(queries, query_name)
            ).repartition(5, "iduser")

        return sendgrid_events, sent_events, clicked_events
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error extracting query [`extract.extract_bq`] ",
            day,
            False)

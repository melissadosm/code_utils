import argparse
import importlib

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

if __name__ == "__main__":
    """
        Usage: candidate_monetization --path [base_path]
    """

    # Initialize Spark module ------------------------------

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="gcs base path")
    args = parser.parse_args()

    spark = SparkSession.builder.appName("CandidateMonetizationBQ").getOrCreate()
    sqlContext = SQLContext(spark)

    # Importing packages ----------------------------------

    # The imports need to happen after the Spark module has been initialized
    from datetime import date
    from pyspark.sql import functions as F
    from pyspark.sql import DataFrame

    # Personal tools
    queries = importlib.import_module('queries')
    extract = importlib.import_module('extract')
    preprocess = importlib.import_module('preprocess')
    messages = importlib.import_module('messages')

    # Initialize variables ----------------------------------

    # Set the webhook_url to the one provided by Slack
    webhook_url = 'https://hooks.slack.com/services/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'
    day = date.today()

    # Posting start message
    messages.post_message_to_slack(
        webhook_url,
        "[PySpark] Hello hello! :wave: Today's run of candidate_monetization is starting! :mia: ",
        day,
        False)

    # Extracting data from BQ ----------------------------------
    tables = [
        'sendgrid_events',
        'sent_events',
        'clicked_events'
    ]

    source_sendgrid, source_sent, source_clicked = extract.extract_bq(tables, spark)

    # Saving data in GCS ----------------------------------

    # Define locations in google cloud storage
    # location_source_sendgrid = "gs://merlin-datascience/melissa/candidate_monetization_bq/source_sendgrid"
    # location_source_sent = "gs://merlin-datascience/melissa/candidate_monetization_bq/source_sent"
    # location_source_clicked = "gs://merlin-datascience/melissa/candidate_monetization_bq/source_clicked"
    #
    # # Write .parquet versions of the data loaded from BQ
    # source_sendgrid.write.mode("overwrite").partitionBy("subject_id").parquet(location_source_sendgrid + ".parquet")
    # source_sent.write.mode("overwrite").partitionBy("subject_id").parquet(location_source_sent + ".parquet")
    # source_clicked.write.mode("overwrite").partitionBy("subject_id").parquet(location_source_clicked + ".parquet")
    #
    # # Read .parquet versions of the tables written the storage
    # source_sendgrid = sqlContext.read.parquet(location_source_sendgrid + "*.parquet")
    # source_sent = sqlContext.read.parquet(location_source_sent + "*.parquet")
    # source_clicked = sqlContext.read.parquet(location_source_clicked + "*.parquet")


    # Posting finish extraction message
    messages.post_message_to_slack(
        webhook_url,
        "Data extraction completed",
        day,
        "• Source sendgrid size: {} \n • Source mails sent size: {} \n • Source clicked size: {}".\
            format(source_sendgrid.count(), source_sent.count(), source_clicked.count()),
        True
    )

    # Preprocessing data ----------------------------------

    # Building DF for actions from mails
    df_sent = preprocess.preprocess_emails_sent(source_sent, source_sendgrid)
    df_opened = preprocess.preprocess_emails_opened(source_sendgrid)
    df_clicked = preprocess.preprocess_emails_clicked(source_clicked)

    #Building funnel and master table
    df_funnel = preprocess.build_funnel(df_sent, df_opened, df_clicked)
    df_master = preprocess.build_master(df_funnel)
    cols_num_null = ['num_clicks']
    df_master = preprocess.preprocess_master(df_master,cols_num_null)

    messages.post_message_to_slack(
        webhook_url,
        "Preprocessing finished! \n Proceeding to export table in BQ.",
        day,
        False)

    # Exporting data ----------------------------------
    write_path = "merlin-pro:miscellaneous.candidate_monetization_mails"
    df_master.write \
          .format("bigquery") \
          .option("table", write_path) \
          .option("temporaryGcsBucket", "merlin-datascience/hadoop/tmp/") \
          .option("intermediateFormat", "orc") \
          .option("partitionField", "timestamp") \
          .mode("overwrite") \
          .save()

    # Posting finish extraction message
    messages.post_message_to_slack(
        webhook_url,
        "[PySpark] Process finished!",
        day,
        " • Data loaded in `{}` \n • Table size: {}".format(write_path, df_master.count()),
        True)

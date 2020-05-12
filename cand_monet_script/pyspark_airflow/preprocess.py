# Importing libraries ---------------------------
import importlib
from pyspark.sql import functions as F
from pyspark.sql import DataFrame

messages = importlib.import_module('messages')
from datetime import date

# Initialize variables ---------------------------
webhook_url = 'https://hooks.slack.com/services/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'
day = date.today()

# Spark functions ---------------------------
def preprocess_emails_sent(source_sent, source_sendgrid):
    '''
    Preprocess emails sent df
    @source_sent: source emails sent
    @source_sendgrid: source events of sendgrid
    '''

    try:
        list_bounce = ["email-bounce", "email-dropped"]
        list_unsubscribed = ["email-group_unsubscribe", "email-unsubscribe"]
        list_spam = ["email-spamreport"]

        bounced_mails = source_sendgrid.filter(source_sendgrid.eventname.isin(list_bounce)).dropDuplicates(["iduser", "email_id"])
        unsubscribed_mails = source_sendgrid.filter(source_sendgrid.eventname.isin(list_unsubscribed)).dropDuplicates(["iduser", "email_id"])
        spam_mails = source_sendgrid.filter(source_sendgrid.eventname.isin(list_spam)).dropDuplicates(["iduser", "email_id"])

        # Bounced Mails
        df_sent = source_sent.join(bounced_mails.select(["iduser", "eventname", 'email_id']), on=["iduser", "email_id"], how="left")
        df_sent = df_sent.withColumn('bounced_mail',
            F.when(F.col("eventname").isin(list_bounce), True)\
            .otherwise(False)
        )
        df_sent = df_sent.drop("eventname")

        # Unsubscribed Mails
        df_sent = df_sent.join(unsubscribed_mails.select(["iduser", "eventname", 'email_id']), on=["iduser", "email_id"], how="left")
        df_sent = df_sent.withColumn('unsubscribed_mail',
            F.when(F.col("eventname").isin(list_unsubscribed), True)\
            .otherwise(False)
        )
        df_sent = df_sent.drop("eventname")

        # Spam Mails
        df_sent = df_sent.join(spam_mails.select(["iduser", "eventname", 'email_id']), on=["iduser", "email_id"], how="left")
        df_sent = df_sent.withColumn('spam_mail',
            F.when(F.col("eventname").isin(list_spam), True)\
            .otherwise(False)
        )
        df_sent = df_sent.drop("eventname")

        return df_sent

    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error preprocessing emails sent [`preprocess.preprocess_emails_sent`] ",
            day,
            False)

def preprocess_emails_opened(source_sendgrid):
    '''Preprocess email opened df'''

    try:
        df_opened = source_sendgrid.filter(source_sendgrid.eventname == 'email-open').dropDuplicates()
        df_opened = df_opened.withColumnRenamed('timestamp', 'opened_timestamp')
        df_opened = df_opened.dropDuplicates(['iduser', 'email_id'])

        return df_opened
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error preprocessing emails opened [`preprocess.preprocess_emails_opened`] ",
            day,
            False)

def preprocess_emails_clicked(source_clicked):
    '''Preprocess emails clicked df'''

    try:
        df_clicked = source_clicked.withColumnRenamed('timestamp', 'clicked_timestamp')
        df_clicked = source_clicked.withColumnRenamed('ziprecruiter_job_id', 'zipr_jobid_clicked')
        df_clicked = df_clicked.dropDuplicates(['iduser', 'email_id', 'zipr_jobid_clicked'])
        df_clicked = df_clicked.groupBy(['iduser', 'email_id']).count()
        df_clicked = df_clicked.withColumnRenamed('count', 'num_clicks')
        return df_clicked
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error preprocessing emails clicked [`preprocess.preprocess_emails_clicked`] ",
            day,
            False)

def build_funnel(df_sent, df_opened, df_clicked):
    '''Builds funnel from mail sent to clicked, campaign info and user characteristics + stratification. '''

    try:
        df_funnel = df_sent.join(df_opened.drop("campaign", "subject_id"), on=["iduser", "email_id"], how="left")
        df_funnel = df_funnel.join(df_clicked, on=["iduser", "email_id"], how="left")

        return df_funnel
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error building funnel [`preprocess.build_funnel`] ",
            day,
            False)

def build_master(df_funnel):
    '''Builds raw master table for analysis'''

    try:
        df_master = df_funnel.withColumn('opened_mail',
            F.when(df_funnel.opened_timestamp.isNotNull(), True)\
            .otherwise(False)
        )
        df_master = df_master.withColumn('clicked_mail',
            F.when(df_funnel.num_clicks.isNotNull(), True)\
            .otherwise(False)
        )
        df_master = df_master.drop('ziprecruiter_job_id_array', 'eventname')

        return df_master
    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error building master [`preprocess.build_master`] ",
            day,
            False)

def preprocess_master(df_master, cols_num_null):
    '''
    Preprocess master table, ready to be analized
    @df_master: Master df to be preprocessed
    @values_num_dict: Dictionary with all numeric values to be replaced (NaNs)
    @values_bool_dict: Dictionary with all boolean values to be replaced (NaNs)
    '''

    try:
        # Replace all NaN elements in columns with its respective value.
        # Numerical
        df_master = df_master.fillna(0, subset=cols_num_null)

        return df_master

    except:
        messages.post_message_to_slack(
            webhook_url,
            "[PySpark] :heavy_exclamation_mark: Error preprocessing master [`preprocess.preprocess_master`] ",
            day,
            False)

    

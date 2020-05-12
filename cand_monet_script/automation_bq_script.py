# Importing libraries
import slack_messages
import extract_automation as extract
import preprocess_automation as preprocess
import pandas_gbq
from datetime import date

# Posting start message in Slack
webhook_url = 'https://hooks.slack.com/services/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'
day = date.today()
slack_messages.post_message_to_slack(
    webhook_url,
    "[Python] Hello hello! :wave: Today's run of candidate_monetization is starting! :mia: ",
    day,
    False)

# Extracting data
source_sendgrid, source_sent, source_clicked = extract.extract_data_candidate(tables = [
        'sendgrid_events',
        'sent_events',
        'clicked_events'
])

# Posting finish extraction message
slack_messages.post_message_to_slack(
    webhook_url,
    "Data extraction completed",
    day,
    "• Source sendgrid size: {} \n • Source mails sent size: {} \n • Source clicked size: {}".\
            format(len(source_sendgrid), len(source_sent), len(source_clicked)),
    True)

# Preprocessing data
df_sent = preprocess.preprocess_emails_sent(source_sent, source_sendgrid)
df_opened = preprocess.preprocess_emails_opened(source_sendgrid)
df_clicked = preprocess.preprocess_emails_clicked(source_clicked)

# Builiding funnel: Sent -> Opened -> Clicked
df_funnel = preprocess.build_funnel(df_sent, df_opened, df_clicked)

# Building master dataframe
drop_cols_master = ['ziprecruiter_job_id_array', 'eventname']
df_master = preprocess.build_master(df_funnel, drop_cols_master)

# Preprocessing master dataframe
values_bool = dict.fromkeys(['num_clicks'], 0)
df_master = preprocess.preprocess_master(df_master, values_num_dict={}, values_bool_dict=values_bool)

# Importing to GBQ
bq_table_name = 'miscellaneous.candidate_monetization_mails'
print('Saving results to {}'.format(bq_table_name))
df_master.to_gbq(bq_table_name, 'merlin-pro', if_exists='replace')

# Posting finish extraction message
slack_messages.post_message_to_slack(
    webhook_url,
    "[Python] Process finished!",
    day,
    " • Data loaded in `{}` \n • Table size: {}".format(bq_table_name, len(df_master)),
    True)

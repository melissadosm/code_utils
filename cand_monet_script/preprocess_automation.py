import pandas as pd
import numpy as np


def preprocess_emails_sent(source_sent, source_sendgrid):
    '''
    Preprocess emails sent df
    @source_sent: source emails sent
    @source_sendgrid: source events of sendgrid
    '''
    print('Preprocessing emails sent...')

    try:
        list_bounce = ['email-bounce', 'email-dropped']
        list_unsubscribed = ['email-group_unsubscribe', 'email-unsubscribe']
        list_spam = ['email-spamreport']

        bounced_mails = source_sendgrid[source_sendgrid['eventname'].isin(list_bounce)] \
            .drop_duplicates(subset=['iduser', 'email_id'])
        unsubscribed_mails = source_sendgrid[source_sendgrid['eventname'].isin(list_unsubscribed)] \
            .drop_duplicates(subset=['iduser', 'email_id'])
        spam_mails = source_sendgrid[source_sendgrid['eventname'].isin(list_spam)] \
            .drop_duplicates(subset=['iduser', 'email_id'])

        print('Number emails sent: ' + str(len(source_sent)))

        # Bounced Mails
        df_sent = pd.merge(source_sent, bounced_mails[['iduser', 'eventname', 'email_id']], on=['iduser', 'email_id'],
                           how='left')
        df_sent['bounced_mail'] = False
        df_sent.loc[df_sent['eventname'].isin(list_bounce), 'bounced_mail'] = True
        print('Number emails bounced/dropped: {}'.format(len(df_sent[df_sent['bounced_mail']])))
        df_sent = df_sent.drop(columns=['eventname'])

        # Unsubscribed Mails
        df_sent = pd.merge(df_sent, unsubscribed_mails[['iduser', 'eventname', 'email_id']], on=['iduser', 'email_id'],
                           how='left')
        df_sent['unsubscribed_mail'] = False
        df_sent.loc[df_sent['eventname'].isin(list_unsubscribed), 'unsubscribed_mail'] = True
        print('Number emails unsubscribed: {}'.format(len(df_sent[df_sent['unsubscribed_mail']])))
        df_sent = df_sent.drop(columns=['eventname'])

        # Spam Mails
        df_sent = pd.merge(df_sent, spam_mails[['iduser', 'eventname', 'email_id']], on=['iduser', 'email_id'], how='left')
        df_sent['spam_mail'] = False
        df_sent.loc[df_sent['eventname'].isin(list_spam), 'spam_mail'] = True
        print('Number emails spammed: {}'.format(len(df_sent[df_sent['spam_mail']])))
        df_sent = df_sent.drop(columns=['eventname'])

        return df_sent

    except:
        print('Error preprocessing emails sent!')


def preprocess_emails_opened(source_sendgrid):
    '''Preprocess email opened df'''
    print('Preprocessing emails opened...')
    try:
        df_opened = source_sendgrid.loc[source_sendgrid['eventname'] == 'email-open', :].drop_duplicates()
        df_opened.rename(columns={'timestamp': 'opened_timestamp'}, inplace=True)
        print('Length emails opened with duplicates: ' + str(len(df_opened)))

        df_opened = df_opened.drop_duplicates(subset=['iduser', 'email_id'])
        print('Length emails opened without duplicates: ' + str(len(df_opened)))

        return df_opened
    except:
        print('Error preprocessing emails opened!')

def preprocess_emails_clicked(source_clicked):
    '''Preprocess emails clicked df'''
    print('Preprocessing emails clicked...')
    try:
        df_clicked = source_clicked.copy()

        df_clicked.rename(columns={'timestamp': 'clicked_timestamp', 'ziprecruiter_job_id': 'zipr_jobid_clicked'},
                          inplace=True)

        print('Length emails clicked with duplicates: ' + str(len(df_clicked)))
        df_clicked = df_clicked.drop_duplicates(subset=['iduser', 'email_id', 'zipr_jobid_clicked'])

        df_clicked = df_clicked.groupby(['iduser', 'email_id']).size().reset_index(name='num_clicks')
        print('Length emails clicked without duplicates: ' + str(len(df_clicked)))

        return df_clicked
    except:
        print('Error preprocessing emails clicked!')


def build_funnel(df_sent, df_opened, df_clicked):
    '''Builds funnel from mail sent to clicked, campaign info and user characteristics + stratification. '''
    print('Building funnel...')
    try:
        print('Length before joining: ' + str(len(df_sent)))
        df_funnel = pd.merge(df_sent, df_opened.drop(columns=['campaign', 'subject_id']), on=['iduser', 'email_id'], how='left')
        df_funnel = pd.merge(df_funnel, df_clicked, on=['iduser', 'email_id'], how='left')
        print('Length after joining: ' + str(len(df_funnel)))
        return df_funnel
    except:
        print('Error building funnel!')

def build_master(df_funnel, drop_cols):
    '''Builds raw master table for analysis'''
    print('Building master table...')

    try:
        df_master = df_funnel.copy()
        df_master['opened_mail'] = (~df_master['opened_timestamp'].isna())
        df_master['clicked_mail'] = (~df_master['num_clicks'].isna())
        df_master = df_master.drop(drop_cols, axis=1)
        print('Length master df: ' + str(len(df_master)))
        return df_master

    except:
        print('Error builing master table!')

def preprocess_master(df_master, values_num_dict={}, values_bool_dict={}):
    '''
    Preprocess master table, ready to be analized
    @df_master: Master df to be preprocessed
    @values_num_dict: Dictionary with all numeric values to be replaced (NaNs)
    @values_bool_dict: Dictionary with all boolean values to be replaced (NaNs)
    '''
    print('Preprocessing master table...')

    try:
        # Replace all NaN elements in columns with its respective value.
        # Numerical
        if any(values_num_dict) == True:
            df_master = df_master.fillna(value=values_num_dict)
        # Categorical
        if any(values_bool_dict) == True:
            df_master = df_master.fillna(value=values_bool_dict)

        return df_master

    except:
        print('Error preprocessing master df!')

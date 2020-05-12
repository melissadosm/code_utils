query_sendgrid_events = '''
select * from (
    select (select value from unnest(properties) where key = 'id_user') as iduser, 
      eventname, 
      (select value from unnest(properties) where key = 'campaign') as campaign, 
      (select value from unnest(properties) where key = 'email_id') as email_id,
      (select value from unnest(properties) where key = 'subject_id') as subject_id,
      timestamp
    from `merlin_events.Event`
    where eventName in ('email-open', 'email-bounce', 'email-dropped', 'email-group_unsubscribe', 'email-spamreport', 'email-unsubscribe')
    and timestamp >= '2020-03-27'
    and (select value from unnest(properties) where key = 'email_id') is not null
    and (select value from unnest(properties) where key = 'email_id') != ''
    and (select value from unnest(properties) where key = 'email_template') = 'CANDIDATE_THIRD_PARTY_JOBS'
)
where iduser in (select iduser from data_warehouse_views.dw_approved_candidates)

'''

query_sent_events = '''
select * except(r) 
from (
  select *, 
    row_number() over(partition by iduser, campaign, ziprecruiter_job_id_array order by timestamp) as r
  from (  
    select distinct iduser, 
      (select value from unnest(properties) where key = 'campaign') as campaign,
      (select value from unnest(properties) where key = 'email_id') as email_id,
      (select value from unnest(properties) where key = 'subject_id') as subject_id,
      (select value from unnest(properties) where key = 'ziprecruiter_job_id_array') as ziprecruiter_job_id_array,
      timestamp
    from `merlin_events.Event`
    where eventName = 'email_send_redirection_jobs'
    and (select value from unnest(properties) where key = 'email_id') is not null
    and timestamp >= '2020-03-27'
  )  
)
where r=1
and iduser in (select iduser from data_warehouse_views.dw_approved_candidates)
'''

query_clicked_events = '''
select * from (
    select (select value from unnest(properties) where key = 'candidate_id') as iduser, 
      (select value from unnest(properties) where key = 'campaign') as campaign,
      (select value from unnest(properties) where key = 'email_id') as email_id,
      (select value from unnest(properties) where key = 'subject_id') as subject_id,
      (select value from unnest(properties) where key = 'ziprecruiter_job_id') as ziprecruiter_job_id,
      timestamp
    from `merlin_events.Event`
    where screenName = 'redirection_external_jobs'
    and eventName = 'info_external_jobs'
    and timestamp >= '2020-03-27'
    and (select value from unnest(properties) where key = 'email_id') is not null
)    
where iduser in (select iduser from data_warehouse_views.dw_approved_candidates)
'''

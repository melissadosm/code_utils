from __future__ import print_function, absolute_import
import logging

import apache_beam as beam


def track_events():
    import ujson
    from uuid import uuid4
    from conf import conf
    from settings.settings import keys, appsflier_fields, events_schema, send_event_schema
    from utils.functions import validate_version, set_properties, validate_appsflyer, send_appsflyer_event
    from utils.redis_client import RedisClient

    project = conf.PROJECT
    redis_client = RedisClient()

    def transform(message):
        event = ujson.loads(message)
        # if event.get("platform") in ("Android", "iOS"):
        #     appsflyer_version = validate_version(event.get("appVersion"), keys.get("appsflyer_version_{}".
        #                                                                            format(event.get("platform"))))
        # else:
        #     appsflyer_version = False

        # event["send_appsflyer"] = validate_appsflyer(event, keys.get("appsflyer_events"), appsflyer_version)
        event["send_appsflyer"] = False
        return [event]

    def send_appsflyer(event):
        event_af = ujson.loads(ujson.dumps(event))
        if (not event_af.get("send_appsflyer")) or project == "merlin-qa":
            return []

        try:
            send_appsflyer_event(event_af, appsflier_fields)
            return [{"type": "apps", "idEvent": event_af.get("idEvent"), "createdAt": "{:%Y-%m-%d %H:%M:%S.%f}"
                .format(datetime.now()), "sent": True}]
        except Exception as ex:
            logging.error(ex.message)
            return [{"type": "apps", "idEvent": event_af.get("idEvent"), "createdAt": "{:%Y-%m-%d %H:%M:%S.%f}"
                .format(datetime.now()), "sent": False, "error": ex.message}]

    from datetime import datetime

    def transform_bigquery(event):
        from google.cloud import datastore

        event_bq = ujson.loads(ujson.dumps(event))
        event_bq = set_properties(event_bq)
        if "idJob" in event_bq:
            try:
                job_key = datastore.Key.from_legacy_urlsafe(urlsafe=event_bq.get("idJob"))
                event_bq["idJob"] = job_key.name
            except Exception:
                pass
        event_bq.pop("appsflyer", None)
        event_bq.pop("send_appsflyer", None)
        return [event_bq]

    def select_table(bq_event):
        if bq_event.get("eventName") not in keys.get("expensive_events"):
            return [bq_event]
        return []

    def select_table_expensive(bq_event):
        if bq_event.get("eventName") in keys.get("expensive_events"):
            return [bq_event]
        return []

    # Define pipeline
    storage_bucket = "gs://{}/dataflow".format(conf.BUCKET_NAME)
    pipeline = beam.Pipeline(runner=conf.RUNNER, argv=[
        "--project", project,
        "--subnetwork", "regions/us-central1/subnetworks/default",
        "--staging_location", "{}/staging_location".format(storage_bucket),
        "--temp_location", "{}/temp".format(storage_bucket),
        "--output", "{}/output".format(storage_bucket),
        "--setup_file", "./setup.py",
        "--job_name", "events-sync-{}".format(str(uuid4())),
        "--batch",
        "--worker_machine_type", "n1-standard-2"
    ])

    # PTransforms
    # Read from pubsub
    events = pipeline | "Read pubsub messages" >> beam.Create(redis_client.receive_messages())
    events = events | "Transform message" >> beam.FlatMap(lambda message: transform(message))
    # Send event to appsflyer
    # apps_events = events | "Send to appsflyer" >> beam.FlatMap(lambda event: send_appsflyer(event))
    bigquery_events = events | "Transform to bigquery" >> beam.FlatMap(lambda event: transform_bigquery(event))
    bigquery_events_normal = bigquery_events | "Select event to bigquery" >> beam.FlatMap(
        lambda event: select_table(event))
    bigquery_events_expensive = bigquery_events | "Select event expensive to bigquery" >> beam.FlatMap(
        lambda event: select_table_expensive(event))

    from apache_beam.io.gcp.bigquery import parse_table_schema_from_json
    bigquery_events_schema = parse_table_schema_from_json(ujson.dumps(events_schema))
    bigquery_path = "{}:merlin_events.Event".format(project)
    bigquery_events_normal | "Write events on bigquery" >> beam.io.WriteToBigQuery(
        bigquery_path,
        schema=bigquery_events_schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    )

    bigquery_path = "{}:merlin_events.Event_expensive".format(project)
    bigquery_events_expensive | "Write events expensive on bigquery" >> beam.io.WriteToBigQuery(
        bigquery_path,
        schema=bigquery_events_schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    )

    bigquery_events_schema = parse_table_schema_from_json(ujson.dumps(send_event_schema))
    bigquery_path = "{}:merlin_events.SendEvent".format(project)
    # apps_events | "Write sent apps events on bigquery" >> beam.io.WriteToBigQuery(
    #     bigquery_path,
    #     schema=bigquery_events_schema,
    #     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    #     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    # )
    result = pipeline.run()
    if conf.ENV == "LOCAL":
        result.wait_until_finish()

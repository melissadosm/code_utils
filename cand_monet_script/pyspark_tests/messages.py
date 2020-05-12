import json
import requests
from datetime import date

# Set the webhook_url to the one provided by Slack when you create the webhook
# at https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/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'
day = date.today()

def post_message_to_slack(webhook_url, text_intro, date, text_2=None, blocks=False):
    """
    post_message_to_slack

    Returns messages to desired slack channel.

    Requires,
    webhook_url: Webhook_url to the one provided by Slack when you create the
        webhook at https://my.slack.com/services/new/incoming-webhook/
    """
    slack_data = {"text" : text_intro,
        "blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text_intro
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text_2
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "Last updated: {}".format(date)
				}
			]
		}
	] if blocks else None
    }
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

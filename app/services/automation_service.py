import requests

def trigger_workflow(data):

    webhook = "https://your-n8n-webhook-url"

    try:
        requests.post(webhook, json=data)
    except:
        pass
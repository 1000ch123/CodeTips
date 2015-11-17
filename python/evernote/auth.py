# -*- coding: utf-8 -*-
from evernote.api.client import EvernoteClient

client = EvernoteClient(
    consumer_key='1000-ch',
    consumer_secret='64f4a5313d5dac51',
    sandbox=True
    )
request_token = client.get_request_token('YOUR CALLBACK URL')
client.get_authorize_url(request_token)

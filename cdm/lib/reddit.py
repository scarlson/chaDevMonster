# -*- coding: utf-8 -*-

import requests
import requests.auth
import json
from cdm import config

class Reddit(object):
    """Interact with reddit."""

    def __init__(self, *args, **kwargs):
        self.config()

    def config(self):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.username = config.REDDIT_USERNAME
        self.password = config.REDDIT_PASSWORD
        self.user_pass_dict = {'user': self.username,
                               'passwd': self.password,
                               'api_type': 'json', }

    def submit_link(self, title, link):
        access_token = self.get_access_token()
        post_data = {
            'url': link,
            'text': title,
            'kind': 'link',
            'sr': 'chadev',
            'title': 'Daily Inspiration: %s' % (title),
            'r': 'chadev',
            'api_type': 'json'
        }

        headers = {"Authorization": "bearer %s" % (access_token), "User-Agent": "chaDevMonster"}
        response = requests.post("https://oauth.reddit.com/api/submit/.json", headers=headers, data=post_data)
        if response.status_code == 200:
            return True
        else:
            return False

    def get_access_token(self):
        """Get the access token from reddit."""
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = {"grant_type": "password", "username": self.username, "password": self.password}
        headers = {'User-Agent': 'chaDevMonster', 'Content-Type': "application/x-www-form-urlencoded"}
        client = requests.session()
        client.headers = headers
        response = client.post(
            "https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data)

        if response.status_code == 200:
            token_json = response.json()
            access_token = token_json['access_token']
            return access_token
        else:
            return None

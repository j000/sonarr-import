import json
import requests


class Config:
    def __init__(self, config_path):
        with open(config_path, "r") as file:
            config = json.load(file)
        self.api_key = config['api_key']
        self.url = config['sonarr_url']
        self.quality = config['quality']


class Wrapper:
    def __init__(self, config_path):
        self.config = Config(config_path)
        self.rootfolder = self.get_root()
        self.quality = self.get_qualities()

    def get(self, url, *, params=None):
        headers = {'X-Api-Key': self.config.api_key}
        return requests.get(
            self.config.url + url,
            headers=headers,
            params=params)

    def post(self, url, *, payload=None, json=None):
        headers = {"X-Api-Key": self.config.api_key}
        return requests.post(
            self.config.url + url,
            headers=headers,
            data=payload,
            json=json)

    def get_root(self):
        rootfolders = self.get('/api/v3/rootfolder').json()
        return rootfolders[0]['path']

    def get_qualities(self):
        qualities = self.get('/api/v3/qualityprofile').json()
        return next(
            filter(
                lambda x: x['name'] == self.config.quality,
                qualities
            ),
            qualities[0]
        )['id']

    def add_series(self, tvdbid, *, rootfolder=None, quality=None):
        if rootfolder is None:
            rootfolder = self.rootfolder
        if quality is None:
            quality = self.quality
        data = [{
            'tvdbId': tvdbid,
            'rootFolderPath': rootfolder,
            'qualityProfileId': quality,
            'monitored': False,
            'addOptions': {
                'searchForMissingEpisodes': False,
                'searchForCutoffUnmetEpisodes': False,
            }
        }]
        return self.post('/api/v3/series/import', json=data)

    def search(self, term):
        return self.get('/api/v3/series/lookup', params={'term': term}).json()

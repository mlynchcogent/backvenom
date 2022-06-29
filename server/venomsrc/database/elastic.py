#!/usr/bin/env python3

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime
from tenacity import retry
from time import sleep
import json
import requests
import uuid
import os

class ElasticHandler:
    """
    Elasticsearch database handler class
    """
    def __init__(self):
        self.es = Elasticsearch("http://127.0.0.1:9200", http_auth=('elastic', os.environ["ELASTICSEARCH_PASSWORD"]))

        for index in ["listener", "agent"]:
            if not self.es.indices.exists(index=index):
                self.es.indices.create(index=index, ignore=400)

        with open('venomsrc/database/index.json', 'r') as f:
            dashboard = json.load(f)

        self.set_dashboard(dashboard)  # load dashboard into kibana

    @retry
    def set_dashboard(self, dashboard: dict):
        requests.post("https://127.0.0.1:5601/api/kibana/dashboards/import?exclude=index-pattern&force=true", headers={"kbn-xsrf": "reporting"}, json=dashboard,
                      verify=False)  # Add backvenom dashbaord to kibana
        sleep(1)

    def bulk_json_data(self, doc: list, index: str) -> str:
        """
        Returns the json to index with useful properties, also used yield due helpers.bulk
        @return: indexable json
        """
        doc["_index"] = index
        doc["_id"] = uuid.uuid4()
        doc["@timestamp"] = datetime.now()
        yield doc

    def bulkDB(self, json: str, index: str) -> None:
        """
        Index document to elasticsearch
        """
        helpers.bulk(self.es, self.bulk_json_data(json, index))

    def indexListerner(self, json) -> int:
        """
        Index listener to BBDD index
        """
        self.bulkDB(json, "listener")
        return json["_id"]

    def removeListener(self, listener: object) -> None:
        """
        Removes listener from BBDD index
        """
        self.es.delete(index="listener", id=listener.uuid)

    def indexAgent(self) -> None:
        """
        Index Agent to elasticsearch
        """
        self.bulkDB(json, "agent")

    def removeAgent(self, id: int) -> None:
        """
        Removes agent from BBDD index
        """
        self.es.delete(index="agent", id=id)

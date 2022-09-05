# -*- coding: utf-8 -*-

"""Zenodo _Licenses class

"""

import requests
from entities.record import Record
from entities.metadata import records_search_headers
from errors import zenodo_error
import logging

logger = logging.getLogger(__name__)


class _Licenses(object):
    """Licenses class provides APIs for searching licenses on Zenodo servers and
    is used for serving the license metadata that can be applied to uploaded content
    on Zenodo."""

    def __init__(self, client):
        self._client = client
        self._base_licenses_url = self._client._base_url + "/licenses/"
        self._params = self._client._params

    def list_licenses(
        self,
        query: str = None,
        page: int = None,
        size: int = None,
    ) -> list[Record]:
        """List all licenses matching the (elastic) search query statement.
        For further details see https://help.zenodo.org/guides/search/"""
        tmp_params = self._params.copy()
        keys_list = ["query", "page", "size"]
        values_list = [query, page, size]
        for key, value in zip(keys_list, values_list):
            if value is not None:
                tmp_params[key] = value

        tmp_url = self._base_licenses_url.strip().rstrip("/")
        response = requests.get(url=tmp_url, params=tmp_params)
        status_code = response.status_code
        if status_code != 200:
            zenodo_error(status_code)
        search_result = response.json()
        search_result_list = search_result["hits"]["hits"]
        records_list = []
        if isinstance(search_result_list, list) and search_result_list != []:
            for record in search_result_list:
                records_list.append(Record(self._client, record=record))
            return records_list
        else:
            return search_result

    def retrieve_license(self, id_: str = None) -> Record:
        """Retrieve a single license resource"""
        if id_ is not None and id_ != "":
            tmp_url = self._base_licenses_url + str(id_)
            return Record(self._client, id_=None, url=tmp_url, record=None)
        else:
            raise ValueError(
                "The license ID is None or empty.\n" "Please use a valid license ID.\n"
            )

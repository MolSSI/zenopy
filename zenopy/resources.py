# -*- coding: utf-8 -*-

"""Zenodo _Resources class

"""

import requests
import logging
from zenopy.record import Record
from zenopy.errors import zenodo_error

logger = logging.getLogger(__name__)


class _Resources(object):
    """Licenses class provides APIs for searching licenses on Zenodo servers and
    is used for serving the license metadata that can be applied to uploaded content
    on Zenodo."""

    def __init__(self, client, resource: str = None):
        self._client = client
        valid_resources = ["communities", "licenses", "grants", "funders"]
        if resource is not None and resource != "":
            if resource in valid_resources:
                self._base_resources_url = self._client._base_url + f"/{resource}/"
            else:
                raise ValueError(
                    f"The requested resource ({resource}) is not valid.\n"
                    f"Possible values are: {valid_resources}\n"
                )
        else:
            raise ValueError(
                "The value of the 'resource' argument cannot be None or empty.\n"
                f"Possible values are: {valid_resources}\n"
            )
        self._params = self._client._params

    def list_resources(
        self,
        query: str = None,
        page: int = None,
        size: int = None,
    ) -> list[Record]:
        """List all record/deposition resources (licenses, grants, funders
        and communities) matching the (elastic) search query statement.
        For further details see https://help.zenodo.org/guides/search"""
        tmp_params = self._params.copy()
        keys_list = ["q", "page", "size"]
        values_list = [query, page, size]
        for key, value in zip(keys_list, values_list):
            if value is not None:
                tmp_params[key] = value

        tmp_url = self._base_resources_url.strip().rstrip("/")
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

    def retrieve_resource(self, id_: str = None) -> Record:
        """Retrieve a single resource"""
        if id_ is not None and id_ != "":
            tmp_url = self._base_resources_url + str(id_)
            return Record(self._client, id_=None, url=tmp_url, record=None)
        else:
            raise ValueError(
                "The license ID is None or empty.\n" "Please use a valid license ID.\n"
            )

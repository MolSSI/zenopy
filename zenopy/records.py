# -*- coding: utf-8 -*-

"""Zenodo _Records class

"""

import requests
import json
from typing import Any
from zenopy.record import Record
from zenopy.metadata import records_search_headers
from zenopy.errors import zenodo_error
import logging

logger = logging.getLogger(__name__)


class _Records:
    """Records class offers search capabilities for published records
    on Zenodo."""

    def __init__(self, client):
        self._client = client
        self._base_records_url = self._client._base_url + "/records/"
        self._params = self._client._params
        self._headers = self._client._headers

    def list_records(
        self,
        content_type: str = None,
        query: Any = None,
        status: str = None,
        sort: str = None,
        page: int = None,
        size: int = None,
        all_versions: (int | bool) = False,
        communities: str = None,
        type_: str = None,
        subtype: str = None,
        bounds: str = None,
        custom: str = None,
    ) -> list[Record]:
        """List all published open access records matching the
        (elastic) search query statement. For further details
        see https://help.zenodo.org/guides/search/"""
        tmp_params = self._params.copy()
        if content_type is not None and content_type != "":
            if content_type in records_search_headers.keys():
                self._headers["Content-Type"] = records_search_headers[content_type]
            else:
                raise ValueError(
                    f"Invalid 'content_type' argument value ({content_type}).\n"
                    "The following values are allowed for the content_type argument:\n"
                    f"{json.dumps(list(records_search_headers.keys()), indent=4)}\n"
                )
        else:
            logger.warning(
                "The value of 'content_type' argument is None.\n"
                "ZenoPy will adopt JSON encoding.\n"
            )
            self._headers["Content-Type"] = records_search_headers["json"]
        if status is not None:
            if status in ["draft", "published"]:
                tmp_params["status"] = status
            else:
                raise ValueError(
                    f"Invalid status argument value ({status}).\n"
                    "The status argument can either be 'draft' or 'published'.\n"
                )
        else:
            logger.warning(
                "The value of 'status' argument is None.\n"
                "ZenoPy will search for 'published' record.\n"
            )
        if sort is not None:
            if sort in ["bestmatch", "mostrecent", "-mostrecent"]:
                tmp_params["sort"] = sort
            else:
                raise ValueError(
                    f"Invalid sort argument value ({sort}).\n"
                    "The sort argument can either be 'bestmatch', "
                    "'mostrecent' (ascending), '-mostrecent' (descending).\n"
                )
        else:
            logger.warning(
                "The value of 'sort' argument is None.\n"
                "ZenoPy will sort the search results according to 'bestmatch' sort option.\n"
            )
        if all_versions is not None and all_versions in [0, 1, False, True]:
            tmp_params["all_versions"] = all_versions
        keys_list = [
            "q",
            "page",
            "size",
            "communities",
            "type",
            "subtype",
            "bounds",
            "custom",
        ]
        values_list = [query, page, size, communities, type_, subtype, bounds, custom]
        for key, value in zip(keys_list, values_list):
            if value is not None:
                tmp_params[key] = value

        tmp_url = self._base_records_url.strip().rstrip("/")
        response = requests.get(url=tmp_url, params=tmp_params, headers=self._headers)
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

    def retrieve_record(self, id_: int = None) -> Record:
        """Retrieve a single record."""
        if id_ is not None and isinstance(id_, int):
            return Record(self._client, id_=id_, url=None, record=None)
        else:
            raise ValueError("The record ID cannot be None and must be an integer.")

# -*- coding: utf-8 -*-

"""Zenodo Utility Modules

"""


@staticmethod
def disable_method(msg: str = None):
    if msg is not None and msg != "":
        if isinstance(msg, str):
            raise AttributeError(msg)
        else:
            raise TypeError("The message argument should be of string type.")
    else:
        raise RuntimeError(
            "The error message in the 'disable_method()' cannot be empty or None."
        )


def search(
    self,
    authors=None,
    query="",
    communities=None,
    keywords=None,
    title=None,
    description=None,
    all_versions=False,
    size=25,
    page=1,
):
    """Search for records in Zenodo."""
    url = self.base_url + "/records/"
    payload = {
        "size": size,
        "page": page,
    }
    if all_versions:
        payload["all_versions"] = 1
    if communities is not None:
        for community in communities:
            query += f' AND +communities:"{community}"'
    if keywords is not None:
        for keyword in keywords:
            query += f' AND +keywords:"{keyword}"'
    payload["q"] = query
    logger.debug("Payload for query request:\n" + pprint.pformat(payload))
    try:
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
    except Exception:
        response = requests.get(url, params=payload)
    else:
        response = requests.get(url, headers=headers, params=payload)
    if response.status_code != 200:
        raise RuntimeError(
            f"Error in search: code = {response.status_code}"
            f"\n\n{pprint.pformat(response.json())}"
        )
    result = response.json()
    records = []
    if "hits" in result:
        hits = result["hits"]
        n_hits = hits["total"]
        logger.debug(f"{n_hits=}")
        for record in hits["hits"]:
            records.append(Record(record, None))
        for record in records:
            logger.debug(f"\t{record['id']}: {record['metadata']['title']}")
    else:
        logger.debug("Query returned no hits!")
    return n_hits, records

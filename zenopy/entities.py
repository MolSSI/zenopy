    def add_version(self, _id):
        """Create a new record object for uploading a new version to Zenodo."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        url = self.base_url + f"/deposit/depositions/{_id}/actions/newversion"
        response = requests.post(url, headers=headers)

        if response.status_code != 201:
            raise RuntimeError(
                f"Error in add_version: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        # The result is for the original DOI, so get the data for the new one
        url = result["links"]["latest_draft"]
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in add_version get latest draft: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, self.token)

    def create_record(self):
        """Create a new record object for uploading to Zenodo."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        url = self.base_url + "/deposit/depositions"
        response = requests.post(url, json={}, headers=headers)

        if response.status_code != 201:
            raise RuntimeError(
                f"Error in create_record: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, self.token)

    def get_deposit_record(self, _id):
        """Get an existing deposit record object from Zenodo."""
        url = self.base_url + f"/deposit/depositions/{_id}"
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        except Exception:
            token = None
            response = requests.get(url, json={})
        else:
            token = self.token
            response = requests.get(url, json={}, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in get_deposit_record: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, token)

    def get_record(self, _id):
        """Get an existing record object from Zenodo."""
        url = self.base_url + f"/api/records/{_id}"
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        except Exception:
            response = requests.get(url, json={})
        else:
            response = requests.get(url, json={}, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Error in get_record: code = {response.status_code}"
                f"\n\n{pprint.pformat(response.json())}"
            )

        result = response.json()

        return Record(result, None)

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
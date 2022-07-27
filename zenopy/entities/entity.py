# -*- coding: utf-8 -*-

"""Zenodo Entity class

"""
import logging
from client import Zenodo

logger = logging.getLogger(__name__)

class Entity(Zenodo):
    def __init__(self):
        Zenodo.__init__(self)
        self._data = {}
        self._metadata = {}
        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self._params = {}
        self._params["access_token"] = self.token
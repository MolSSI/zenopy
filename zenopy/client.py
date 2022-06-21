# -*- coding: utf-8 -*-

"""Zenodo client objects for credentials management

"""

import configparser
import logging
from pathlib import Path
import pprint

logger = logging.getLogger(__name__)

class Zenodo(object):
    def __init__(self, token=None, config_path="~/.zenodorc", use_sandbox=False):
        self._token = token
        self.config_path = config_path
        self.config = self.fetch_config(self.config_path)
        # setting the default section to MOLSSI
        # self.config.default_section = "MOLSSI"
        self.use_sandbox = use_sandbox
        if use_sandbox:
            self.base_url = "https://sandbox.zenodo.org/api"
        else:
            self.base_url = "https://zenodo.org/api"

    @property
    def token(self):
        """Getter for the Zenodo class token attribute."""
        return self._token

    @token.setter
    def token(self, token):
        """Setter for the Zenodo class token attribute."""
        self._token = token

    def fetch_config(self, file_path=None):
        """Returns the configfile"""
        path = Path(file_path).expanduser()
        if not path.exists():
            raise RuntimeError(
                f"You need a config file to publish to Zenodo. "
                "See the documentation for more details."
            )
        config = configparser.ConfigParser()
        config.read(path)    
        return config

    def list_sections(self):
        """List all sections in a config file"""
        return [sec for sec, _ in self.config.items()]

    def list_tokens(self, section=None):
        """List all tokens in a specific section"""
        if section is None:
            raise configparser.NoSectionError(
                f"A section name is needed as an argument."
            )
        section = section.upper()

        if section not in self.config.sections():
            raise configparser.NoSectionError(
                f"There is no [{section}] section in {self.config_path}."
            )
        return list(self.config[section].items())

    def read_token(self, key=None):
        """Setting the appropriate token for Zenodo."""
        if key is None:
            raise configparser.NoOptionError(
                f"A token name is needed as an argument."
            )
        if self.use_sandbox:
            section = "SANDBOX"
        else:
            section = "ZENODO"
        if section not in self.config.sections():
            raise configparser.NoSectionError(
                f"There is no [{section}] section in {self.config_path}."
            )
        if key not in self.config[section]:
            raise configparser.NoOptionError(
                f"The requested token key ({key}) does not exist "
                f"in [{section}] section."
            )
        self._token = self.config[section][key]

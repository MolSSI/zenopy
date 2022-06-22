# -*- coding: utf-8 -*-

"""Zenodo client objects for credentials management

"""

import configparser
import logging
from pathlib import Path
import pprint

logger = logging.getLogger(__name__)

class Zenodo(object):
    def __init__(self, token=None, config_path=None, use_sandbox=False):
        self._token = token
        self._config_path = config_path
        if self._token is None and (self._config_path is None or self._config_path == ""):
            self._config_path = "~/.zenodorc"
            if not Path(self._config_path).expanduser().exists():
                logger.warning(
                    "Both token and config_path arguments are None.\n"
                    f"Creating a config_file in {self._config_path}."
                )
                self.create_config_file(self._config_path)
        self._config_file = self.read_config_file(self._config_path)
        self._use_sandbox = use_sandbox
        if self._use_sandbox:
            self.base_url = "https://sandbox.zenodo.org/api"
        else:
            self.base_url = "https://zenodo.org/api"

    @property
    def config_file(self):
        return self._config_file
    
    @config_file.setter
    def config_file(self, cfg_file):
        self._config_file = cfg_file

    @property
    def token(self):
        """Getter for the Zenodo class token attribute."""
        return self._token

    @token.setter
    def token(self, token):
        """Setter for the Zenodo class token attribute."""
        self._token = token
    
    @property
    def use_sandbox():
        return self._use_sandbox

    def create_config_file(self, config_path=None):
        """Creates an empty config_file in file_path"""
        if config_path is None or config_path == "":
            raise RuntimeError(
                "The file_path argument is None or empty. "
                "Please provide a valid address for a config_file."
            )
        path = Path(config_path).expanduser()
        if not path.exists():
            config_file = configparser.ConfigParser()
            config_file["ZENODO"]  = {}
            config_file["SANDBOX"] = {}
            with open(path, 'w') as cfg_obj:
                config_file.write(cfg_obj)

    def read_config_file(self, config_path=None):
        """Returns the configfile"""
        if config_path is None:
            raise RuntimeError(
                "The file_path argument is None. "
                "Please provide a valid address for a config_file."
            )
        path = Path(config_path).expanduser()
        if not path.exists():
            raise RuntimeError(
                f"You need a config file to publish to Zenodo. "
                "See the documentation for more details."
            )
        config_file = configparser.ConfigParser()
        config_file.read(path)    
        return config_file

    def list_sections(self):
        """List all sections in a config file"""
        return [sec for sec, _ in self.config_file.items()]

    def list_tokens(self, section=None):
        """List all tokens in a specific section"""
        if section is None:
            raise configparser.NoSectionError(
                f"A section name is needed as an argument."
            )
        section = section.upper()
        if section not in self.config_file.sections():
            raise configparser.NoSectionError(
                f"There is no [{section}] section in {self._config_path}."
            )
        return list(self.config_file[section].items())

    def write_token(self, section=None, key=None, token=None, force_rewrite=False):
        """Setting the appropriate token within a specific section."""
        if key is None:
            raise configparser.NoOptionError(
                f"A token name is needed as an argument."
            )
        section = section.upper()
        if not self._config_file.has_section(section):
            raise configparser.NoSectionError(
                f"Section [{section}] does not exist in {self._config_path}."
            )
        if self._config_file.has_option(section, key):
            if force_rewrite:
                logger.warning(
                    f"Rewriting the existing token key ({key}) "
                    f"in section [{section}]..."
                )
        self._config_file.set(section, key, token)

    def read_token(self, section=None, key=None):
        """Reading a specific token from a selected section."""
        # Raises the configparser.NoSectionError/NoOptionError 
        # if the section/key does not exist in the config_file
        return self._config_file.get(section, key)
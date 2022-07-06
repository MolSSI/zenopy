# -*- coding: utf-8 -*-

"""Zenodo client objects for credentials management

"""

import configparser
import logging
from pathlib import Path
import pprint

logger = logging.getLogger(__name__)

class Zenodo(object):
    def __init__(self, token=None, config_file_path=None, use_sandbox=False):
        self._token = token
        self._config_file_path = config_file_path
        self._use_sandbox = use_sandbox
        if self._use_sandbox:
            self.base_url = "https://sandbox.zenodo.org/api"
        else:
            self.base_url = "https://zenodo.org/api"
        if self._token is None and (self._config_file_path is None or self._config_file_path == ""):
            self._config_file_path = "~/.zenodorc"
            if not Path(self._config_file_path).expanduser().exists():
                logger.warning(
                    "WARNING: Both token and config_file_path arguments are None.\n"
                    f"The {self._config_file_path} does not exist.\n"
                    f"Creating a config_file in {self._config_file_path}."
                )
                self.create_config_file(self._config_file_path)
            else:
                logger.warning(
                    f"WARNING: The config file ({self._config_file_path}) is found."
                )
        self._config_obj = self.read_config_file(self._config_file_path)


    @property
    def config_obj(self):
        return self._config_obj
    
    @config_obj.setter
    def config_file(self, cfg_obj):
        self._config_obj = cfg_obj

    @property
    def token(self):
        """Getter for the Zenodo class token attribute."""
        return self._token

    @token.setter
    def token(self, token):
        """Setter for the Zenodo class token attribute."""
        self._token = token
    
    @property
    def use_sandbox(self):
        return self._use_sandbox
    
    @use_sandbox.setter
    def use_sandbox(self, value):
        self._use_sandbox = value

    def update_config_file(self):
        """Commits the current changes to the state of the 
        self._config_obj object to the config file located
        at self._config_file_path
        """
        path = Path(self._config_file_path).expanduser()
        if path.exists():
            with open(path, 'w') as f:
                self._config_obj.write(f)

    def create_config_file(self, config_file_path=None):
        """Creates an empty config_file in file_path"""
        if config_file_path is None or config_file_path == "":
            raise RuntimeError(
                "The file_path argument is None or empty. "
                "Please provide a valid address for a config_file."
            )
        path = Path(config_file_path).expanduser()
        if not path.exists():
            config_obj = configparser.ConfigParser()
            config_obj["ZENODO"]  = {}
            config_obj["SANDBOX"] = {}
            section =  "SANDBOX" if self._use_sandbox else "ZENODO"
            config_obj[section]["token"] = '<FIXME>'
            with open(path, 'w') as f:
                config_obj.write(f)

    def read_config_file(self, config_file_path=None):
        """Returns the configfile"""
        if config_file_path is None:
            raise RuntimeError(
                "The file_path argument is None. "
                "Please provide a valid address for a config_file."
            )
        path = Path(config_file_path).expanduser()
        if not path.exists():
            raise RuntimeError(
                f"You need a config file to publish to Zenodo. "
                "See the documentation for more details."
            )
        config_obj = configparser.ConfigParser()
        config_obj.read(path)    
        return config_obj

    def list_sections(self):
        """List all sections in a config file"""
        return self.config_file.sections()

    def list_tokens(self, section=None):
        """List all tokens in a specific section"""
        if section is None:
            raise configparser.NoSectionError(
                f"A section name is needed as an argument."
            )
        section = section.upper()
        if section not in self.config_file.sections():
            raise configparser.NoSectionError(
                f"Section [{section}] does not exist in {self._config_file_path}."
            )
        return list(self.config_file[section].items())

    def write_token(self, section=None, key=None, token=None, force_rewrite=False):
        """Setting the appropriate token within a specific section."""
        if key is None:
            raise configparser.NoOptionError(
                f"A token name is needed as an argument."
            )
        section = section.upper()
        if not self._config_obj.has_section(section):
            raise configparser.NoSectionError(
                f"Section [{section}] does not exist in {self._config_file_path}."
            )
        if self._config_obj.has_option(section, key):
            if force_rewrite:
                logger.warning(
                    f"WARNING: Rewriting the existing token key ({key}) "
                    f"in section [{section}]..."
                )
        self._config_obj.set(section, key, token)

    def read_token(self, section=None, key=None):
        """Reading a specific token from a selected section."""
        # Raises the configparser.NoSectionError/NoOptionError 
        # if the section/key does not exist in the config_file
        return self._config_obj.get(section, key)
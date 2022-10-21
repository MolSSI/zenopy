# -*- coding: utf-8 -*-

"""Zenodo client objects for credentials management

"""

import configparser
import logging
from pathlib import Path
from zenopy.deposition_actions import _DepositionActions
from zenopy.deposition_files import _DepositionFiles
from zenopy.depositions import _Depositions
from zenopy.records import _Records
from zenopy.resources import _Resources

logger = logging.getLogger(__name__)


class Zenodo(object):
    """zenopy client class

    The Zenodo client class instance allows the users to connect to
    their accounts on Zenodo server and communicate with it through
    REST APIs.

    Examples
    --------
    >>> import zenopy
    >>> cli = zenopy.Zenodo()
    WARNING: The config file (~/.zenodorc) is found.
    """
    def __init__(
        self,
        token: str = None,
        config_file_path: (str | Path) = None,
        use_sandbox: bool = False,
    ):
        """zenopy client class constructor

        Parameters
        ----------
        token : str, optional
            Token created through a personal Zenodo account, by default None
        config_file_path : str  |  Path, optional
            Path to the configuration file listing tokens for Zenodo 
            (and Sandbox) account(s). This file is usually located at ~/.zenodorc,
            by default None
        use_sandbox : bool, optional
            If True, the tokens will be read from the [SANDBOX] section of the
            configuration file, by default False


        See Also
        --------
        create_config_file
        """
        self._token = token
        self._config_file_path = config_file_path
        self._use_sandbox = use_sandbox
        if self._use_sandbox:
            self._base_url = "https://sandbox.zenodo.org/api"
        else:
            self._base_url = "https://zenodo.org/api"
        if self._token is None and (
            self._config_file_path is None or self._config_file_path == ""
        ):
            self._config_file_path = "~/.zenodorc"
            if not Path(self._config_file_path).expanduser().exists():
                self.create_config_file(self._config_file_path)
            else:
                logger.warning(
                    f"WARNING: The config file ({self._config_file_path}) is found."
                )
        self._config_obj = self.read_config_file(self._config_file_path)
        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self._params = {}
        self._params["access_token"] = self.token

    @property
    def config_obj(self) -> configparser.ConfigParser:
        """Getter for the client's active ConfigParser object

        Returns
        -------
        _config_obj : configparser.ConfigParser
            The client's active ``ConfigParser`` object which stores
            all authentication tokens and credentials in memory.
        """
        if self._config_obj is None:
            return self.read_config_file(self._config_file_path)
        return self._config_obj

    @config_obj.setter
    def config_obj(self, cfg_obj: configparser.ConfigParser) -> None:
        """Setter for the client's active ConfigParser object

        Parameters
        ----------
        cfg_obj : configparser.ConfigParser
            An instance of the ``ConfigParser`` object to be stored in
            client class' corresponding attribute.
        """
        self._config_obj = cfg_obj

    @property
    def token(self) -> str:
        """Getter for the Zenodo class token attribute

        Returns
        -------
        _token : str
            The first token from [ZENODO] (if ``_use_sandbox == False``) 
            or [SANDBOX] (if ``_use_sandbox == True``) sections listed 
            in the configuration file
        """
        if self._token is None or self._token == "":
            section = "SANDBOX" if self._use_sandbox else "ZENODO"
            self._token = self.list_tokens(section)[0][1]
        return self._token

    @token.setter
    def token(self, token: str) -> None:
        """Setter for the Zenodo class token attribute

        Parameters
        ----------
        token : str
            User-defined token to be stored in the ``_token`` attribute
            of the Zenodo client class
        """
        self._token = token

    @property
    def use_sandbox(self) -> bool:
        """Getter for the Zenodo class use_sandbox boolean attribute

        Returns
        -------
        _use_sandbox : str
            Boolean attribute for switching between the SANDBOX and
            ZENODO accounts
        """
        return self._use_sandbox

    @use_sandbox.setter
    def use_sandbox(self, value) -> None:
        """Setter for the Zenodo class use_sandbox attribute

        Parameters
        ----------
        value : str
            True if client should connect to SANDBOX, False
            otherwise.
        """
        self._use_sandbox = value

    def create_config_file(self, config_file_path: str = None) -> None:
        """Creates an empty config file in the `config_file_path`

        Parameters
        ----------
        config_file_path : str, optional
            A valid address for creating the config file, by default None

        Raises
        ------
        RuntimeError
            If the provided ``config_file_path`` is None or an empty string
        configparser.Error
            If a config file does already exist in the target address
            provided by ``config_file_path``
        """        
        """"""
        if config_file_path is None or config_file_path == "":
            raise RuntimeError(
                "The file_path argument is None or empty. "
                "Please provide a valid address for a config file."
            )
        path = Path(config_file_path).expanduser()
        if not path.exists():
            config_obj = configparser.ConfigParser()
            config_obj["ZENODO"] = {}
            config_obj["SANDBOX"] = {}
            section = "SANDBOX" if self._use_sandbox else "ZENODO"
            config_obj[section]["token"] = "<FIXME>"
            with open(path, "w") as f:
                config_obj.write(f)
        else:
            raise configparser.Error(f"A config file already exists in '{path}'.")

    def init_deposition(self):
        """Creates an instance of the _Depositions class

        The returned object exposes all functionalities
        pertinent to the ``_Depositions`` class.
        
        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        >>> depo = cli.init_deposition()
        >>> depo
        <zenopy.depositions._Depositions at 0x7fad2e053790>

        Returns
        -------
        : zenopy.depositions._Depositions
            An instance of the ``zenopy.depositions._Depositions`` class
        """
        return _Depositions(self)

    def init_deposition_actions(self):
        """Creates an instance of the _DepositionActions class

        The returned object exposes all functionalities
        pertinent to the ``_DepositionActions`` class such as
        editing, publishing, creating a new version and discarding
        ongoing changes on the deposition draft.
        
        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        >>> depo_act = cli.init_deposition_actions()
        >>> depo_act
        <zenopy.deposition_actions._DepositionActions at 0x7f2f77742a10>

        Returns
        -------
        : zenopy.deposition_actions._DepositionActions
            An instance of the ``zenopy.deposition_actions._DepositionActions``
            class
        """
        return _DepositionActions(self)

    def init_deposition_file(self):
        """Creates an instance of the _DepositionFiles class

        The returned object exposes all functionalities
        of the ``_DepositionFiles`` class such as creating, listing,
        retrieving, sorting, etc. of files in a deposition draft.
        
        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        >>> depo_file = cli.init_deposition_file()
        >>> depo_file
        <zenopy.deposition_files._DepositionFiles at 0x7fad2e0533a0>

        Returns
        -------
        : zenopy.deposition_files._DepositionFiles
            An instance of the ``zenopy.deposition_files._DepositionFiles``
            class
        """
        return _DepositionFiles(self)

    def init_records(self):
        """Creates an instance of the _Records class

        The returned object exposes all functionalities
        of the ``_Records`` class such as retrieving the records
        and performing elastic search among them.
        
        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        >>> rec_obj = cli.init_records()
        >>> rec_obj
        <zenopy.records._Records at 0x7fb020d5b760>

        Returns
        -------
        : zenopy.depositions._Records
            An instance of the ``zenopy.records._Records`` class
        """
        return _Records(self)

    def init_resources(self, resource: str = None):
        """Creates an instance of the _Resources class

        The returned object provides users with search
        capabilities through the created resources type
        objects. The resource type can be ``communities``,
        ``licenses``, ``grants``, or ``funders``.
        
        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        >>> resrc_obj = cli.init_resources(resource="communities")
        >>> resrc_obj
        <zenopy.resources._Resources at 0x7f51ad3e58d0>

        Returns
        -------
        : zenopy.resources._Resources
            An instance of the ``zenopy.resources._Resources``
            class
        """        
        return _Resources(self, resource=resource)

    def list_sections(self):
        """List all sections in a config file

        Returns
        -------
        _config_obj.sections() : list[str]
            A list of section titles in the instance's active 
            ``_config_obj`` attribute

        Examples
        --------
        >>> import zenopy
        >>> cli = zenopy.Zenodo()
        WARNING: The config file (~/.zenodorc) is found.
        # equivalent to `cli.config_obj.sections()`
        >>> cli.list_sections()
        ['ZENODO', 'SANDBOX']
        """
        return self._config_obj.sections()

    def list_tokens(self, section: str = None) -> list[tuple[str, str]]:
        """List all tokens in a specific section
        
        Lists all tokens in a specific section in the client instance's
        active ``_config_obj`` attribute.

        Returns
        -------
        _config_obj[section].items() : list[tuple[str, str]]
            A list of all available token labels and values
            formatted as doubles (key-value pairs as tuples)

        Raises
        ------
        configparser.NoSectionError
            if the provided argument (section) is None or does not
            exist in the client instance's active ``_config_obj``
            attribute.
        """
        if section is None:
            raise configparser.NoSectionError(
                f"A section name is needed as an argument."
            )
        section = section.upper()
        if section not in self._config_obj.sections():
            raise configparser.NoSectionError(
                f"Section [{section}] does not exist in {self._config_file_path}."
            )
        return list(self._config_obj[section].items())

    def read_config_file(
        self, config_file_path: str = None
    ) -> configparser.ConfigParser:
        """Reads the config file from disk
        
        Reads the config file from a path pointed to by
        the ``config_file_path`` argument and returns a
        ``configparser.ConfigParser`` object constructed from
        it.

        Returns
        -------
        configparser.ConfigParser().read(path) : configparser.ConfigParser
            a ``configparser.ConfigParser`` object the contents of which
            is read from disk
        
        Raises
        ------
        RuntimeError
            If ``config_file_path`` is None or refers to a non-existent config
            file
        """
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

    def read_token(self, section: str = None, key: str = None) -> str:
        """Reading a specific token from a selected section
        
        Raises
        ------
        configparser.NoSectionError
            If the section argument does not exist in the client
            instance's active ``_config_obj`` attribute
        configparser.NoOptionError
            If the key argument does not exist in the client
            instance's active ``_config_obj`` attribute
        
        Notes
        -----
        The ``read_token()`` is case insensitive with respect to the
        entered section argument and automatically turns it to
        upper case.
        """
        section = section.upper()
        return self._config_obj.get(section, key)

    def update_config_file(self) -> None:
        """Commit the current contents of the config object to config file on disk 
        
        Commits the current contents of the client instance's active ``_config_obj`` 
        attribute to the config file located at ``_config_file_path`` on disk.

        Raises
        ------
        configparser.Error
            If the client instance's ``_config_file_path`` points to a non-existent
            config file
        """
        path = Path(self._config_file_path).expanduser()
        if path.exists():
            with open(path, "w") as f:
                self._config_obj.write(f)
        else:
            raise configparser.Error(f"No config file exists in '{path}'.")

    def write_token(
        self,
        section: str = None,
        key: str = None,
        token: str = None,
        force_rewrite: bool = False,
    ) -> None:
        """Setting the appropriate token within a specific section

        Setting the passed token-key pair arguments in the corresponding
        designated config file section.

        Raises
        ------
        configparser.NoSectionError
            If the section argument does not exist in the client
            instance's active ``_config_obj`` attribute
        configparser.NoOptionError
            If the key argument does not exist in the client
            instance's active ``_config_obj`` attribute
        configparser.Error
            If the passed token already exists in the section selected by the user.
        
        Notes
        -----
        Set ``force_rewrite = True`` if you want to overwrite an existing token in 
        a config file section
        """
        if key is None:
            raise configparser.NoOptionError(f"A token name is needed as an argument.")
        section = section.upper()
        if not self._config_obj.has_section(section):
            raise configparser.NoSectionError(
                f"Section [{section}] does not exist in {self._config_file_path}."
            )
        if self._config_obj.has_option(section, key):
            if force_rewrite:
                logger.warning(
                    f"WARNING: Rewriting the existing token ({key}) "
                    f"in section [{section}]..."
                )
                self._config_obj.set(section, key, token)
            else:
                raise configparser.Error(
                    f"The token ({key}) already exists in section [{section}].\n"
                    "Set 'force_rewrite = True' if you want to overwrite the token."
                )
        self._config_obj.set(section, key, token)

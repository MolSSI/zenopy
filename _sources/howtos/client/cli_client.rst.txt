.. _cli_client:

*****************************
How to Create a Client Object
*****************************

Here, we assume you have created a config file on your disk
and stored your Zenodo (Sandbox) token in it as described 
in the :ref:`cli_config` guide.

In order to create a client object, all you need to do is to 
call the client class constructor, ``zenopy.Zenodo()``

>>> cli = zenopy.Zenodo(config_file_path="<config-file-location>", use_sandbox=False)

You should replace the placeholder **<config-file-location>** with the path to 
your config file. If you do not pass in the ``config_file_path`` argument,
``zenopy`` will first check the default path for a config file in your home
directory (**~/.zenodorc**) to see if the config file exists. If not, it will 
create a config file for you.

.. tip::

    By default, ``zenopy`` uses the token from our Zenodo account. You can pass 
    the ``use_sandbox=True`` to the constructor to have the token placeholder in the ``[SANDBOX]``
    section and let the client class know you want to use your Zenodo Sandbox account.

.. seealso::

   - :ref:`cli_config`
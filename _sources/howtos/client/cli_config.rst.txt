.. _cli_config:

**********************************
How to Create a Configuration File
**********************************

A ``zenopy`` config file is a text file that can consist of two sections: 
``[ZENODO]`` and ``[SANDBOX]`` ad looks like the following

.. code-block:: python

    [ZENODO]
    token = <FIXME>

    [SANDBOX]

The former section should be used to store your account token hosted on 
`Zenodo <https://zenodo.org/>`_ and the latter should be adopted to keep 
your `Zenodo Sandbox's <https://sandbox.zenodo.org/>`_ account token.

One way to create a ``zenopy`` config file is to copy and paste 
the above code block into an empty text file and then let the client 
constructor, ``zenopy.Zenodo()``, know where you have stored it

>>> cli = zenopy.Zenodo(config_file_path="<config-file-location>")

You should replace the placeholder **<config-file-location>** with the path to 
your freshly minted config file and the **<FIXME>** placeholder with the 
actual tokens generated from your Zenodo (Sandbox) account(s).

Instead of doing all this work manually, you can also call ``zenopy`` 
client constructor function ``zenopy.Zenodo()`` without passing the 
``config_file_path`` argument.

.. seealso::

   - :ref:`cli_token`
   - :ref:`cli_client`
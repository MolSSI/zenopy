.. _files_howtos:

*********************************
How to Work with Deposition Files
*********************************

This section lays out a list of brief interconnected recipes that allow users
to focus on a specific tasks pertinent to the ``_DepositionFiles`` objects 
in ``zenopy``.

.. toctree::
   :maxdepth: 2
   :titlesonly:
    
   file_list
   file_retrieve
   file_create
   file_sort
   file_delete

All tutorials in this section are based upon the following two steps:

#. Creating a ``zenopy`` client object (see :ref:`here <cli_client>`
   for details)
#. Constructing a ``_DepositionFiles`` object

The first step begins with importing the ``zenopy`` package,

>>> import zenopy

which allows you to call the ``Zenodo()`` constructor
in order to get a handle to the client object 

>>> cli = zenopy.Zenodo()
WARNING: The config file (~/.zenodorc) is found.

A warning will notify you that the ``zenopy`` client is now
connected to your Zenodo account. 

Next, you can now call the client object's ``init_deposition_file()``
function to construct an instance of the ``_DepositionFiles`` class.

>>> depo_file_obj = cli.init_deposition_file()

The **depo_file_obj** object allows you to create, update, list, delete *etc.*
the files in the depositions on your Zenodo account as you will see in more details
in the guidelines list.

.. seealso::

   - :ref:`cli_config`
   - :ref:`cli_client`

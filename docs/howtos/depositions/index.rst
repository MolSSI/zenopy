.. _deposition_howtos:

****************************
How to Work with Depositions
****************************

This section lays out a list of brief interconnected recipes that allow users
to focus on a specific tasks pertinent to the ``_Depositions`` objects 
in ``zenopy``.

.. toctree::
   :maxdepth: 2
   :titlesonly:
    
   depo_list
   depo_retrieve
   depo_create
   depo_update
   depo_delete

For almost all of the tutorials in this section, you will need to start from the
following two steps:

#. Create a ``zenopy`` client object (see :ref:`here <cli_client>`
   for details)
#. Construct a ``_Depositions`` object

The first step begins with importing the ``zenopy`` package,

>>> import zenopy

This enables you to call the ``Zenodo()`` constructor
to get a handle to the client object 

>>> cli = zenopy.Zenodo()
WARNING: The config file (~/.zenodorc) is found.

A warning will notify you that the ``zenopy`` client is now
connected to your Zenodo account. 

Next, you can now call the client object's ``init_deposition()`` function 
to construct an instance of the ``_Depositions`` class.

>>> depo_obj = cli.init_deposition()

The **depo_obj** object allows you to create, update, list, delete *etc.*
the depositions on your Zenodo account as you will see in more details
in the guidelines list.

.. seealso::

   - :ref:`cli_config`
   - :ref:`cli_client`

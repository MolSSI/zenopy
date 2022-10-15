.. _records_howtos:

************************
How to Work with Records
************************

The present section provide a list of guidelines that help users
interact with the ``_Records`` objects in ``zenopy``.

.. toctree::
    :maxdepth: 2
    :titlesonly:
    :glob:
    
    rec_*

For almost all of the tutorials in this section, you will need to start from the
following two steps:

#. Create a ``zenopy`` client object (see :ref:`here <cli_client>`
   for details)
#. Construct a ``_Records`` object

The first step begins with importing the ``zenopy`` package,

>>> import zenopy

This enables you to call the ``Zenodo()`` constructor
to get a handle to the client object 

>>> cli = zenopy.Zenodo()
WARNING: The config file (~/.zenodorc) is found.

A warning will notify you that the ``zenopy`` client is now
connected to your Zenodo account. 

Next, you can now call the client object's ``init_records()`` function 
to construct an instance of the ``_Records`` class.

>>> rec_obj = cli.init_records()
>>> rec_obj
<zenopy.records._Records at 0x7f9f01c50fa0>

The **rec_obj** object allows you to retrieve or search through all
published open access records on Zenodo and list those matching your
`(elastic) search query statement <https://help.zenodo.org/guides/search>`_.
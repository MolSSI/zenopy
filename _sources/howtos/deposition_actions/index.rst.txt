.. _actions_howtos:

***********************************
How to Work with Deposition Actions
***********************************

This section offers a series of guidelines for users
and help them to interact with the ``_DepositionActions`` objects in ``zenopy``

.. toctree::
    :maxdepth: 2
    :titlesonly:
    
    act_edit
    act_discard
    act_newversion
    act_publish

For all tutorials in this section you will need to start from the
following two steps:

#. Create a ``zenopy`` client object (see :ref:`here <cli_client>`
   for details)
#. Construct a ``_DepositionActions`` object

We begin by importing the ``zenopy`` package,

>>> import zenopy

which enables you to call the ``Zenodo()`` constructor
in order to generate an instance of the client class

>>> cli = zenopy.Zenodo()
WARNING: The config file (~/.zenodorc) is found.

A warning will notify you that the ``zenopy`` client is now
connected to your Zenodo account. 

Next, you can now call the client object's ``init_deposition_actions()``
function to construct an instance of the ``_DepositionActions`` class.

>>> depo_act_obj = cli.init_deposition_actions()
>>> depo_act_obj
<zenopy.deposition_actions._DepositionActions at 0x7f738010e500>

The **depo_act_obj** object allows you to perform four types of 
**actions** on your depositions:

- ``edit``: Unlocks a submitted deposition for further modifications
- ``newversion``: Creates a new version of the deposition
- ``publish``: Publishes a deposition
- ``discard``: Discards the changes in the current editing session of the deposition.
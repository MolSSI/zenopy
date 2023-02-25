.. _installation:

************
Installation
************

.. tip::

    Although not necessary, we recommend installing ``zenopy`` and its dependencies
    within an isolated ``virtualenv`` or ``conda`` environment. In order to 
    create a ``conda`` environment with **Python 3.10** (or newer) installed on it,
    run the following command in a terminal

    .. code-block:: bash
        
        conda env create -n <env-name> python=3.10

    where, the **<env-name>** placeholder should be replaced with the desired
    environment name. Upon successful execution, we can activate the environment
    using

    .. code-block:: bash
        
        conda activate <env-name>
    
    Following the remaining part of this instruction will now result in the 
    installation of ``zenopy`` and its dependencies in an isolated ``conda``
    environment.

The easiest way to install ``zenopy`` is through 
`pypi <https://pypi.org/project/zenopy/>`_:

.. code-block:: bash

    pip install zenopy

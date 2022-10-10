.. _installation:

************
Installation
************

Although not necessary, we recommend installing ``zenopy`` within an isolated
``virtualenv`` or ``conda`` environment. Let's create an environment using
``conda`` with Python 3.10 installed on it

.. code-block:: bash
    
    conda env create -n <env-name> python=3.10

Here, the **<env-name>** placeholder should be replaced with the desired
environment name. Then, we can activate the environment using

.. code-block:: bash
    
    conda activate <env-name>

Once the environment is activated, we can install ``zenopy`` in it 
through `pypi <https://pypi.org/project/zenopy/>`_:

.. code-block:: bash

    pip install zenopy

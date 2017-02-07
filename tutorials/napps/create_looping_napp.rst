:tocdepth: 2
:orphan:

.. _tutorial-napps-create-your-own:

############################
How to create a Looping NApp
############################

********
Overview
********

This tutorial covers the basics on how to create a Network Application (NApp)
with a looping for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will learn
====================
* How to Create a NApp with a looping
* How to adjust `settings.py` file to your NApp

What you will need
===================
* How to create a basic NApp - Refer to |Tutorial_01|

************
Introduction
************

Now that you have learned how to build a simple NApp, in this tutorial we will
help you to develop a more complex NApp. Suppose that you need an application
that needs gather some data sporadically from the controller or from the
switches. In this situation is desirable to have a NApp that can run repeatedly
without creating complexes loops. Kytos provides the necessary tools to create
such NApp.

*******************************
Creating your NApp with Looping
*******************************

In this tutorial we will show how to create a NApp that gets the controller
uptime and display it.


settings.py
===========

In order to adjust the pooling frequency, you should set the variable
`STATS_INTERVAL` in seconds. In this example, NApp will get the controller
uptime every fifteen seconds.

.. code-block:: python

    import logging

    # Log Registry Type
    log = logging.getLogger(__name__)

    # Pooling frequency
    STATS_INTERVAL = 15


main.py
=======

Setup
^^^^^

In `main.py` file, we have to adjust the `setup()` method. This adjust tells the
controller that this NApp will run repeatedly.

.. code-block:: python

   def setup(self):
       log.info("Looping NApp Loaded!")
       self.execute_as_loop(settings.STATS_INTERVAL)

Execute
^^^^^^^

In `execute()` method we code what will be execute every fifteen seconds. In
this case, we gather the controller's uptime and print in log file.

.. code-block:: python

   def execute(self):
       log.info("Controller Uptime: %s ", self.Controller.uptime())


Running periodically
~~~~~~~~~~~~~~~~~~~~

Following, the entire NApp's source code of the looping NApp.

.. code-block:: python

    from kyco.core.napps import KycoNApp
    from napps.tutorial.loopingnapp import settings

    log = settings.log

    class Main(KycoNApp):

        def setup(self):
            log.info("Looping NApp Loaded!")
            self.execute_as_loop(settings.STATS_INTERVAL)

        def execute(self):
            log.info("Controller Uptime: %s ", self.Controller.uptime())

        def shutdown(self):
            log.info("Looping NApp Unloaded!")



.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

:tocdepth: 2
:orphan:

.. _tutorial-napps-create-loop:

###################################
How to create your own NApp: Part 2
###################################

********
Overview
********

This tutorial covers the basics on how to create a Network Application (NApp)
with a looping for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will learn
====================
* How to Create a NApp with a loop
* How to adjust `settings.py` file to your NApp

What you will need
===================
* How to create a basic NApp - Refer to |Tutorial_01|_

************
Introduction
************

Now that you have learned how to build a simple NApp, in this tutorial we will
help you to develop a more sophisticated NApp.

Suppose that you need an application
that gather some data sporadically from the controller or from the
switches. In this situation is desirable to have a NApp that can run repeatedly
without creating complexes loops. Kytos provides the necessary tools to create
such NApp.

******************
Creating Loop NApp
******************

In this tutorial we will create a simple NApp, too. This NApp gets the controller
uptime from time to time and display it.

Also we are going to introduce you to the NApps settings, a basic python module
where you can store all variables used by your NApp.

You can create the napp structure manually, but the Kytos project has an
``kytos-utils`` package with few command line utilities that can help you to
create this.

.. NOTE:: Make sure that you had completed your |dev_env|_  setup.

Let's create the structure:

.. code-block:: bash

   $ mkdir ~/tutorial02/
   $ cd ~/tutorial02/
   $ kytos napp init .

.. TODO:: We need to code the kytos napp init. Using jinga2 templates.

.. Template should be inserted here: /etc/skell/kytos/napp-structre/ with the
.. structure and template files.

You will be asked for few questions. Answer them according to your needs, they
are very basic questions like author and napp name.

For this tutorial, when asking for the author and napp name, answer **tutorial**
and **loopnapp**, respectively.

.. TIP:: If you wanna to change the answers on the future, just edit the
   ``kytos.json`` file, and rename the directories if necessary.

Now you have a bootstrap napp struct to work on it.

During this tutorial, the only files that we need to worry about are the
``main.py`` and ``settings.py``.  Open with your preferred editor and let's code.

.. TIP:: ``main.py`` is located inside your napp folder.

settings.py
===========

In order to adjust the pooling frequency, let's define a variable on
`settings.py`. For instance: `STATS_INTERVAL` it will store a number (in
seconds) that we will use it for determine our pooling interval. In this
example, NApp will get the controller uptime every fifteen seconds.

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
       log.info("NApp Loop Loaded!")
       self.execute_as_loop(settings.STATS_INTERVAL)


The method execute_as_loop() is a built in Kytos NApps method that instructs the controller
to execute the method `execute` every x seconds.

If you dont call `execute_as_loop` the `execute` method it will be executed only once,
right after the `setup` method.

Execute
^^^^^^^

In `execute()` method we code what will be execute every fifteen seconds. In
this case, we gather the controller's uptime and print in log file.

.. code-block:: python

   def execute(self):
       uptime = self.controller.uptime()
       log.info("Controller Uptime: {}".format(uptime))


Running Periodically
~~~~~~~~~~~~~~~~~~~~

Following, the entire NApp's source code of the looping NApp.

.. code-block:: python

    from kyco.core.napps import KycoNApp
    from napps.tutorial.loopingnapp import settings

    log = settings.log

    class Main(KycoNApp):

        def setup(self):
            log.info("NApp Loop Loaded!")
            self.execute_as_loop(settings.STATS_INTERVAL)

        def execute(self):
            uptime = self.controller.uptime()
            log.info("Controller Uptime: {}".format(uptime))

        def shutdown(self):
            log.info("NApp Loop Unloaded!")

*****************
Running your NApp
*****************

In order to run your napp, first your have to install it. Again, we are going to
use the ``kytos`` command line from the ``kytos-utils`` package.

.. code-block:: bash

  $ sudo kytos napps install tutorial02/loopnapp

.. NOTE:: This will try to get this napp from your current directory, then
   install it into your system. This napp it will also be enable.

Now, your Napp is ready to be executed.

You can also see if your Napp is installed and enabled, by running the command:

.. code-block:: bash

  $ kytos napps list

For this demo, we don't wanna any other napp running except this created during
this tutorial. So if your setup has multiple napps, please disable them, with
the command:

.. code-block:: bash

  $ kytos napps disable <author_name>/<napp_name>


Yes, we are not running any napp for now, we are disabling everything including
OpenFlow Napps.

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

  $ kytos-kyco start

You will get into the controller terminal, and you can see your NApp output.

.. include:: ../back_to_list.rst


.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |dev_env| replace:: *Development Environment*
.. _dev_env: /general/development_environment_setup

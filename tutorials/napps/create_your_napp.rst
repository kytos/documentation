:tocdepth: 2
:orphan:

.. _tuto-create-your-napp:

###########################
How to create your own NApp
###########################

********
Overview
********
This tutorial covers the basics on how to create your own Netwok Application
(**NApp**) for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: ``XX min``

What you will learn
====================
* How to Create your NApp
* How your NApp comunicate with the Controller
* How to install, test and debug your NApp
* How to publish your NApp

What you will need
===================
* Your |dev_env|_ already setup
* Basic knowledge about |KycoEvents|_

************
Introduction
************
Most of Kytos ecossystem functionalities are delivered by the Network
Applications (NApps). These applications comunicate with the controller, and
between themselves, throught events (KycoEvents), and they can also expose REST
endpoints to the world.

The idea of a NApp is to be as atomic as it can be, solving a small and
specific problem, in a way that NApps can work togheter to solve a bigger
problem, following the |dotdiw|_.

Moreover, you can see the NApps developped by the Kytos Community on our NApps
Server: http://napps.kytos.io.

.. _napp_naming:

Naming your NApp
================
Since your NApp will work as a Python Module, its name must follow the same
naming rules from python modules, defined by
`PEP8 <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_,
which states that:

  Modules should have short, all-lowercase names. Underscores can be used in
  the module name if it improves readability. Python packages should also have
  short, all-lowercase names, although the use of underscores is discouraged.


The namespacing rule for kytos NApps are::
    napps.<author_name>.<napp_name>

This namespace structure allow many authors to develop Network Applications
with the same name.

Understanding the NApp structure
================================
Under the ``<napp_name>`` directory you must have at leasst the following::

    └── of_core
        ├── __init__.py
        ├── kytos.json
        ├── main.py
        ├── README.rst
        └── settings.py

- **README.rst**: Main description and informations about your NApp
- **__init__.py**: Marker to indicate that your NApp is a python module
- **kytos.json**: Attributes used on the |napps_server|_ to distribute your
  NApp
- **main.py**: Main source code of your NApp
- **settings.py**: Main settings parameters of your NApp

.. _readme_description:

README.rst
----------
The content of the *README.rst* file will be shown on your NApp page on the
|napps_server|_ and will be the first contact of kytos community with it. So,
because of that, we recommend you to write at least the following sections:

- **Overview**: A brief description of your NApp, presenting the problem that
  it solves and its main characteristics.
- **Requirements**: If your NApp requires any software that cannot be installed
  by default from Pypi (*pip*), then here is the place to advise your NApp
  users that they need to install it by themselves. If you want to add
  instructions on how to do the needed setup, you can create a section for that
  as well (**Installing** section).

.. NOTE:: Remember that this is a ``.rst`` file, so you can use the ``.rst``
    markup language to stylish your README. See more at:
    http://docs.kytos.io/kytos/utils/rst_cheatsheet/ and at
    http://docs.kytos.io/kytos/utils/rst_quickstart/

.. _kytosjson_desc:

kytos.json
----------
The *kytos.json* file is composed by some mandatory fields:

- **name** ``[string]``: The name of the NApp (according to ":ref:`napp_naming`" rule)
- **long_description** ``[string]``: A more complete description of your NApp (one or two sentenses).
- **description** ``[string]``: A brief description of your NApp
- **version** ``[string]``: The version of your NApp. We recommend you to follow the `Semmantic Versioning <http://semver.org/>`_
- **author** ``[string]``: Your username on the |napps_server|_
- **ofversion** ``[list]``: A list with the versions of the OpenFlow Protocol your NApp support or require.
- **dependencies** ``[list]``: List of NApps that your own NApp require to work. ``"<author>/<napp_name>"``
- **license** ``[string]``: NApp License.
- **git** ``[string]``: The url to git clone your NApp (ending with ``.git``).
- **branch** ``[string]``: The git branch name to be used for your napp.
- **tags** ``[list]``: List of tags for your NApp.

Some of this fields will be used on the |napps_server|_. The ``description``
will be used on all NApps pages that list multiple NApps. The
``long_description`` will be presented under your NApp name on your NApp page.
The ``tags`` will also be used every time your NApp is presented. The
``license`` and the ``git`` repository will also be presented on the NApp page.

The ``git`` and ``branch`` fields will be used by the Controller to look for
and install NApps automatically.

.. _settings_desc:

settings.py
-----------
The *settings.py* file must contain variables and constants that may be changed
by those who are going to use the NApp. So, this is the place to look for while
trying to understand the main configurations of a NApp.

.. NOTE:: For now, our kytos logging system requires you to "manually" init a
    logger. This will be done on the settings.py file.

.. _main_desc:

main.py
-------
This is the main file of our NApp. This is the file that will be loaded by the
|kyco| Controller while loading your NApp.

Here you will define the main structure of your NApp, do a primary setup, if
any is needed, and call other modules you may have built.

The NApp can work with three different behaviors:

- **Active Mode**
    Periodical execution of a specific routine.
- **Reactive Mode**
    A NApp method will be called by the controller when a specific events
    take place at the controller.
- **Rest Mode**
    The NApp define REST API Endpoints on the controller and answer to requests
    made by external agents on that endpoint.

The main module ought to contain a class named ``Main`` that inherits from our
``KycoNapp`` class (``kyco.core.napps.KycoNapp``). This class must implement at
least three methods: ``setup(self)``, ``execute(self)`` and ``shutdown(self)``.
If you are not going to use one of them, you can just ``pass`` it, but you
still need to implement it.

.. WARNING::
    You had better not override the __init__ method on this class or your NApp
    will not work.

The ``setup(self)`` method is a replacement for the ``__init__`` method of the
class. Being so, it will be called during you NApp startup process as the first
execution (after the inherited ``__init__``). If you need any kind of startup
parameters, they must be on the ``settings.py`` file. Here you will import them
and use at your will.

The ``shutdown(self)`` method will be called by the controller when unloading
your NApp.

If you need your NApp to implement the **active mode**, do some periodic
routine, then the ``execute(self)`` method was made for you. Here you will put
the code that need to be runned periodically and, togheter with some settings
during the ``setup`` it will be called regularly. To see how the ``execute``
works on our :ref:`tuto_napp_loop` tutorial.

If you need your NApp to implement the **reactive mode**, on the ``Main`` class
you will write other methods and tell the controller that when a specific event
is dispatched, this method must be called. To see how you can write a method to
listen to an event, go to the :ref:`tuto_napp_listener` tutorial.

At last, your NApp can also define a REST Endpoint on the Kyco REST API. Doing
so, you will be able to exchange data with the outside world, throught both
``POST`` (receive) and ``GET`` (send) methods. To see how this works, see our
:ref:`tuto_napp_rest_api` tutorial.

*************************
Creating your first NApp
*************************
Now that we understand the basic structure of a |kyco|_ NApp, lets start
building our own, the |nn| NApp.

README.rst
==========
Based on what we saw at :ref:`readme_description`, our ``README.md`` will be

.. code-block:: rst

   Overview
   ========
   The *hello_world* NApp prints a welcome message on the controller console
   when it is started and a good bye message when it is stopped. On the
   welcome message there will be the name of the 'network admin', defined on
   the settings.py file. This messages will also be sent to the log system.

   Requirements
   ============
   This NApp does not require non-python softwares.

kytos.json
==========
Based on what we saw at :ref:`kytosjson_desc`, our ``kytos.json`` will be:

.. code-block:: json

   {
     "name": "hello_world",
     "long_description": "This is our Hello World Network Application. It is a basic NApp focused on the understandment of a NApp structure and it print some messages during its startup and shutdown.",
     "description": "This is our Hello World NApp! =).",
     "version": "0.1.0",
     "author": "kytos",
     "ofversion": [],
     "dependencies": [],
     "license": "MIT",
     "git": "https://github.com/kytos/kyco-core-napps.git",
     "branch": "develop",
     "tags": ["hello world", "example"]
   }

Notice that we have not set an ofversion, since our NApp will not deal with any
openflow messages on this tutorial. Also, as we have a very basic napp, there
are no python dependencies as well.

settings.py
===========
As stated on the README.md, our |nn| NApp will print a name defined on the
NApp settings.py. Also, as stated on the note of :ref:`settings_desc`), we also
have to get a Logger for our NApp. Being so, our ``settings.py`` file will be:

.. code-block:: python

   # Importing the python logging module
   import logging

   # Defining our Logger.
   log = logging.getLogger(__name__)

   # Defining our username variable
   username = 'Kytos Team'

main.py
=======

Now lets go to the main code.


.. TODO:: Explore the following ideas

This is the main file of your NApp....

It loads the settings...

Contains the Main class that will be called by the controller to instantiate
and represent your NApp...

.. TODO:: Should we talk about it?

Run as a thread on the controller


This is the main file of our NApp. 


Main Class
----------

.... inherits from the KycoNapp class ....

.... This is the class that the controller will call to start the napp....

.... contains at least three mandatory methods .....

.... to define other methods that will handle specific events see the section
:ref:`listening_to_events`.

Setup and Shutdown
^^^^^^^^^^^^^^^^^^

.. TODO:: Review this section

The ``setup`` and ``shutdown`` methods are executed only once. Although it is
not mandatory to implement them, you must at least declare them with ``pass``,
as we did in the `Running once`_ section.

Before ``execute``, ``setup`` is called. Besides setting the interval between
``execute`` calls (optional, explained in `active_napp`_), you can also
initialize any attribute just as you would in Python constructor
(``__init__``).

.. important::
   Do not override ``__init__``. Instead, use ``setup``.

If we want to run any code just before our napp is finished, it must be
implemented in the ``shutdown`` method.


Execute
^^^^^^^

.. NOTE:: Do not implement an infinite loop here, this method is supposed to be
    runned only once. If you want it to be runned more than once, then see the
    :ref:`active_napp` section below.

.. _reactive_napp:

Reactive NApp behavior
~~~~~~~~~~~~~~~~~~~~~~

.. TODO:: Talk about creating a new method to listen to a specific KycoEvent.

.. _active_napp:

Active NApp behavior (Running periodically)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO:: Explain about the `self.execute_as_loop(settings.POOLING_TIME)`
    option during the `setup()` and that the `execute()` will be runned
    periodically.

Let's say we want to run the ``execute`` method periodically, e.g. every 10
seconds. For that, we must add one line to the ``setup`` method:

.. code-block:: python

   def setup(self):
       self.execute_as_loop(10)  # seconds

With the line above, the ``execute`` method will be called once when our napp
is loaded and again after 10 seconds. This will keep running indefinitely.


REST endpoints
--------------

.. TODO:: Explain how to register an endpoint on the controller, both for
    `POST` and `GET` methods, and explain the 'callback'.

.. TODO:: Talk about the possibility of communication between NApps by REST,
    instead of by KycoEvents?

******************************
Understanding the Kytos Events
******************************

Events Naming Convention
========================

.. TODO:: How should events be named

.. _listening_to_events:

Listening to events
===================

.. TODO:: Talk about our `listen_to` decorator, both when listening to one
    event and more than one event.

Creating and Triggering events
===============================

.. TODO:: How to create a new KycoEvent.

.. TODO:: How to dispatch the created event.

*****************
Napp Installation
*****************

Now lets install our newly created NApp. There are two ways of installing a
NApp.

Development mode
================
Symbolic link from source to the *.installed* directory. .....

Production mode
===============
Source on the *.installed* directory. .....

*****************
Testing your NAPP
*****************

Enabling and Loading your NApp
==============================
.. TODO:: How to enable and start the napp on the controller

.. TODO:: How to manually enable the NApp (symlink)

.. TODO:: How to enable it using the controller `enable_napp()` method.

.. TODO:: How to disable the napp?

.. TODO:: How to **load** the napp on a running Kyco instance?

*******************
Debugging your NApp
*******************
Instead of writing to a file, you can use the standard Python logging module to
see messages in the output of ``controller.start()``. Check below the complete
napp code using log messages.

.. code-block:: python
   :linenos:
   :emphasize-lines: 1, 4, 10, 14

    import logging
    from kyco.core.napps import KycoNApp

    log = logging.getLogger(__name__)

    class Main(KycoNapp):

        def setup(self):
            self.execute_as_loop(10)  # seconds
            log.info('Setup finished.')

        def execute(self):
            nr_switches = len(self.controller.switches)
            log.info('Hello, world of %s switches!', nr_switches)

        def shutdown(self):
            pass

By just adding lines 1 and 4, we can use ``log.info`` (and also ``log.error``,
``log.debug``, etc) to print messages in Kyco's log. The output will be similar
to (some lines were removed for clarity)::

 2016-12-19 15:46:02,322 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller2016-12-19 15:46:02,322 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
 2016-12-19 15:46:02,329 - INFO [my_project/my_napp] (Thread-3) Setup finished.
 2016-12-19 15:46:02,330 - INFO [my_project/my_napp] (Thread-3) Hello, world of 0 switches!
 2016-12-19 15:46:02,562 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...
 2016-12-19 15:46:02,567 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...
 2016-12-19 15:46:12,337 - INFO [my_project/my_napp] (Thread-3) Hello, world of 2 switches!
 2016-12-19 15:46:22,338 - INFO [my_project/my_napp] (Thread-3) Hello, world of 2 switches!

In the output above, our log outputs are identified by *my_project/my_napp*. The
``execute`` method is run right after ``setup`` is finished and prints 0
switches. After a few milliseconds Kyco has started, the switches are added and
we have 2 switches, as expected. After 10 seconds (the interval we defined), the
same message is printed again.

.. tip::
  To see only the output of *my_napp*, run the script of `Running Kyco` with
  a pipe: ``./start_controller.py 2>&1 | grep my_project/my_napp``.

********************
Publishing your NApp
********************

.. TODO:: Explain how to publish a NApp on http://napps.kytos.io

.. include:: ../back_to_list.rst

.. |nn| replace:: ``hello_world``

.. |pyof| replace:: *python3-openflow*
.. _pyof: http://docs.kytos.io/pyof

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |dev_env| replace:: *Development Environment*
.. _dev_env: /general/development_environment_setup

.. TODO:: Where does the Kyco Events documentation will be hosted?
    Should we link to the main kyco documentation? Or we will have a Tutorial
    explaining the KycoEvents?

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: http://docs.kytos.io/kyco/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |dotdiw| replace:: "*Do one thing, do it well*" Unix philosophy
.. _dotdiw: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well

.. |napp_ipv6| replace:: *kytos/of_ipv6drop* napp
.. _napp_ipv6: http://napps.kytos.io/kytos/of.ipv6drop/

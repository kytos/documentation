.. _tutorial-napps-create-your-own:

How to create your own napp
===========================

Code
----

Running once
^^^^^^^^^^^^

Let's build a simple application line by line. First, create the file *main.py*
and extend the ``KycoNApp`` class overriding its 3 main methods:

.. code-block:: python

    from kyco.core.napps import KycoNApp

    class Main(KycoNapp):

        def setup(self):
            pass

        def execute(self):
            pass

        def shutdown(self):
            pass

The application above is the minimum code to be loaded by the Kyco controller.
However, it doesn't do anything and we're going to change that in the next step.
Let's change the ``execute`` method to print the traditional *Hello, world!* in
the file */tmp/my_napp.txt*:

.. code-block:: python

    def execute(self):
        with open('/tmp/my_napp.txt', 'w') as f:
            f.write('Hello, world!')

When our napp is loaded, it will write *Hello, world!* in the file
*/tmp/my_napp.txt*. We can make it more interesting by counting the number of
switches that is available in the ``controller`` attribute:

.. code-block:: python

    def execute(self):
        nr_switches = len(self.controller.switches)
        msg = 'Hello, world of {} switches!'.format(nr_switches)
        with open('/tmp/my_napp.txt', 'w') as f:
            f.write(msg)

.. important::
   When the napp is loaded, the controller may not have detected the switches
   yet and you may see 0 switches in the first message.

Periodical execution
^^^^^^^^^^^^^^^^^^^^
Let's say we want to run the ``execute`` method periodically, e.g. every 10
seconds. For that, we must add one line to the ``setup`` method:

.. code-block:: python

   def setup(self):
       self.execute_as_loop(10)  # seconds

With the line above, the ``execute`` method will be called once when our napp
is loaded and again after 10 seconds. This will keep running indefinitely.


``setup()`` and ``shutdown()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``setup`` and ``shutdown`` methods are executed only once. Although it is
not mandatory to implement them, you must at least declare them with ``pass``,
as we did in the `Running once`_ section.

Before ``execute``, ``setup`` is called. Besides setting the interval between
``execute`` calls (optional, explained in `Periodical execution`_), you can also
initialize any attribute just as you would in Python constructor (``__init__``).

.. important::
   Do not override ``__init__``. Instead, use ``setup``.

If we want to run any code just before our napp is finished, it must be
implemented in the ``shutdown`` method.


Running a napp
--------------

Where to save a napp
^^^^^^^^^^^^^^^^^^^^

In the section `Code`_, we created the file *main.py*. Where should we save that
file? The answer is in the napps folder, and it can be in different locations
depending on how you installed kyco, as described in the following table:

+----------------------------+------------------------------------+
| Installation method        | Napps folder                       |
+============================+====================================+
| ``sudo pip3 install kyco`` | */var/lib/kytos/napps*             |
+----------------------------+------------------------------------+
| virtualenv                 | *$VIRTUAL_ENV/var/lib/kytos/napps* |
+----------------------------+------------------------------------+

Below the napps folder, you'll find the *kytos* folder with all its napps
inside. Similarly, create a folder for your napps and, below it, one for our new
napp. Then, move the code (*main.py*) to that folder. For example, if you
installed Kyco by ``sudo pip3...`` (you don't need to use ``sudo`` with
virtualenv):

.. code-block:: bash

   sudo mkdir -p /var/lib/kytos/napps/my_project/my_napp
   sudo mv main.py /var/lib/kytos/napps/my_project/my_napp/

Running Kyco
^^^^^^^^^^^^

You'll probably want to restart the controller as you develop and improve your
napp. One way to do this is:

.. code-block:: python

   from kyco.config import KycoConfig
   from kyco.controller import Controller

   options = KycoConfig().options['daemon']
   controller = Controller(options)
   controller.start()
   # observe the log messages and /tmp/my_napp.txt
   controller.stop()  # If stop() doesn't work, try ctrl+c

.. tip::
   To make it more practical, make a script with the lines above except the last
   one. Run the script and, to restart the controller, press ctrl+c and run
   the script again.


Log messages
------------

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

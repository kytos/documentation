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

    class MyApp(KycoNapp):

        def setup(self):
            pass

        def execute(self):
            pass

        def shutdown(self):
            pass

The application above is the minimum code to be loaded by the Kyco controller.
However, it doesn't do anything and we're going to change that in the next step.
Let's change the ``execute`` method to print the traditional *Hello, world!* in
the file */tmp/my_app.txt*:

.. code-block:: python

    def execute(self):
        with open('/tmp/my_app.txt', 'w') as f:
            f.write('Hello, world!')

When our napp is loaded, it will write *Hello, world!* in the file
*/tmp/my_app.txt*. We can make it more interesting by counting the number of
switches that is available in the ``controller`` attribute:

.. code-block:: python

    def execute(self):
        nr_switches = len(self.controller.switches)
        msg = 'Hello, world of {} switches!'.format(nr_switches)
        with open('/tmp/my_app.txt', 'w') as f:
            f.write(msg)


Running periodically
^^^^^^^^^^^^^^^^^^^^
Let's say we want to run the ``execute`` method periodically, e.g. every hour.
For that, we must add one line to the ``setup`` method:

.. code-block:: python

   def setup(self):
       self.execute_as_loop(60 * 60)  # seconds

With the line above, the ``execute`` method will be called once when our napp
is loaded and again after *60 \* 60 = 3600* seconds = 1 hour. This will keep
running indefinitely.


``setup()`` and ``shutdown()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``setup`` and ``shutdown`` methods are executed only once. Although it is
not mandatory to implement them, you must at least declare them with ``pass``,
as we did in the `Running once`_ section.

Before ``execute``, ``setup`` is called. Besides setting the interval between
``execute`` calls (optional, explained in `Running periodically`_), you can also
initialize any attribute just as you would in Python constructor (``__init__``).

.. important::
   Do not override ``__init__``. Instead, use ``setup``.

If we want to run any code just before our napp is finished, it must be
implemented in the ``shutdown`` method.

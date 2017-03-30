:tocdepth: 2
:orphan:

.. _tutorial-statistics-example:

#######################
RESTful Statistics NApp
#######################

********
Overview
********

We will and use a statistics NApp (*kytos/of_stats*) with a Mininet network.
The NApp provides a REST API that we will consume to get some data about flows.

The average time to go through it is: 15 min.


What you will learn
====================

* NApps Server: search for, download and enable a NApp;
* Access a NApp's REST API.


What you will need
==================

* :doc:`Kytos and Mininet <how_to_use_kytos_with_mininet>`;
* The dependencies *rrdtool* and *librrd-dev* (Ubuntu package names) as
  installed in :doc:`development_environment_setup`.


******************************
Installing the statistics NApp
******************************

Search for NApps with the term *of_stats*. You should see something like this::

  $ kytos napps search tutorial

  Status |      NApp ID      |               Description
  =======+===================+=========================================
   [--]  | kytos/of_stats    | Provide statistics of openflow switches.

  Status: (i)nstalled, (e)nabled

The status column shows that kytos/of_stats is neither installed nor enabled.
If you see ``[i-]`` in the status, it means it is already installed, but you need
to enable it.
We can download, install and enable a NApp with a single command. If everything goes
well, you should see an output like the one below::

  $ kytos napps install tutorial/of_stats

  INFO  NApp tutorial/of_stats:
  INFO    Searching local NApp...
  INFO    Not found. Downloading from NApps Server...
  INFO    Downloaded and installed.
  INFO    Enabling...
  INFO    Enabled.

You can either check the status by running the search command again or by
listing all of your local network applications. If the NApp is installed but
not enabled, don't forget to enable it.::

  $ kytos napps list

  Status |          NApp ID          |                   Description
  =======+===========================+=================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsibl...
   [i-]  | kytos/of_flow_manager     | NApp that manages switches flows.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all swi...
   [ie]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlo...
   [i-]  | kytos/of_l2lsloop         | A L2 learning switch application for openflow...
   [i-]  | kytos/of_lldp             | App responsible by send packet with lldp prot...
   [ie]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | A simple app that update links between machin...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface...

  Status: (i)nstalled, (e)nabled

.. ATTENTION::
   For this tutorial, make sure that you have only the following NApps enabled:
   *kytos/of_core*, *kytos/of\_l2ls* and *kytos/of_stats*.

*****************
Kytos and Mininet
*****************

We are going to use the same command of the tutorial
:doc:`how_to_use_kytos_with_mininet` but, before, we are going to run the clean
command::

  $ sudo mn -c
  $ sudo mn --topo linear,2 --mac --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow10

Finally, let's generate 5 packets per second from host h1 to h2 with::

  mininet> h1 ping -i 0.2 h2

Of course, this will fail until we launch the Kytos Controller. If it is
running, remember that, at the moment of this writing, it is necessary to
restart Kytos for any change in enabled/disabled NApps to take effect.

After launching Kytos, there are two important lines in its log::

  $ kytosd -f
  (...)
  INFO [werkzeug] (Thread-1)  * Running on http://0.0.0.0:8181/
  (...)
  INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_stats
  (...)

The first ``INFO`` line above shows that the REST API is available at port 8181
and, the second, that *kytos/of_stats* was successfully loaded.

********
REST API
********

To see some flow statistics, visit
http://localhost:8181/kytos/stats/00:00:00:00:00:00:00:01/flows.
At any time, refresh the page to get the latest statistics.

This endpoint of *kytos/of_stats* will show statistics of the last second
about all flows of the DataPathID *00:00:00:00:00:00:00:01* (try to change the
last number to 2).
It follows the `JSON API <http://jsonapi.org/>`_ standard and it is easy for
humans to understand the data. Let's take a closer look at some lines:

.. note:: Some lines were omitted from the output below.

.. code-block:: json

  {
    "data": [
        {
            "actions": [
                {
                    "port": 1,
                    "type": "action_output"
                }
            ],
            "dl_dst": "00:00:00:00:00:01",
            "dl_src": "00:00:00:00:00:02",
            "stats": {
                "Bps": 494.4685778065101,
                "pps": 5.045597732719491
            }
        },
        {
            "actions": [
                {
                    "port": 2,
                    "type": "action_output"
                }
            ],
            "dl_dst": "00:00:00:00:00:02",
            "dl_src": "00:00:00:00:00:01",
            "stats": {
                "Bps": 494.55888395423847,
                "pps": 5.046519224022841
            }
        }
    ]
  }

*Bps* and *pps* mean bytes per second and packets per second, respectively.
As we are sending one ping every 0.2 seconds, *pps* will be close to 5.

In the Mininet console, hit ``ctrl+c`` and run ``h1 ping -i 0.5 h2``.
After a few seconds, *pps* will be close to 2.

********
Database
********

This NApp uses `RRDtool <http://oss.oetiker.ch/rrdtool/>`_. If you wish to erase
the database files, you can run the following command after stopping the
controller: ``cd kytos-napps/napps/kytos/of_stats/rrd && rm -rf flows/ ports/``
(they will be regenerated by the NApp).

.. include:: ../back_to_list.rst

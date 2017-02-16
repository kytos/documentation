:tocdepth: 2
:orphan:

.. _tutorial-how-to-use-kyco-with-mininet:

#############################
How to use Kytos with Mininet
#############################

********
Overview
********

In this tutorial you will learn how to manager your Napps
(Network Applications) to be used with Kytos Controller (**Kyco**). Then, you
will learn how to use the tool |mininet|_ to simulate a virtual network using
the Openflow protocol and turn on the Kyco to handle that virtual network using
the Napps enabled.

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will need
===================

* Your |dev_env|_ already setup

What you will learn
===================

* How to manage the Kytos Napps
* About the Napps used in this tutorial
* How to build a simple topology
* Understanding Kyco's logs
* Verify if ping is working

************
Introduction
************

Now that you have your own development environment you can build a simple
virtual network using the tool |mininet|_. In this tutorial you will build a
simple topology composed by two switches and two hosts connected.This virtual
network should be handled by the controller Kyco using the openflow protocols.

In this tutorial the Napps *of_core*, *of_l2ls* and *of_lldp* must be installed
and enabled to allow the hosts into the network to be connected and recognized
by your IP Address.

*****************************
How to manage the Kytos Napps
*****************************

In order to run the Napps used by this tutorial, first you have to install
them.Once more use the ``kytos`` command line from the ``kytos-utils`` package.

To install and enable the Napps run the commands below:

.. code-block:: bash

 $ kytos napps install kytos/of_core
 $ kytos napps install kytos/of_l2ls
 $ kytos napps install kytos/of_lldp

Now your Napps are ready to be executed.

You can also verify if the Napps are installed and enabled, by running the
comamnd:

.. code-block:: bash

  $ kytos napps list

If you want enable a Napp listed you can run the command:

.. code-block:: bash

  $ kytos napps enable <author_name>/<napp_name>

On the other hand if you want to disable an installed napp you can run the
command:

.. code-block:: bash

  $ kytos napps disable <author_name>/<napp_name>


.. NOTE::
  For this tutorial, you don't want any other napp running except those
  selected. So if your setup has several napps enabled, please disable them,
  with the command that you have learned in this section.


*******************************************************
Brief description about the Napps used in this tutorial
*******************************************************

As we said earlier we will use the napps **of_core**, **of_l2ls** and
**of_lldp** build by the kytos team.In this section you will learn a little
about each one.

of_core
=======

The **of_core** application is the default Kytos Network Application because
that is responsible to handle OpenFlow basic operations such as handle hello
messages, echo request/reply messages and send/receive openflow message by
network.

of_l2ls
=======

The **of_l2ls** application is used to allow basic operations of switches. It
implements the algorithm know as L2 Learning Switch, which aims to figure out
which host is attached to which port.So if you enable this app you will be able
to ping machines.

of_lldp
=======

The **of_lldp** application implements the protocol Link Layer Discovery
Protocol (LLDP).This protocol is vendor free and used to discover network
devices and all links between them.This protocol is implemented as layer 2 (L2)
and defined in the IEEE 802.lab.A network manager system(NMS) can rapidly
obtain the L2 network topology and topology changes over the time using LLDP.

******************************
How to build a simple topology
******************************

Now that you have installed and enabled only NApps used by this tutorial you
must turn on the |mininet|_ service.As said earlier we need build a simple
network using two switches and two hosts.

To do this we will use the command below:

.. code-block:: bash

  $ sudo mn --topo linear,2 --mac --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow10
  *** Creating network
  *** Adding controller
  Unable to contact the remote controller at 127.0.0.1:6633
  *** Adding hosts:
  h1 h2
  *** Adding switches:
  s1 s2
  *** Adding links:
  (h1, s1) (h2, s2) (s2, s1)
  *** Configuring hosts
  h1 h2
  *** Starting controller
  c0
  *** Starting 2 switches
  s1 s2 ...
  *** Starting CLI:
  mininet>

After run that command the mininet output will print that was build two hosts,
two switches and that switches and hosts are linked.So, the mininet console
will be activated and you can send commands to each switch or hosts connected.
For instance if you need see the IP Address of the host 1 you can use the
command below. ::

  mininet> h1 ifconfig
  h1-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
           inet 10.0.0.1  netmask 255.0.0.0  broadcast 10.255.255.255
           inet6 fe80::200:ff:fe00:1  prefixlen 64  scopeid 0x20<link>
           ether 00:00:00:00:00:01  txqueuelen 1000  (Ethernet)
           RX packets 20  bytes 2394 (2.3 KiB)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 13  bytes 1018 (1018.0 B)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

  lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
           inet 127.0.0.1  netmask 255.0.0.0
           inet6 ::1  prefixlen 128  scopeid 0x10<host>
           loop  txqueuelen 1  (Local Loopback)
           RX packets 0  bytes 0 (0.0 B)
           RX errors 0  dropped 0  overruns 0  frame 0
           TX packets 0  bytes 0 (0.0 B)
           TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

  mininet>

If you want see if the ping between hosts is running you can do: ::

  mininet> h1 ping h2
  PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.

That ping is now working well because the Kyco is nos running yet.


*************************
Understanding Kyco's logs
*************************

Now that you have learned how to start Mininet and all NApps needed to this
tutorial was installed and enabled you must start Kyco service running the
command below.

.. code-block:: bash

  $ kyco
  2017-02-10 18:35:03,833 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
  2017-02-10 18:35:03,835 - INFO [kyco.core.tcp_server] (TCP server) Kyco listening at 0.0.0.0:6633
  2017-02-10 18:35:03,836 - INFO [kyco.controller] (RawEvent Handler) Raw Event Handler started
  2017-02-10 18:35:03,837 - INFO [kyco.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-02-10 18:35:03,837 - INFO [kyco.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-02-10 18:35:03,837 - INFO [kyco.controller] (AppEvent Handler) App Event Handler started
  2017-02-10 18:35:03,838 - INFO [kyco.controller] (MainThread) Loading kyco apps...
  2017-02-10 18:35:03,838 - INFO [kyco.controller] (MainThread) Loading NApp kytos/of_core
  2017-02-10 18:35:03,862 - INFO [werkzeug] (Thread-2)  * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
  2017-02-10 18:35:03,892 - INFO [kyco.core.napps] (Thread-3) Running Thread-3 App
  2017-02-10 18:35:03,892 - INFO [kyco.controller] (MainThread) Loading NApp kytos/of_l2ls
  2017-02-10 18:35:03,895 - INFO [kyco.core.napps] (Thread-4) Running Thread-4 App
  2017-02-10 18:35:04,640 - INFO [kyco.core.tcp_server] (Thread-5) New connection from 192.168.56.101:48857
  2017-02-10 18:35:04,641 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...
  2017-02-10 18:35:04,641 - INFO [kyco.core.tcp_server] (Thread-6) New connection from 192.168.56.101:48858
  2017-02-10 18:35:04,648 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...

If every things works the Kyco's logs will be displayed and you can see the
logs of all Napps enabled. In this console output shown above the last four
lines show that two new switches are connected with Kyco.

When a NApp write a log instance the Kyco will show a message in this format: ::

  <date_format> - <TYPE_OF_MESSAGE> [<NAPP_NAME>] <MESSAGE>

All messages shown above was written by Kyco.

*************************
Verify if ping is working
*************************

Now if you try to use the ping command between the host 1 and host 2 the
mininet will display: ::

  mininet> h1 ping h2
  PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
  64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=62.6 ms
  64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.271 ms
  64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.099 ms
  64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.140 ms

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/

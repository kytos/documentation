:tocdepth: 2
:orphan:

.. _tutorial-how-to-use-kytos-with-mininet:

#############################
How to use Kytos with Mininet
#############################

********
Overview
********

In this tutorial you will learn how to use the |mininet|_ tool to simulate a
virtual network using the OpenFlow protocol and manage this virtual network
with **Kytos** and some of our Kytos NApps.

The average time to go through it is: ``10 min``

What you will need
===================

* Your |dev_env|_ already up and running

What you will learn
===================

* How to manage the Kytos NApps
* What NApps used in this tutorial can do
* How to build a simple topology with mininet
* Understanding Kytos logs
* Verify network functionality with ping

************
Introduction
************

Now that you have your own development environment you can build a simple
virtual network using the |mininet|_ tool. In this tutorial you will build a
simple topology, composed of two switches and two hosts connected to each
switch. This virtual network should be handled by the **Kytos** controller
and will use the OpenFlow protocol.

In this tutorial the ``of_core``, ``of_l2ls`` and ``of_lldp`` NApps must be
installed and enabled in order to make the network work as expected.

*****************************
How to manage the Kytos NApps
*****************************

First of all, you need start Kytos:

.. code-block:: console

  $ kytosd -f
  2017-07-18 10:37:07,409 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-18 10:37:07,410 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-18 10:37:07,411 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-18 10:37:07,415 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6653
  2017-07-18 10:37:07,416 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-18 10:37:07,423 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-18 10:37:07,424 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-18 10:37:07,447 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-18 10:37:07,447 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-18 10:37:07,460 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-18 10:37:07,462 - INFO [kytos.core.controller] (MainThread) Loading NApp tutorial/ping
  2017-07-18 10:37:07,471 - INFO [kytos.core.controller] (MainThread) Loading NApp tutorial/pong
  2017-07-18 10:37:07,897 - INFO [root] (ping) Running NApp: <Main(ping, started 140237107877632)>
  2017-07-18 10:37:07,908 - INFO [tutorial/ping] (ping) 2017-07-18 10:37:07.899829 Ping sent.
  2017-07-18 10:37:07,912 - INFO [tutorial/pong] (Thread-6) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:37:07.911947, and the ping was dispatched at 2017-07-18 10:37:07.899829.
  2017-07-18 10:37:07,912 - INFO [root] (pong) Running NApp: <Main(pong, started 140237099484928)>

  (...)

  kytos $>

If you are following the tutorials, you can see the ``tutorial/ping`` and ``tutorial/pong``
NApps enabled and running. To disable them, run:

.. code-block:: console

  $ kytos napps disable tutorial/ping tutorial/pong
  INFO  NApp tutorial/ping:
  INFO    Disabling...
  INFO    Disabled.
  INFO  NApp tutorial/pong:
  INFO    Disabling...
  INFO    Disabled.

To enable the NApps used in this tutorial, you need to have them installed on your
system. You probably already have them, but, in case you don't, you can install
them with the `kytos-utils` package by doing:

.. NOTE:: Do not forget to enable your virtualenv, where you installed the
    Kytos project components.

.. code-block:: console

 $ kytos napps install kytos/of_core kytos/of_l2ls kytos/of_lldp

Now your Napps are installed, enabled and running.

You can also verify the state of each NApp by running the comamnd:

.. code-block:: console

  $ kytos napps list

If you already have them installed, but they are disabled, you can enable them
with the command:

.. code-block:: console

  $ kytos napps enable kytos/of_core kytos/of_l2ls kytos/of_lldp

*******************************************************
Brief description about the NApps used in this tutorial
*******************************************************

As we said earlier, we will use the **of_core**, **of_l2ls** and **of_lldp** NApps
provided by the Kytos team. In this section you will learn a little about each
one.

of_core
=======

The **of_core** application is responsible for doing basic OpenFlow operations,
such as handling hello and echo request/reply messages, and also receiving and
unpacking OpenFlow messages from the network.

of_l2ls
=======

The **of_l2ls** application is used to allow basic operations of switches. It
implements the algorithm known as *L2 Learning Switch*, which aims to figure
out which host is attached to which port. So, if you enable this NApp you will
be able to ping from a host to another.

of_lldp
=======

The **of_lldp** application implements the *Link Layer Discovery
Protocol* (LLDP). This is a vendor-neutral protocol useful for discovering network
devices and the links between them. This protocol is implemented at the network
layer 2 (L2), and defined in the IEEE 802.1ab. A network manager system (NMS)
can rapidly obtain the L2 network topology and topology changes over the time
using LLDP.

******************************
How to build a simple topology
******************************

Now that you have installed and enabled only NApps used by this tutorial, you
must turn on the |mininet|_ service. We will build a simple network, using two
switches and two hosts, with each host connected to one switch, and we'll also
define that the switches will work on the OpenFlow 1.0 protocol.

To do this, use the command below:

.. code-block:: console

  $ sudo mn --topo linear,2 --mac --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow10
  *** Creating network
  *** Adding controller
  Unable to contact the remote controller at 127.0.0.1:6653
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

After running that command, the mininet output will show that two hosts and two
switches were created, and that the switches and the hosts are linked. So, the
mininet console will be activated and you can send commands to each switch or
host connected. For instance, if you need to see the IP Address of host1 (`h1`)
you can use the command below.

.. code-block:: console

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

As Kytos is running with the necessary NApps, your topology should be fully
functional by now. You can test it with ping (ICMP protocol) by running, in
mininet:

.. code-block:: console

  mininet> h1 ping h2
  PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
  64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=62.6 ms
  64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.271 ms
  64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.099 ms
  64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.140 ms

*************************
Understanding Kytos logs
*************************

Let's take a look at the terminal:

.. code-block:: console

  $ kytosd -f
  2017-07-18 10:53:56,567 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-18 10:53:56,568 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-18 10:53:56,569 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-18 10:53:56,577 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6653
  2017-07-18 10:53:56,579 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-18 10:53:56,584 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-18 10:53:56,585 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-18 10:53:56,590 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-18 10:53:56,591 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-18 10:53:56,595 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-18 10:53:56,598 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_lldp
  2017-07-18 10:53:56,746 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_l2ls
  2017-07-18 10:53:56,756 - INFO [root] (of_lldp) Running NApp: <Main(of_lldp, started 139968915678976)>
  2017-07-18 10:53:56,761 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_core
  2017-07-18 10:53:56,766 - INFO [root] (of_l2ls) Running NApp: <Main(of_l2ls, started 139968907286272)>
  2017-07-18 10:53:56,875 - INFO [root] (kytos/of_core) Running NApp: <Main(kytos/of_core, started 139968907286272)>

  (...)

  kytos $> 2017-07-18 10:54:01,761 - INFO [kytos.core.tcp_server] (Thread-23) New connection from 127.0.0.1:56658
  2017-07-18 10:54:01,766 - INFO [kytos.core.tcp_server] (Thread-26) New connection from 127.0.0.1:56660
  2017-07-18 10:54:01,822 - INFO [kytos/of_core] (Thread-33) Connection ('127.0.0.1', 56660), Switch 00:00:00:00:00:00:00:02: OPENFLOW HANDSHAKE COMPLETE
  2017-07-18 10:54:01,823 - INFO [kytos/of_core] (Thread-34) Connection ('127.0.0.1', 56658), Switch 00:00:00:00:00:00:00:01: OPENFLOW HANDSHAKE COMPLETE


On Kytos logs you can see the logs of all enabled NApps.

In the above output, the last four lines shows us that two new switches were
connected to Kytos. Those are the switches running in mininet.

When a NApp writes a log message, Kytos shows it in this format: ::

  <date_format> - <TYPE_OF_MESSAGE> [<NAPP_NAME>] <MESSAGE>

You can see the messages logged by Kytos (kytos.core.*) and by the running NApps.

Good job!

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/

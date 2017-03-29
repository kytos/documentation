:tocdepth: 2
:orphan:

.. _tutorial-how-to-use-kyco-with-mininet:

#############################
How to use Kytos with Mininet
#############################

********
Overview
********

In this tutorial you will learn how to use the |mininet|_ tool to simulate a
virtual network using the Openflow protocol and manage this virtual network
with **Kytos** and some of our Kytos NApps.

The average time to go throught it is: ``10 min``

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
simple topology, composed by two switches and two hosts connected one to each
switch. This virtual network should be handled by the controller **Kytos** and
will use the openflow protocol.

In this tutorial the NApps ``of_core``, ``of_l2ls`` and ``of_lldp`` must be
installed and enabled in order to make the network work as expected.

*****************************
How to manage the Kytos NApps
*****************************

To run the NApps used in this tutorial, you need to have them installed on your
system. You probably already have them, but, in case you don't, you can install
them with the kytos-utils package by doing:

.. NOTE:: Do not forget to enable your virtualenv, where you installed the
    Kytos project components.

.. code-block:: bash

 $ kytos napps install kytos/of_core kytos/of_l2ls kytos/of_lldp

Now your Napps are ready to be executed.

You can also verify if the Napps are installed and enabled, by running the
comamnd:

.. code-block:: bash

  $ kytos napps list

If you already have them installed, but they are disabled, you can enable them
with the command:

.. code-block:: bash

  $ kytos napps enable kytos/of_core kytos/of_l2ls kytos/of_lldp

*******************************************************
Brief description about the NApps used in this tutorial
*******************************************************

As said earlier, we will use the NApps **of_core**, **of_l2ls** and **of_lldp**
provided by the Kytos team. In this section you will learn a little about each
one.

of_core
=======

The **of_core** application is responsible for doing basic OpenFlow operations,
such as handling hello and echo request/reply messages and also receiving and
unpacking openflow messages from the network.

of_l2ls
=======

The **of_l2ls** application is used to allow basic operations of switches. It
implements the algorithm known as *L2 Learning Switch*, which aims to figure
out which host is attached to which port. So, if you enable this NApp you will
be able to ping from a host to another.

of_lldp
=======

The **of_lldp** application implements the protocol *Link Layer Discovery
Protocol* (LLDP). This protocol is vendor free and used to discover network
devices and all links between them. This protocol is implemented at network
layer 2 (L2), and defined in the IEEE 802.1ab. A network manager system(NMS)
can rapidly obtain the L2 network topology and topology changes over the time
using LLDP.

******************************
How to build a simple topology
******************************

Now that you have installed and enabled only NApps used by this tutorial, you
must turn on the |mininet|_ service. We will build a simple network, using two
switches and two hosts, being each host connected to one switch, and also we
need to define that the switches will work on the OpenFlow 1.0 protocol.

To do this use the command below:

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

After running that command, the mininet output will show that two hosts and two
switches were created, and that the switches and the hosts are linked. So, the
mininet console will be activated and you can send commands to each switch or
host connected. For instance, if you need see the IP Address of the host 1 you
can use the command below. ::

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

Since **Kytos** is not running, your network will not be functional. So,
let's start **Kytos**. As you wan't to run both **Kytos** and Mininet at the same
time, open a new terminal window, enable your virtual environment, and run
the controller:

.. code:: shell

  $ cd ~/
  $ source test42/bin/activate
  $ kytosd -f

Going back to your other terminal with mininet, now you can test the ping: ::

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

.. code-block:: bash

  $ kytosd -f
  2017-03-29 09:07:45,852 - INFO [kytos.core.core] (MainThread) Starting Kytos - Kytos Controller
  2017-03-29 09:07:45,856 - INFO [kytos.core.core] (RawEvent Handler) Raw Event Handler started
  2017-03-29 09:07:45,857 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6633
  2017-03-29 09:07:45,857 - INFO [kytos.core.core] (MsgInEvent Handler) Message In Event Handler started
  2017-03-29 09:07:45,859 - INFO [kytos.core.core] (MsgOutEvent Handler) Message Out Event Handler started
  2017-03-29 09:07:45,860 - INFO [kytos.core.core] (AppEvent Handler) App Event Handler started
  2017-03-29 09:07:45,861 - INFO [kytos.core.core] (MainThread) Loading kytos apps...
  2017-03-29 09:07:45,864 - INFO [kytos.core.core] (MainThread) Loading NApp kytos/of_core
  2017-03-29 09:07:45,869 - INFO [werkzeug] (Thread-1)  * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
  2017-03-29 09:07:45,953 - INFO [kytos/of_core] (of_core) Running of_core App
  2017-03-29 09:07:45,955 - INFO [kytos.core.core] (MainThread) Loading NApp kytos/of_l2ls
  2017-03-29 09:07:45,999 - INFO [kytos/of_l2ls] (of_l2ls) Running of_l2ls App
  2017-03-29 09:07:45,999 - INFO [kytos.core.core] (MainThread) Loading NApp kytos/of_lldp
  2017-03-29 09:07:46,007 - INFO [kytos/of_lldp] (of_lldp) Running of_lldp App
  2017-03-29 09:07:46,042 - INFO [kytos.core.tcp_server] (Thread-5) New connection from 127.0.0.1:57730
  2017-03-29 09:07:46,044 - INFO [kytos.core.core] (RawEvent Handler) Handling KytosEvent:kytos/core.connection.new ...
  2017-03-29 09:07:46,050 - INFO [kytos.core.tcp_server] (Thread-6) New connection from 127.0.0.1:57732
  2017-03-29 09:07:46,051 - INFO [kytos.core.core] (RawEvent Handler) Handling KytosEvent:kytos/core.connection.new ...

On Kytos logs you can see the logs of all NApps enabled.

In the above output, the last four lines shows that two new switches were
connected to Kytos. Those are the switches running in mininet.

When a NApp write a log message, Kytos shows it in this format: ::

  <date_format> - <TYPE_OF_MESSAGE> [<NAPP_NAME>] <MESSAGE>

You can see messages logged by Kytos (kytos.core.*) and by the running NApps.

Good job!

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/

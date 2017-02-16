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
with **Kyco** and some of our Kytos NApps.

The average time to go throught it is: ``XX min``

What you will need
===================

* Your |dev_env|_ already setup

What you will learn
===================

* How to manage the Kytos Napps
* About the Napps used in this tutorial
* How to build a simple topology on mininet
* Understanding Kyco's logs
* Verify if ping is working

************
Introduction
************

Now that you have your own development environment you can build a simple
virtual network using the |mininet|_ tool. In this tutorial you will build a
simple topology, composed by two switches and two hosts connected one to each
switch. This virtual network should be handled by the controller **Kyco** and
will use the openflow protocol.

In this tutorial the Napps ``of_core``, ``of_l2ls`` and ``of_lldp`` must be
installed and enabled in order to make the network work as expected.

*****************************
How to manage the Kytos NApps
*****************************

To run the NApps used in this tutorial, you need to have them installed on your
system. You probably already have them, but, in case you don't, you can install
them with the kytos-utils package by doinbg:

.. NOTE:: Do not forget to enable your virtualenv, where you installed the
    kytos projects.

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
Brief description about the Napps used in this tutorial
*******************************************************

As said earlier, we will use the napps **of_core**, **of_l2ls** and **of_lldp**
provided by the Kytos team. In this section you will learn a little about each
one.

of_core
=======

The **of_core** application is responsible for doing basic OpenFlow operations,
such as handling hello and echo request/reply messages as much as receiving and
unpacking openflow message from network.

of_l2ls
=======

The **of_l2ls** application is used to allow basic operations of switches. It
implements the algorithm known as *L2 Learning Switch*, which aims to figure
out which host is attached to which port. So, if you enable this app you will
be able to ping machines.

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

Since **Kyco** is still not running, your network will not be functional. So,
let's start **Kyco**. As you wan't to run both **Kyco** and Mininet at the same
time, open a new terminal window, enable your virtual environment, and run
your **Kyco**:

.. code:: shell

  $ cd tutorials
  $ source test42/bin/activate
  $ kyco

Going back to your other terminal with mininet, now you can test the ping: ::

  mininet> h1 ping h2
  PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
  64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=62.6 ms
  64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.271 ms
  64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.099 ms
  64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.140 ms

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

On Kyco's logs you can see the logs of all Napps enabled.

In the above output, the last four lines shows that two new switches were
connected on Kyco.

When a NApp write a log message, Kyco shows it in this format: ::

  <date_format> - <TYPE_OF_MESSAGE> [<NAPP_NAME>] <MESSAGE>

All messages shown above were written by Kyco. (except the *wekzeug* line)

Nice work! =)

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/

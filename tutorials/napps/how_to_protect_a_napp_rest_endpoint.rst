:tocdepth: 2
:orphan:

.. _tutorial-how-to-protect-a-napp-rest-endpoint:

###################################
How to create your own NApp: Part 4
###################################

********
Overview
********

In this tutorial, you will learn how to create a Network Application (NApp) for
*Kytos* (|kytos|_) to communicate with your application. This NApp will be made
with a public and a private REST endpoints.

The average time to go through this is: ``20 min``.

What you will learn
===================

* How to create a superuser;
* How to create a NApp with a public and a private REST endpoint.

What you will need
==================

* How to create a basic NApp: Part 1 - Refer to |Tutorial_01|_;
* How to create a basic NApp: Part 2 - Refer to |Tutorial_02|_;
* How to create a basic NApp: Part 3 - Refer to |Tutorial_03|_;
* Your |dev_env|_ already up and running;
* The Storehouse NApp, installed and running.


************
Introduction
************

Besides events, another method to communicate with your NApp is
through REST endpoints. These endpoints can be public or private
(please note that the latter is still under development).

The creation of a new endpoint is made by the use of the `@rest` decorator,
and it can be optionally protected using the `@authenticated`
decorator. More information about this module can be found in
the |protect_rest|_ and in the |auth|_.


*************************
Creating your application
*************************

First, to create your application, you have to run the following commands:

.. code-block:: console

    $ mkdir ~/tutorials
    $ cd ~/tutorials
    $ kytos napps create

Now, you must input some data about your NApp:

.. code-block:: console

    --------------------------------------------------------------
    Welcome to the bootstrap process of your NApp.
    --------------------------------------------------------------
    In order to answer both the username and the napp name,
    You must follow this naming rules:
    - name starts with a letter
    - name contains only letters, numbers or underscores
    - at least three characters
    --------------------------------------------------------------

    Please, insert your NApps Server username: <username>
    Please, insert your NApp name: hellorest
    Please, insert a brief description for your NApp [optional]: Hello, world!

    Congratulations! Your NApp have been bootstrapped!
    Now you can go to the directory <username>/hellorest and begin to code your NApp.
    Have fun!

After filling your data, you can access the base code of your application in main.py:

.. code-block:: console

    $ cd ~/tutorials
    $ gedit <username>/hellorest/main.py

The base code will initially look like this:

.. code-block:: python

    from kytos.core import KytosNApp, log
    from napps.<username>.hellorest import settings


    class Main(KytosNApp):

        def setup(self):
            pass

        def execute(self):
            pass

        def shutdown(self):
            pass

Then, edit the methods of Main class:

.. code-block:: python

    from kytos.core import KytosNApp, log
    from napps.<username>.hellorest import settings


    class Main(KytosNApp):

        def setup(self):
            self.name = "REST NApp"

        def execute(self):
            log.info("Running!")

        def shutdown(self):
            log.info("Bye!")

Now, import the REST decorator and create a REST endpoint to return the name of
your application:

.. code-block:: python

    from kytos.core import KytosNApp, log, rest
    from napps.<username>.hellorest import settings
    from flask import jsonify, request


    class Main(KytosNApp):

        def setup(self):
            self.name = "REST NApp"

        def execute(self):
            log.info("Running!")

        def shutdown(self):
            log.info("Bye!")
        
        @rest('v1/name', methods=['GET'])
        def get_name(self):
            return jsonify(self.name), 200

Run kytos:

.. code-block:: console

    $ kytosd -f

Open another terminal and install your application:

.. code-block:: console

    $ python setup.py develop

Check if your application is installed and running with the command:

.. code-block:: console

    $ kytos napps list

    Status |          NApp ID          |              Description
    =======+===========================+=======================================
    [ie]  | kytos/storehouse          | ….
    [ie]  | kytos/hellorest           | ….

Accessing the REST endpoint of your application in a browser or REST client,
you will receive a message with a return like this:

.. code-block:: console

    GET http://0.0.0.0:8181/api/<username>/<napp_name>/name

    $ curl -X GET \
        -H 'Content-type: application/json' \
        -H 'Accept: application/json' \
        http://0.0.0.0:8181/api/<username>/<napp_name>/name

    {"REST NApp"}

How to protect your endpoint
============================

Now, you can secure the created endpoint. To do this, you have to
import the `@authenticated` decorator and add it to this endpoint method.

.. code-block:: python

    from kytos.core import KytosNApp, log, rest, authenticated
    from napps.<username>.hellorest import settings
    from flask import jsonify, request

    class Main(KytosNApp):

        def setup(self):
            self.name = "REST NApp"

        def execute(self):
            log.info("Running!")

        def shutdown(self):
            log.info("Bye!")
        
        @rest('v1/name', methods=['GET'])
        @authenticated
        def get_name(self):
            return jsonify(self.name), 200

Then, if you try to access this endpoint, you will receive an error message
requesting the authentication token. This token must be obtained in the
superuser login process.

.. code-block:: console

    GET http://0.0.0.0:8181/api/<username>/<napp_name>/name

    $ curl -X GET \
        -H 'Content-type: application/json' \
        -H 'Accept: application/json' \
        http://0.0.0.0:8181/api/<username>/<napp_name>/name

    {"error": "Token not send or expired."}

How to create a Superuser
=========================

The protection of the public REST endpoints is accomplished by creating a user
in authentication module. In development environment, run the command below:

.. code-block:: console

    $ kytosd -f -C

    -----------------------
    username: <your_name>
    email: <your_email>
    password: <your_pass>
    re-password: <your_pass>


If all goes well, Kytos will create the user and start normally.

Requesting the authentication token
===================================

Now that superuser has been created, you should access the login endpoint to
request the access token:

.. code-block:: console

    GET http://0.0.0.0:8181/api/kytos/core/auth/login/

    $ curl -X GET \
        -H 'Accept: application/json' \
        -H 'Authorization: Basic <username>:<password>' \
        http://0.0.0.0:8181/api/kytos/core/auth/login/

You will receive the token:

.. code-block:: console

    {
        "token": <token>
    }

Now, you have to send the token in the `Bearer` HTTP header
to be able to access this endpoint:

.. code-block:: console

    GET http://0.0.0.0:8181/api/<username>/<napp_name>/name

    $ curl -X GET \
        -H 'Content-type: application/json' \
        -H 'Accept: application/json' \
        -H 'Authorization: Bearer ${TOKEN}' \
        http://0.0.0.0:8181/api/<username>/<napp_name>/name

If no error occurs, you will receive the normal return from the endpoint:

.. code-block:: console

    {"REST NApp"}

Note: If an error occurs, check the error message and request a new token if
it has expired.

Congratulations! You have completed the tutorial and explored the creation of REST
endpoints using different request methods like POST, PATCH and DELETE. One tip is
that you can use a REST client named |Postman|_ to test your application.


.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |Tutorial_02| replace:: *Tutorial 02*
.. _Tutorial_02: https://tutorials.kytos.io/napps/create_looping_napp/

.. |Tutorial_03| replace:: *Tutorial 03*
.. _Tutorial_03: https://tutorials.kytos.io/napps/create_ping_pong_napps/

.. |protect_rest| replace:: *How to protect a NApp REST endpoint*
.. _protect_rest: https://docs.kytos.io/developer/creating_a_napp/#how-to-protect-your-rest-endpoint

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |auth| replace:: *Auth Documentation*
.. _auth: https://docs.kytos.io/developer/auth

.. |postman| replace:: *Postman*
.. _postman: https://www.getpostman.com/

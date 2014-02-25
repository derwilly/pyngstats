=========
Pyngstats
=========

A Python script for creating long term ping statistics

**Table of Contents**

.. contents::
    :local:
    :depth: 1
    :backlinks: none

Usage
=====
The usage of Pyngstats is simple, just take a look at the examples below

.. code-block:: bash

    # ping a host, stats will be created
    $ python3 pygnstats.py --ping
    
To generate a report, just use

.. code-block:: bash
    
    $ python3 pygnstats.py --report
    
An Advanced Example:

.. code-block:: bash

    # ping the host 8.8.8.8 5 times every 10 secounds
    $ python3 pygnstats.py --ping --host=8.8.8.8 --count=10 --interval=5
    
Commandline interface
=====================

+-----------------------+-----------------------------------------------------+
| Parameter             | Description                                         |
+=======================+=====================================================+
| --report              | generates a html report                             |
+-----------------------+-----------------------------------------------------+
| --ping                | ping a host                                         |
+-----------------------+-----------------------------------------------------+
| --report_dir          | define a report directory                           |
+-----------------------+-----------------------------------------------------+
| --stat_dir            | define a statistics directory                       |
+-----------------------+-----------------------------------------------------+
| --host                | define a specific host to ping                      |
+-----------------------+-----------------------------------------------------+
| --timeout             | timeout for ping in secounds                        |
+-----------------------+-----------------------------------------------------+
| --count               | ping the host x times                               |
+-----------------------+-----------------------------------------------------+
| --interval            | ping the host every x secounds                      |
+-----------------------+-----------------------------------------------------+
| --debug               | print debug information.                            |
+-----------------------+-----------------------------------------------------+
| --version             | print version info                                  |
+-----------------------+-----------------------------------------------------+

Pinging
=======
Use Pygnstats in combination with a cronjob to get a bunch of values the day over to monitor your connection.

.. code-block:: bash

    # pinging
    */1 * * * *    python3 /home/user/pyngstats/pyngstats.py --ping --host=8.8.8.8 --stat_dir=/home/user/reports > /home/user/pyngstats/ping.log

And make the report generate daily

.. code-block:: bash

    # report
    59 23 * * *    python3 /home/user/pyngstats/pyngstats.py --report --stat_dir=/home/user/reports --report_dir=/var/www/report > /home/user/pygnstats/ping.log

Templates
=========
Pyngstats uses html-templates for its reports. You can find them in the templates/ directory.

+-----------------------+-----------------------------------------------------+
| template              | Description                                         |
+=======================+=====================================================+
| index.html            | the frameset for the entire report                  |
+-----------------------+-----------------------------------------------------+
| menu.html             | menu which contains all daily reports               |
+-----------------------+-----------------------------------------------------+
| overview.html         | summery of the daily reports                        |
+-----------------------+-----------------------------------------------------+
| daily.html            | template for the daily reports                      |
+-----------------------+-----------------------------------------------------+

Platforms
=========
Pyngstats is only available for GNU/Linux at the moment. (not tested on Windows or Mac yet)


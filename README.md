pyngstats
=========

A Python script for creating long term ping statistics

Usage
-----
The usage of Pyngstats is simple, just take a look at the examples below

    # ping a host, stats will be created
    python3 pygnstats.py --ping
    
To generate a report, just use

    python3 pygnstats.py --report
    
Commandline interface
---------------------

    # generate a html report
    --report
    
    # ping a host
    --ping
    
    # define a report directory
    --report_dir
    
    # define a statistics directory
    --stat_dir
    
    # define a specific host to ping
    --host
    
    # timeout for ping in secounds
    --timeout
    
    # printing the version
    --version

![Pyngstats Daily](https://raw.github.com/derwilly/pyngstats/master/screenshots/daily.png)
  
Pinging
-------
Use Pygnstats in combination with a cronjob to get a bunch of values the day over to monitor your connection.

    # pinging
    */1 * * * *    python3 /home/uer/pyngstats/pyngstats.py --ping --host=8.8.8.8 > /home/user/pyngstats/ping.log

And make the report generate daily
   
    # report
    59 23 * * *    python3 /home/user/pyngstats/pyngstats.py --report > /home/user/pygnstats/ping.log
    
![Pyngstats Overview](https://raw.github.com/derwilly/pyngstats/master/screenshots/overview.png)

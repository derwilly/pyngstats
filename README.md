pyngstats
=========

A Python script for creating long term ping statistics

Usage
-----
The usage of pyngstats is simple, just take a look at the examples below

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

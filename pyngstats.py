#! /usr/bin/env python3
'''
pygnstats
==============================================================================
Author:   Ferdinand Saufler <mail@saufler.de>
Version:  0.22
Date:     23.02.2014

For documentation please visit https://github.com/derwilly/pyngstats
==============================================================================
'''

import collections
import os
import re
import sys
import time
from subprocess import check_output, CalledProcessError

# version
version = '0.22'

# host
host = 'example.com' # or 192.168.0.1

# this hostname
hostname = os.uname()[1]

# timeout in secounds
timeout = '3'

# default path
path = os.path.dirname(os.path.realpath(__file__))

# path for html reports
report_dir = os.path.dirname(os.path.realpath(__file__)) + '/reports'

# path for measured data
stat_dir = os.path.dirname(os.path.realpath(__file__)) + '/stats'

# create report?
report = False

# do a ping?
do_ping = False

# Hex color (FFFFFF) to RGB tuple (255,255,255)
def hex_to_rgb(value):
   value = value.lstrip('#')
   lv = len(value)
   return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

# RGB tubple (255,255,255) to hex value (FFFFFF)
def rgb_to_hex(rgb):
   return '%02x%02x%02x' % rgb
   
# a formatted, colored output
def out(msg, ctype='info'):
    if not msg or not ctype:
        return
    else:
        if ctype == "warn":
            srt = "warn"
            color = 166 # orange
        elif ctype == "ok":
            srt = " ok "
            color = 34 # green
        elif ctype == "fail":
            srt = "fail"
            color = 160 # red
        else:
            srt = "info"
            color = 33 # blue
        print('[\033[38;5;'+str(color)+'m'+srt+'\033[0m] ' + time.strftime('%d.%m.%y %H:%M') + ' ' + msg)

# create report directory, if no exists       
def create_report_dir(p):
    if os.path.exists(p):
        return True
    else:
        try:
            os.makedirs(p)
            out('report_dir ' + p + ' created.', 'ok')
            return True
        except:
            out('cant create report_dir.', 'fail')
            return False

# create stat directory, if no exists                  
def create_stat_dir(p):
    if os.path.exists(p):
        return True
    else:
        try:
            os.makedirs(p)
            out('stat_dir ' + p + ' created.', 'ok')
            return True
        except:
            out('cant create stats.', 'fail')
            return False
            
def print_version():
    print(os.path.basename(__file__) + ' version ' + version + '\n' +
         'please report bugs to <mail@saufler.de>')
            
def print_help():
    print('Arguments:\n' +
          '  \033[1m --report \033[22m\n' +
          '      Generates a html-report. \n' + 
          '  \033[1m --ping \033[22m\n' +
          '      Do a ping to the given host. \n' + 
          '  \033[1m --report_dir \033[22m\n' +
          '      Specify the directory for html-reports. \n' +
          '  \033[1m --stat_dir \033[22m\n' +
          '      Specify the directory for statistics. \n' + 
          '  \033[1m --host \033[22m\n' +
          '      Take that host for ping. \n' +
          '  \033[1m --timeout \033[22m\n' +
          '      Timeout in secounds (1-30).\n' + 
          '  \033[1m --version \033[22m\n' +
          '      prints the version of this script.\n')
                        
# command line options
for i in sys.argv:
    if '--report' in i:
        report = True
    if '--ping' in i:
        do_ping = True
    if '--report_dir=' in i:
        rdir = str(re.findall(r"^--report_dir=.*", i)[0])
        rdir = rdir[13:]
        if create_report_dir(rdir):
            report_dir = rdir
            out('using report directory ' + report_dir, 'info')
        else:
            out('cant use report_dir. please check the path.', 'fail')
            raise SystemExit
    if '--stat_dir=' in i:
        sdir = str(re.findall(r"^--stat_dir=.*", i)[0])
        sdir = sdir[11:]
        if create_stat_dir(sdir):
            stat_dir = sdir
            out('using stats directory ' + stat_dir, 'info')
        else:
            out('cant use stat_dir. please check the path.', 'fail')
            raise SystemExit
    if '--host=' in i:
        ho = str(re.findall(r"^--host=.*", i)[0])
        host = ho[7:]
        out('using host ' + host + ' for ping.', 'info')
    if '--timeout=' in i:
        ti = str(re.findall(r"^--timeout=.*", i)[0])
        ti = ti[10:]
        try:
            if int(ti) > 0 and int(ti) <= 30:
                timeout = ti
                out('using timeout ' + str(timeout) + ' secounds', 'info')
            else:
                out('timeout must be an integer between 1 and 30.', 'fail')
        except ValueError:
            out('timeout must be an integer between 1 and 30.', 'fail')
    if '--version' in i:
        print_version()
    if '--help' in i:
        print_help()

# if do_ping = True, go on and ping the host           
if do_ping:
    latency_str = ''
    pinfo = b''
    
    if not create_stat_dir(stat_dir):
        ('failed to create stat_dir in do_ping procedure.', 'fail')
        raise SystemExit
    
    try:
        pinfo = str(check_output(['ping', '-c', '1', '-W', timeout , host]))
    except CalledProcessError as err:
        if int(err.returncode) == 1:
            out('ping returned exit status "1", no reply from host.', 'fail')
        elif int(err.returncode) == 2:
            out('ping returned exit status "2", unknown error.', 'fail')
        else:
            out('ping returned an unknown error.', 'fail')
    except Exception as err:
        print(str(err.message))

    try:
        latency_str = str(re.findall(r"time=[0-9]{1,4}.[0-9]{1,4}", pinfo)[0])
    except IndexError:
        out('Index error in ping procedure.', 'fail')
    except TypeError:
        out('Type error in ping procedure', 'fail')
        
    latency = latency_str[5:]
        
    try:
        with open(stat_dir + '/' + time.strftime('%y%m%d'), 'a') as f:
            f.write(time.strftime('%H:%M:%S') + ' ' + latency + '\n')
    except IOError:
        out('cant write to file ' + stat_dir + '/' + time.strftime('%y%m%d'), 'fail')

# if report = True, generate the hmtl reports    
if report:
    report_list = {}
    
    # create report directory if not exists
    if not create_report_dir(report_dir):
        out('failed to create report_dir in report procedure.', 'fail')
        raise SystemExit
    
    # generate the html reports
    file_list = []
    for stat_file in os.listdir(stat_dir):
        file_list.append(stat_file)
        
    file_list = sorted(file_list)
    
    for stat_file in file_list:
        count = 0
        latency = 0
        latency_int = 0
        latency_float = 0.0
        highest_latency = 0.0
        lowest_latency = 100.0
        average_latency = 0.0
        sum_latency = 0.0
        packages_lost = 0
        try:
            with open(report_dir + '/' + stat_file + '.html', 'w+') as f:
                html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ping Report</title>
        <style type="text/css">
             body { font-family:arial,helvetica; font-size:12px; }
        </style>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">

          google.load('visualization', '1.1', { packages: ['corechart', 'controls'] });
          google.setOnLoadCallback(drawChart);

          function drawChart() {
            var data = google.visualization.arrayToDataTable([
              ['Time', 'Count', 'Latency in ms', { role: 'style' }],"""
                try:
                    with open(stat_dir + '/' + stat_file, 'r') as fi:
                        for line in fi:                          
                            date = line[:8]
                            latency = line[9:]
                            latency = latency.replace('\n', '')
                            latency = latency.replace(' ', '')
                            if not latency:
                                latency = 0
                                packages_lost += 1
                            try:
                                latency_float = float(latency)
                                latency_int = int(latency_float)
                            except:
                                continue
                                
                            # colors
                            if latency_int >= 0 and latency_int <= 50:
                                val = (latency_int - 0) * 5
                                color = '#' + str(rgb_to_hex((val, 255, 0)))
                            elif latency_int >= 51 and latency_int <= 75:
                                val = (latency_int - 50) * 10
                                color = '#' + str(rgb_to_hex((255, 255-val, 0)))
                            elif latency_int >= 76 and latency_int <= 100:
                                val = (latency_int - 75) * 10
                                color = '#' + str(rgb_to_hex((255, 0, val)))
                            elif latency_int >= 101 and latency_int <= 125:
                                val = (latency_int - 100) * 10
                                color = '#' + str(rgb_to_hex((255-val, 0, 255)))
                            elif latency_int >= 126 and latency_int <= 150:
                                val = (latency_int - 125) * 10
                                color = '#' + str(rgb_to_hex((0, val, 255)))
                            elif latency_int > 150:
                                color = '#' + str(rgb_to_hex((0, 255, 255)))
                            else:
                                color = '#000000'
                                
                            count = count + 1
                                
                            html+="\n              ['"+str(date)+"', "+str(count)+", "+str(latency)+", 'color: "+color+";'],"
                            
                            if(latency_float > 0):
                                if latency_float > highest_latency:
                                    highest_latency = latency_float
                                if latency_float < lowest_latency:
                                    lowest_latency = latency_float
                                    
                            
                            sum_latency += latency_float
                            
                            if count > 0:
                                average_latency = sum_latency / count
                        
                        report_list[stat_file] = { 'name': stat_file,
                                                   'count': count,
                                                   'latency': latency,
                                                   'latency_int': latency_int,
                                                   'latency_float': latency_float,
                                                   'highest_latency': highest_latency,
                                                   'lowest_latency': lowest_latency,
                                                   'average_latency': average_latency,
                                                   'sum_latency': sum_latency,
                                                   'packages_lost': packages_lost }
                        html = html[0:len(html)-1]
                except ValueError as err:
                    out(str(err), 'fail')
                except IOError as err:
                    out(str(err), 'fail')
                except TypeError as err:
                    out(str(err), 'fail')
                except:
                    out('Unexpected error:' +  str(sys.exc_info()[0]), 'fail')
                html+="""                        
            ]);
            
            var chart = new google.visualization.ChartWrapper({
                chartType: 'ColumnChart', // try 'LineChart' as well
                containerId: 'chart_div',
                dataTable: data,
                options: {"""
                html+="title: 'Ping Statistics for "+stat_file[4:6]+"."+stat_file[2:4]+"."+stat_file[0:2]+" on "+hostname+"',"
                html+="""
                    width: 950,
                    height: 450,
                    chartArea: {
                        left: 40,
                        top: 20,
                        width: 700,
                        height: 350
                    },
                    hAxis: {
                        title: 'Time', 
                        titleTextStyle: {color: '#000'}, 
                        slantedText: true, 
                        slantedTextAngle: 45, 
                        textStyle: { fontSize: 10 }, 
                        },
                    legend: {
                        position: 'right',
                        textStyle: {
                            fontSize: 13
                        }
                    },
                },
                view: {
                    columns: [0, 2, 3]
                },
            });
                    
            var control = new google.visualization.ControlWrapper({
                controlType: 'ChartRangeFilter',
                containerId: 'control_activity',
                options: {
                    filterColumnIndex: 1,
                    ui: {
                        chartType: 'LineChart',
                        snapToData: true, // this bugger is not working
                        chartOptions: {
                            width: 950,
                            height: 70,
                            chartArea: {
                                left: 40,
                                top: 0,
                                width: 700,
                                height: 70
                            },
                            hAxis: {
                                textPosition: 'none'
                            }
                        },
                        chartView: {
                            columns: [1, 2]
                        },
                            minRangeSize: 25,
                    }
                },
                state: {
                    range: {
                        start: 0,
                        end: 300
                    }
                }
            });
            
            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard'));
            
            google.visualization.events.addListener(control, 'statechange', function () {
                var v = control.getState();
                document.getElementById('dbgchart').innerHTML = v.range.start + ' -> ' + v.range.end;
                return 0;
            });

            dashboard.bind(control, chart);
            dashboard.draw(data);
          }
        </script>
    </head>
    <body>
        <div id="dashboard">
            <div id="chart_div"></div>
            <div id="control_activity"></div>
        </div>
        <p style="padding-left:50px;">Range: <span id="dbgchart">Init</span>
        </p>
        <br>
        <br>"""
                html += '<b>number of records</b>: ' + str(count) + '<br>\n'
                html += '<b>lowest latency</b>: ' + str(round(lowest_latency,2)) + ' ms<br>\n'
                html += '<b>highest latency</b>: ' + str(round(highest_latency,2)) + ' ms<br>\n'
                html += '<b>average latency</b>: ' + str(round(average_latency,2)) + ' ms<br><br>\n'
                html += 'powered by <b><a href="https://github.com/derwilly/pyngstats" target="_blank">pyngstats</a></b> version: ' + version + '<br><br>\n'
                html+="""
    </body>
</html>"""
                f.write(html)
                #print(html)
        except IOError:
            out('cant write file ' + report_dir + '/' + stat_file + '.html', 'fail')
            
    # Generate the frameset (index.html)
    try:
        with open(report_dir + '/index.html', 'w+') as f:
            html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Ping Report</title>
    </head>
    <frameset cols="200,*" rows="*" id="mainFrameset">"""
            html+='<frame frameborder="0" id="frame_menu" src="menu.html" name="frame_menu" />'
            html+='<frame frameborder="0" id="frame_content" src="overview.html" name="frame_content" />'
            html+="""
        <noframes>
        <body>
            <p>that page works better with a browser which support frames.</p>
        </body>
        </noframes>
    </frameset>
</html>"""
            f.write(html)
    except IOError:
       out('cant write file ' + path + '/index.html', 'fail')
    
    # Generate overview.html
    try:
        with open(report_dir + '/overview.html', 'w+') as f:
            html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Overview</title>
        <style type="text/css">
             body { font-family:arial,helvetica; font-size:12px; }
        </style>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">

          google.load('visualization', '1.1', { packages: ['corechart', 'controls'] });
          google.setOnLoadCallback(drawChart);

          function drawChart() {
            var data = google.visualization.arrayToDataTable([
              ['id', 'Day', 'highest', 'lowest', 'average', 'packages lost'],
            """
            c = 0
            for i in file_list:
                html+="\n              ["+str(c)+", '"+report_list[i]['name'][4:6]+'.'+report_list[i]['name'][2:4]+'.'+report_list[i]['name'][0:2]+"', "+str(report_list[i]['highest_latency'])+", "+str(report_list[i]['lowest_latency'])+", "+str(round(report_list[i]['average_latency'],3))+", "+str(report_list[i]['packages_lost'])+"],"
                c += 1
            html+="""                        
            ]);
            
            var chart = new google.visualization.ChartWrapper({
                chartType: 'ColumnChart', // try 'LineChart' as well
                containerId: 'chart_div',
                dataTable: data,
                options: {"""
            html+="title: 'Ping Overview on "+hostname+"',"
            html+="""
                    width: 950,
                    height: 450,
                    chartArea: {
                        left: 40,
                        top: 20,
                        width: 700,
                        height: 350
                    },
                    hAxis: {
                        title: 'Day', 
                        titleTextStyle: {color: '#000'}, 
                        slantedText: true, 
                        slantedTextAngle: 45, 
                        textStyle: { fontSize: 10 }, 
                        },
                    legend: {
                        position: 'right',
                        textStyle: {
                            fontSize: 13
                        }
                    },
                },
                view: {
                    columns: [1, 2, 3, 4, 5]
                },
            });
                    
            var control = new google.visualization.ControlWrapper({
                controlType: 'ChartRangeFilter',
                containerId: 'control_activity',
                options: {
                    filterColumnIndex: 0,
                    ui: {
                        chartType: 'LineChart',
                        snapToData: true, // this bugger is not working
                        chartOptions: {
                            width: 950,
                            height: 70,
                            chartArea: {
                                left: 40,
                                top: 0,
                                width: 700,
                                height: 70
                            },
                            hAxis: {
                                textPosition: 'none'
                            }
                        },
                        chartView: {
                            columns: [0, 2, 3, 4, 5]
                        },
                            minRangeSize: 25,
                    }
                },
                state: {
                    range: {
                        start: 0,
                        end: 300
                    }
                }
            });
            
            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard'));
            
            google.visualization.events.addListener(control, 'statechange', function () {
                var v = control.getState();
                document.getElementById('dbgchart').innerHTML = v.range.start + ' -> ' + v.range.end;
                return 0;
            });

            dashboard.bind(control, chart);
            dashboard.draw(data);
          }
        </script>
    </head>
    <body>
        <div id="dashboard">
            <div id="chart_div"></div>
            <div id="control_activity"></div>
        </div>
        <p style="padding-left:50px;">Range: <span id="dbgchart">Init</span>
        </p>
        <br>
        <br>"""
            html += '<b>number of records</b>: ' + str(count) + '<br>\n'
            html += '<b>lowest latency</b>: ' + str(round(lowest_latency,2)) + ' ms<br>\n'
            html += '<b>highest latency</b>: ' + str(round(highest_latency,2)) + ' ms<br>\n'
            html += '<b>average latency</b>: ' + str(round(average_latency,2)) + ' ms<br><br>\n'
            html += 'powered by <b><a href="https://github.com/derwilly/pyngstats" target="_blank">pyngstats</a></b> version: ' + version + '<br><br>\n'
            html+="""
    </body>
</html>"""
            f.write(html)
    except IOError:
       out('cant write file ' + report_dir + '/overview.html', 'fail')
       
    # Generate the menu.html
    try:
        with open(report_dir + '/menu.html', 'w+') as f:
            html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Menu</title>
        <style type="text/css">
             body { font-family:arial,helvetica; font-size:12px; }
        </style>
    </head>
    <body>
        <b>Available Reports:</b><br>"""
            
            file_list = reversed(file_list)
            for j in file_list:
                html+='<a href="'+report_list[j]['name']+'.html" target="frame_content">'+report_list[j]['name'][4:6]+'.'+report_list[j]['name'][2:4]+'.'+report_list[j]['name'][0:2]+'</a><br>'
                
            html+="""
    </body>
</html>"""
            f.write(html)
    except IOError:
       out('cant write file ' + report_dir + '/menu.html', 'fail')

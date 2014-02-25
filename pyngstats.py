#! /usr/bin/env python3
'''
pygnstats
==============================================================================
Author:   Ferdinand Saufler <mail@saufler.de>
Version:  0.25
Date:     25.02.2014

For documentation please visit https://github.com/derwilly/pyngstats
==============================================================================
'''

import os
import re
import sys
import time
from subprocess import check_output, CalledProcessError

# version
version = '0.25'

# host
host = 'example.com' # or 192.168.0.1

# this hostname
hostname = os.uname()[1]

# timeout in secounds
timeout = '3'

# count, stop after sending x requests
count = 1

# wait x secounds until next request
interval = 1

# default path
path = os.path.dirname(os.path.realpath(__file__))

# path for html reports
report_dir = path + '/reports'

# path for measured data
stat_dir = path + '/stats'

# path for html-templates
template_dir = path + '/templates'

# create report?
do_report = False

# do a ping?
do_ping = False

# show debug infos?
debug = False

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
         'please report bugs to <mail@saufler.de>\n' +
         'https://github.com/derwilly/pyngstats')
            
def print_help():
    print('Commandline interface:\n' +
          '\033[1m --report \033[22m\n' +
          '    Generates a html-report. \n' + 
          '\033[1m --ping \033[22m\n' +
          '    Do a ping to the given host. \n' + 
          '\033[1m --report_dir \033[22m\n' +
          '    Specify the directory for html-reports. \n' +
          '\033[1m --stat_dir \033[22m\n' +
          '    Specify the directory for statistics. \n' + 
          '\033[1m --host \033[22m\n' +
          '    Take that host for ping. \n' +
          '\033[1m --timeout \033[22m\n' +
          '    Timeout in secounds (1-30).\n' + 
          '\033[1m --count \033[22m\n' +
          '    stop after sending "count" requests.\n' +
          '\033[1m --interval \033[22m\n' +
          '    waiting x secounds until next request.\n' +
          '\033[1m --debug \033[22m\n' +
          '    print additional debug information.\n' +
          '\033[1m --version \033[22m\n' +
          '    print version info.\n')
          
def ping(loops = 0):
    latency_str = ''
    pinfo = b''
    loops += 1
    
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
        
    if loops < count:
        time.sleep(interval)
        ping(loops)
             
# command line options
if '--debug' in sys.argv:
    debug = True
        
for i in sys.argv:
    if '--report' in i:
        do_report = True
    if '--ping' in i:
        do_ping = True
    if '--report_dir=' in i:
        rdir = str(re.findall(r"^--report_dir=.*", i)[0])
        rdir = rdir[13:]
        if create_report_dir(rdir):
            report_dir = rdir
            if debug:
                out('using report directory ' + report_dir, 'info')
        else:
            out('cant use report_dir. please check the path.', 'fail')
            raise SystemExit
    if '--stat_dir=' in i:
        sdir = str(re.findall(r"^--stat_dir=.*", i)[0])
        sdir = sdir[11:]
        if create_stat_dir(sdir):
            stat_dir = sdir
            if debug:
                out('using stats directory ' + stat_dir, 'info')
        else:
            out('cant use stat_dir. please check the path.', 'fail')
            raise SystemExit
    if '--host=' in i:
        ho = str(re.findall(r"^--host=.*", i)[0])
        host = ho[7:]
        if debug:
            out('using host ' + host + ' for ping.', 'info')
    if '--timeout=' in i:
        ti = str(re.findall(r"^--timeout=.*", i)[0])
        ti = ti[10:]
        try:
            if int(ti) > 0 and int(ti) <= 30:
                timeout = ti
                if debug:
                    out('using timeout ' + str(timeout) + ' secounds', 'info')
            else:
                timeout = 3
                out('timeout must be an integer between 1 and 30. setting timeout = 3', 'warn')
        except ValueError:
            timeout = 3
            out('timeout must be an integer between 1 and 30. setting timeout = 3', 'warn')
    if '--count=' in i:
        tmp = str(re.findall(r"^--count=.*", i)[0])
        try:
            tmp = int(tmp[8:])
            if tmp > 0:
                count = tmp
                if debug:
                    out('using count = ' + str(count) + '.', 'info')
            else:
                count = 1
                out('count must be an integer > 0. setting count = 1', 'warn')
        except ValueError:
            count = 1
            out('count must be an integer > 0. setting count = 1', 'warn')
    if '--interval=' in i:
        tmp = str(re.findall(r"^--interval=.*", i)[0])
        try:
            tmp = int(tmp[11:])
            if tmp > 0:
                interval = tmp
                if debug:
                    out('using interval = ' + str(interval) + '.', 'info')
            else:
                interval = 1
                out('interval must be an integer > 0. setting interval = 1', 'warn')
        except ValueError:
            interval = 1
            out('interval must be an integer > 0. setting interval = 1', 'warn')
    if '--version' in i:
        print_version()
    if '--help' in i:
        print_help()

# if do_ping = True, go on and ping the host           
if do_ping:
    ping()

# if do_report = True, generate the hmtl reports    
if do_report:
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
    
    # load the template
    try:
        with open(template_dir + '/daily.html', 'r') as f:
            template = f.read()
            f.close()
    except IOError:
       out('cant read file ' + template_dir + '/daily.html', 'fail')
       raise SystemExit
    
    for stat_file in file_list:
        current_template = template
        data_counts = 0
        latency = 0
        latency_int = 0
        latency_float = 0.0
        highest_latency = 0.0
        lowest_latency = 100.0
        average_latency = 0.0
        sum_latency = 0.0
        packages_lost = 0

        try:
            with open(stat_dir + '/' + stat_file, 'r') as fi:
                chart_data = ''
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
                        
                    data_counts = data_counts + 1
                        
                    chart_data+="['"+str(date)+"', "+str(data_counts)+", "+str(latency)+", 'color: "+color+";'],\n              "
                    
                    if(latency_float > 0):
                        if latency_float > highest_latency:
                            highest_latency = latency_float
                        if latency_float < lowest_latency:
                            lowest_latency = latency_float
                            
                    
                    sum_latency += latency_float
                    
                    if data_counts > 0:
                        average_latency = sum_latency / data_counts
                
                report_list[stat_file] = { 'name': stat_file,
                                           'data_counts': data_counts,
                                           'latency': latency,
                                           'latency_int': latency_int,
                                           'latency_float': latency_float,
                                           'highest_latency': highest_latency,
                                           'lowest_latency': lowest_latency,
                                           'average_latency': average_latency,
                                           'sum_latency': sum_latency,
                                           'packages_lost': packages_lost }
                chart_data = chart_data[0:len(chart_data)-16]
                current_template = current_template.replace('%chart_data%', chart_data)
        except ValueError as err:
            out(str(err), 'fail')
        except IOError as err:
            out(str(err), 'fail')
        except TypeError as err:
            out(str(err), 'fail')
        #except:
         #   out('Unexpected error:' +  str(sys.exc_info()[0]), 'fail')
        
        chart_title="title: 'Ping Statistics for "+stat_file[4:6]+"."+stat_file[2:4]+"."+stat_file[0:2]+" on "+hostname+"',"
        current_template = current_template.replace('%chart_title%', chart_title)
        
        footer = '<b>number of records</b>: ' + str(data_counts) + '<br>\n\t'
        footer += '<b>lowest latency</b>: ' + str(round(lowest_latency,2)) + ' ms<br>\n\t'
        footer += '<b>highest latency</b>: ' + str(round(highest_latency,2)) + ' ms<br>\n\t'
        footer += '<b>average latency</b>: ' + str(round(average_latency,2)) + ' ms<br><br>\n\t'
        footer += 'powered by <b><a href="https://github.com/derwilly/pyngstats" target="_blank">pyngstats</a></b> version: ' + version + '<br><br>'
        current_template = current_template.replace('%footer%', footer)

        try:
            with open(report_dir + '/' + stat_file + '.html', 'w+') as f:
                f.write(current_template)
        except IOError:
            out('cant write file ' + report_dir + '/' + stat_file + '.html', 'fail')
    
    
    
          
    # Generate the frameset (index.html)
    try:
        with open(template_dir + '/index.html', 'r') as f:
            template = f.read()
            f.close()
    except IOError:
       out('cant read file ' + template_dir + '/index.html', 'fail')
       raise SystemExit
       
    try:
        with open(report_dir + '/index.html', 'w+') as f:
            f.write(template)
    except IOError:
       out('cant write file ' + report_dir + '/index.html', 'fail')
    
    
    
    
    # Generate overview.html
    try:
        with open(template_dir + '/overview.html', 'r') as f:
            template = f.read()
            f.close()
    except IOError:
       out('cant read file ' + template_dir + '/overview.html', 'fail')
       raise SystemExit
       
    c = 0
    chart_data = ''
    for i in file_list:
        chart_data+="["+str(c)+", '"+report_list[i]['name'][4:6]+'.'+report_list[i]['name'][2:4]+'.'+report_list[i]['name'][0:2]+"', "+str(report_list[i]['highest_latency'])+", "+str(report_list[i]['lowest_latency'])+", "+str(round(report_list[i]['average_latency'],3))+", "+str(report_list[i]['packages_lost'])+"],\n              "
        c += 1
        
    chart_data = chart_data[:len(chart_data)-16]
        
    template = template.replace('%chart_data%', chart_data)
    chart_title="title: 'Ping Overview on "+hostname+"',"
    template = template.replace('%chart_title%', chart_title)
    powered_by = 'powered by <b><a href="https://github.com/derwilly/pyngstats" target="_blank">pyngstats</a></b> version: ' + version + '<br><br>'
    template = template.replace('%powered_by%', powered_by)
    
    try:
        with open(report_dir + '/overview.html', 'w+') as f:
            f.write(template)
    except IOError:
       out('cant write file ' + report_dir + '/overview.html', 'fail')
    
    
      
       
    # Generate the menu.html
    try:
        with open(template_dir + '/menu.html', 'r') as f:
            template = f.read()
            f.close()
    except IOError:
       out('cant read file ' + template_dir + '/menu.html', 'fail')
       raise SystemExit
            
    file_list = reversed(file_list)
    links = ''
    for j in file_list:
        links+='<a href="'+report_list[j]['name']+'.html" target="frame_content">'+report_list[j]['name'][4:6]+'.'+report_list[j]['name'][2:4]+'.'+report_list[j]['name'][0:2]+'</a><br>\n\t'
    
    template = template.replace('%links%', links)
    
    try:
        with open(report_dir + '/menu.html', 'w+') as f:
            f.write(template)
    except IOError:
       out('cant write file ' + report_dir + '/menu.html', 'fail')

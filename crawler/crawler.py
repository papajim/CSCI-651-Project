#!/usr/bin/env python

import sys
import os
import logging
import time
import json
import subprocess
import signal
import shlex
import requests
from optparse import OptionParser

############### global variables ############### 

prog_dir  = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0])))
prog_base = os.path.split(sys.argv[0])[1]   # Name of this program

logger = logging.getLogger("my_logger")
chrome_pid = None

############### globa variables end ############

def setup_logger(debug_flag):
    # log to the console
    console = logging.StreamHandler()
    
    # default log level - make logger/console match
    logger.setLevel(logging.INFO)
    console.setLevel(logging.INFO)

    # debug - from command line
    if debug_flag:
	logger.setLevel(logging.DEBUG)
	console.setLevel(logging.DEBUG)

    # formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)7s:  %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.debug("Logger has been configured")

def prog_sigint_handler(signum, frame):
    logger.warn("Exiting due to signal %d" % (signum))
    if chrome_pid is not None:
	terminate_chrome_instance()
    sys.exit(1)

def terminate_chrome_instance():
    #os.kill(chrome_pid, signal.SIGKILL)
    chrome_pid.terminate()
    
def startup_chrome_instance(fout, ferr):
    global chrome_pid
    #chrome_start_cmd = "/usr/bin/google-chrome --headless --disable-extensions --disable-component-extensions-with-background-pages --disk-cache-size=1 --enable-logging --v=1 --remote-debugging-port=9222"
    #chrome_start_cmd = "/usr/bin/google-chrome --headless --disk-cache-size=1 --enable-logging --v=1 --remote-debugging-port=9222"
    #chrome_start_cmd = "/usr/bin/google-chrome --headless --v=1 --remote-debugging-port=9222"
    chrome_start_cmd = "/usr/bin/google-chrome --disk-cache-size=1 --enable-logging --v=1 --remote-debugging-port=9222"
    logger.info("Starting Chrome with command \"%s\"" % chrome_start_cmd)
    chrome_pid = subprocess.Popen(shlex.split(chrome_start_cmd), stdout=fout, stderr=ferr, shell=False)
    #chrome_pid = subprocess.Popen(shlex.split(chrome_start_cmd), shell=False)
    time.sleep(5)
    logger.info("Chrome is running")

def get_video_urls(start_counter, total_counter, websites, wdir):
    search_step = 100
    url_history = {}
    url_history_file = None

    # If file exists start from the checkpoint
    url_history_filename = wdir + "/video_urls.txt"
    if os.path.isfile(url_history_filename):
        with open(url_history_filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                tmp = line.split()
                if tmp[0] in url_history:
                    url_history[tmp[0]].add(tmp[1])
                else:
                    url_history[tmp[0]] = set([tmp[1]])
        url_history_file = open(url_history_filename, "a")
    else:
        url_history_file = open(url_history_filename, "w+")

    # Collect total_counter urls for each website
    for website in websites:
        if not website in url_history:
            counter = 0
            url_history[website] = set()
        else:
            counter = len(url_history[website])

        buffer_list = []
        logger.info("Retrieving video urls for %s" % website)

        search_base = start_counter
        while True:
            if counter >= total_counter:
                break
        
            # Blocking operation, we can parallelize the retrieval with threads or Popen, later on
            googler_cmd = "googler --noprompt --nocolor --json -V --start %s --count %s -w %s \"\"" % (search_base, search_step, website)
            #results = subprocess.check_output(["googler/googler", "--noprompt", "--nocolor", "--json", "-V", "-s", str(search_base), "--count", str(search_step), "-w", website[1], ""])
            results = subprocess.check_output(shlex.split(googler_cmd))
            results = json.loads(results)
            for res in results:
                if counter == total_counter:
                    break
                if res['url'] not in url_history[website]:
                    url_history[website].add(res['url'])
                    buffer_list.append(res['url'])
                    if (len(buffer_list) == search_step):
                        for url in buffer_list:
                            url_history_file.write(website + "\t" + url + "\n")
                        buffer_list = []
                    counter += 1
            search_base += search_step
            time.sleep(10) #pace search

        for url in buffer_list:
            url_history_file.write(website + "\t" + url + "\n")
        
    url_history_file.close()
    return url_history

def get_network_requests(website_video_urls, wdir):
    masterfile_urls = []
    for website in website_video_urls:
        counter = 0
        website_dir = wdir + "/" + website
        if not os.path.exists(website_dir):
            try:
                os.makedirs(website_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                logger.warn("%s already exists" % website_dir)
                pass

        for url in website_video_urls[website]:
            if counter >= 30:
                break

            tmp_website = website[website.find("www.")+4:]
            log_filename_base = website_dir + "/" + url[url.find(tmp_website)+len(tmp_website)+1:].replace("/", "_")
            #log_filename_base = website_dir + "/" + url[url.rfind("/")+1:]
            log_filename = log_filename_base + ".out"
            
            if os.path.isfile(log_filename) and (os.stat(log_filename).st_size > 0):
                logger.info("%s already crawled" % log_filename)
                if os.path.isfile(log_filename_base+".m3u8") or os.path.isfile(log_filename_base+".mpd") or os.path.isfile(log_filename_base+".f4m"):
                    counter += 1
                continue

            logger.debug(log_filename)
            network_log = open(log_filename, "w+")
            nodejs_cmd = "node my_network.js %s" % url
            nodejs_pid = subprocess.Popen(shlex.split(nodejs_cmd), stdout = network_log, shell = False)
            nodejs_pid.wait()
            network_log.close()

            with open(log_filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if ".m3u8" in line:
                        counter += 1
                        masterfile_urls.append(line)
                        response = requests.get(line)
                        with open(log_filename_base+".m3u8", "w+") as g:
                            g.write(response.text)
                        break
                    elif ".mpd" in line:
                        counter += 1
                        masterfile_urls.append(line)
                        response = requests.get(line)
                        with open(log_filename_base+".mpd", "w+") as g:
                            g.write(response.text)
                        break
                    elif ".f4m" in line:
                        counter += 1
                        masterfile_urls.append(line)
                        response = requests.get(line)
                        with open(log_filename_base+".f4m", "w+") as g:
                            g.write(response.text)
                        break

    return masterfile_urls

def main():
    # Configure command line option parser
    prog_usage = "usage: %s [options]" % (prog_base)
    parser = OptionParser(usage=prog_usage)
    
    parser.add_option("-s", "--start", action = "store", type = "int", dest = "start_counter", default = 0, help = "Specify starting point for googler")
    parser.add_option("-c", "--count", action = "store", type = "int", dest = "total_counter", default = 10, help = "Specify total number of unique urls")
    parser.add_option("-f", "--file", action = "store", type = "string", dest = "file", help = "File containing base url of websites")
    parser.add_option("-w", "--work_dir", action = "store", type = "string", dest = "wdir", default = "work", help = "Directory to store the outputs")
    parser.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "Enables debugging output")
    
    # Parse command line options
    (options, args) = parser.parse_args()
    setup_logger(options.debug)

    if not options.file:
        logger.critical("An input file has to be given with --file")
        sys.exit(1)
    
    if not options.wdir:
        logger.critical("Work directory cannot be empty string. Please give a directory with --work_dir")
        sys.exit(1)
    
    # Die nicely when asked to (Ctrl+C, system shutdown)
    signal.signal(signal.SIGINT, prog_sigint_handler)
    signal.signal(signal.SIGTERM, prog_sigint_handler)

    # Setup working space
    if not os.path.exists(options.wdir):
        try:
            os.makedirs(options.wdir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            logger.warn("%s already exists" % options.wdir)
            pass

    # Get the websites
    websites = []
    with open(options.file, "r") as data_file:    
        lines = data_file.readlines()
        for line in lines:
            tmp = line.replace("\n", "").split()
            if tmp[1].startswith("-"):
                logger.warn("Skipped website %s" % tmp[1])
                continue
            websites.append(tmp[1])
    
    # Retrieve video urls
    website_video_urls = get_video_urls(options.start_counter, options.total_counter, websites, options.wdir)

    # Start chrome instanc
    fout = open(options.wdir+"/chrome.out", "w+")
    ferr = open(options.wdir+"/chrome.err", "w+")
    startup_chrome_instance(fout, ferr)
    
    # Retrieve files from network and filter for .m3u8 .mpd and flash
    # Dumps the raw network exchange in files and retrieved m3u8 or mpd master files
    masterfile_urls = get_network_requests(website_video_urls, options.wdir)

    print masterfile_urls

    #time.sleep(30)
    terminate_chrome_instance()
    fout.close()
    ferr.close()

if __name__ == '__main__':
    main()


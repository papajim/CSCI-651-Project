#!/usr/bin/env python

import sys
import os
import logging
import time
import json
import subprocess
import signal
import shlex
from optparse import OptionParser

############### global variables ############### 

prog_dir  = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0])))
prog_base = os.path.split(sys.argv[0])[1]   # Name of this program

logger = logging.getLogger("my_logger")
chrome_pid = None
chrome_out = None
chrome_err = None

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
    chrome_start_cmd = "/usr/bin/google-chrome --headless --disable-gpu --disable-extensions --disable-component-extensions-with-background-pages --disk-cache-size=1 --enable-logging --v=1 --remote-debugging-port=9222"
    logger.info("Starting Chrome with command \"%s\"" % chrome_start_cmd)
    chrome_pid = subprocess.Popen(shlex.split(chrome_start_cmd), stdout=fout, stderr=ferr, shell=False)
    time.sleep(10)
    logger.info("Chrome is running")

def retrieve_video_urls(start_counter, total_counter, websites, wdir):
    step = 50

    counter = 0
    max_counter = 10
    for line in lines:
        #print line
        if counter == max_counter:
            break

        if line[1].startswith("-"):
            continue
    
        results = subprocess.check_output(["googler/googler", "--noprompt", "--nocolor", "--json", "-V", "-s", "100", "--count", "100", "-w", line[1], ""])
        results = json.loads(results)
        for res in results:
            g.write(res['url']+"\n")

        counter += 1

    g.close()
    exit()



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

    # Start chrome instanc
    fout = open(options.wdir+"/chrome.out", "w+")
    ferr = open(options.wdir+"/chrome.err", "w+")
    startup_chrome_instance(fout, ferr)

    # Get the websites
    websites = []
    with open(options.file, "r") as data_file:    
        lines = data_file.readlines()
        for line in lines:
            tmp = line.replace("\n", "").split()
            if tmp[1].startswith("-"):
                logger.warn("Skipped website %s" % tmp[1])
                websites.append(tmp)

    # Retrieve video urls

    # Retrieve files from network and filter for .m3u8 .mpd .

    time.sleep(30)
    terminate_chrome_instance()
    fout.close()
    ferr.close()

if __name__ == '__main__':
    main()


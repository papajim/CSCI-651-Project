The tools used by the project can be found in the following repos.
Forked Googler Repo: https://github.com/papajim/googler
General Project Repo: https://github.com/papajim/CSCI-651-Project

In order to execute Googler from anywhere in the system we append its location to the PATH variable of the system.
For example if Googler path is /home/george/GitHub/googler we append it to the path with the following command:
export PATH=/home/george/GitHub/googler:$PATH

We have extented Googler with the -V arguement that searches for urls containing video.
Example usage is:
googler --noprompt --nocolor --json -V --start 10 --count 10 -w www.cnn.com "bitcoin"

Where:
--noprompt -> instructs googler not to be executed in interactive mode
--nocolor -> excludes special characters for color in terminal
--json -> output should be in json format
-V -> search the video tab in google
--start -> start at the Nth URL
--count -> total number of URLs that we try to fetch
-w -> specifies site to be searched

Example usage of the crawler is:
python crawler.py -s 10 -c 10 -f websites.txt -w my_work_dir

Where:
-s -> is the start at number for the googler invocation
-c -> total number of URLs that we attempt to fetch
-f -> specifies the file with the list of video publishers to be searched
-w -> specifies the working directory for the logs and the outpus of the crawler

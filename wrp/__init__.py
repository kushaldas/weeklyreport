# -*- coding: utf-8 -*-

import wunderpy2
import subprocess
import datetime
import dateutil.parser
import pytz
import os
import configparser

utc=pytz.UTC


def system(cmd):
    """
    Invoke a shell command.
    :returns: A tuple of output, err message, and return code
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    if ret.returncode == 0:
        return out.decode("utf-8").strip(' "\n')


def get_password_pass():
    cmd = "pass wunderlist/secret"
    sec = system(cmd)
    cmd = "pass wunderlist/clientid"
    cid = system(cmd)
    return sec, cid

class WeeklyReport:

    def __init__(self):
        self.api = wunderpy2.WunderApi()
        sec, cid = get_password_pass()
        self.client = self.api.get_client(sec, cid)
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), ".weeklyreport.ini"))
        self.inbox_id = config["wunderlist"]["inbox"]

    def generate_report(self, days=7):
        """This generates the real report"""
        # First let us find the completed tasks
        tasks = self.client.get_tasks(list_id=self.inbox_id, completed=True)
        old = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
        tasks.reverse()
        print("# Completed Tasks\n")

        for task in tasks:
            yourdate = dateutil.parser.parse(task['created_at'])
            if yourdate.date() >= old:
                # Now find all the comments for the same task
                print("#### • {0}\n".format(task['title']))
                comments = self.get_comments(task['id'])
                if not comments:
                    print("")
                    continue
                for c in comments:
                    print("* {0}\n".format(c['text']))
                print("")
            else:
                break

        print("# Ongoing Tasks\n")
        tasks = self.client.get_tasks(list_id=self.inbox_id)
        if tasks:
            tasks.reverse()
        for task in tasks:
            print_flag = False
            result = ""
            result += "#### • {0}\n\n".format(task['title'])
            comments = self.get_comments(task['id'])
            if not comments:
                result += "\n"
                yourdate = dateutil.parser.parse(task['created_at'])
                if yourdate.date() >= old:
                    print(result) # Special case for job started without any update

            for c in comments:
                yourdate = dateutil.parser.parse(c['created_at'])
                if yourdate.date()  >= old:
                    print_flag = True
                result += "* {0}\n".format(c['text'])

            # If there any update then print the job
                print(result)

    def get_comments(self, task_id):
        "Gets the comments for the given task"
        task_id = str(task_id)
        comments = self.client.get_comments(task_id)
        return comments


# Alex Wassel (aw7re)

import urllib.request
import re

def name_norm(name0):
    if "," in name0:
        namelast = name0[0:name0.find(",")]
        namefirst = name0[name0.find(",") + 2:len(name0)]
        name = namefirst.lower() + "-" + namelast.lower()
        return name
    else:
        whole = name0.lower()
        name = whole.replace(" ", "-")
        return name

jobname = re.compile(r'id="personjob">(.*)</')

compensation = re.compile(r'id="paytotal">(.*)</')

comprank = re.compile(r"University of Virginia rank</td><td>([0-9],?[0-9]*)")

def report(name0):
    global rank, job, money
    name0 = name_norm(name0)
    try:
        rank = 0
        page = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/uva2016/'+name0)
        for line in page:
            row = line.decode('utf-8').strip()
            for match in jobname.finditer(row):
                job = (match.group(1))
                if '&gt' in job:
                    job = job.replace("&gt;", ">")
                if '&amp' in job:
                    job = job.replace("&amp;", "&")
                if '&lt' in job:
                    job = job.replace("&lt;", "<")
            for match in compensation.finditer(row):
                money = (match.group(1))
                if ',' in money:
                    money = money.replace(",", "")
                if '$' in money:
                    money = money.replace("$", "")
                money = float(money)

            final = (re.search("University of Virginia rank</td><td>", row))
            if final != None and final.group(0) == "University of Virginia rank</td><td>":
                for same in comprank.finditer(row):
                    answer = same.group(1)
                    rank = answer
                    if "," in rank:
                        rank = rank.replace(",", "")
                    rank = int(rank)
    except:
        job = None
        money = 0
        rank = 0
    return job, money, rank

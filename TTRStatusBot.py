import praw
import requests
import time
import json
import collections
import re

try:
    import settings
except:
    exit("Unable to pull settings from settings.py.\n")


def main():
    # Dictionary is ordered so that the table doesn't change order
    services = collections.OrderedDict()
    services['Game'] = {}
    services['Website'] = {}

    timestamp = str(int(round(time.time())))

    # We only update the sidebar when something has changed,
    # so read in the file that determines when we last updated
    updateFile = open('lastUpdate', 'a+')
    updateFile.seek(0)
    lastUpdate = updateFile.read()
    doUpdate = False

    print 'Checking service statuses.'
    for service in services:
        url = 'http://ttrstatus.nfshost.com/status.php?'
        r = requests.get(url+timestamp+'&service='+service)
        # This is checking to make sure ttrstat.us is responding correctly
        if r.status_code == 200:
            data = json.loads(r.text)
            # This needs to be checked for every service
            if data['lastChanged'] > lastUpdate:
                doUpdate = True
            if data['status'] == 1:
                services[service]['status'] = 'Online'
            else:
                services[service]['status'] = 'Offline'

            services[service]['duration'] = data['duration']
        else:
            services[service] = 'Error'

    if doUpdate:
        updateFile.write(timestamp)
        updateFile.close()
        reddit = praw.Reddit(user_agent=settings.UA)
        reddit.login(settings.REDDIT_LOGIN, settings.REDDIT_PASSWORD)
        reddit.config.decode_html_entities = True

        subSettings = reddit.get_settings(settings.SUBREDDIT_NAME)
        sidebarContents = subSettings['description']
        # Makes header row in table blank
        sidebarStatusTable = "|||\n|:--------------------|---------:|\n"

        # Adds table rows for services. Makes the status a link so that CSS pseudo selectors can be used
        for service, status in services.iteritems():
            sidebarStatusTable += service+' | ['+status['status']+' ('+status['duration']+')](http://ttrstat.us/#'+status['status']+")\n"

        # Please do not remove this :)
        sidebarStatusTable += "\n##[TTR status provided by TTRStat.us](http://ttrstat.us/)\n"

        # Replaces the sidebar with the updated table.
        sidebarContents = re.sub("(\[\]\(#TTRStatusStart\)).*(\[\]\(#TTRStatusEnd\))", r'\1'+'\n\n'+sidebarStatusTable+'\n'+r'\2', sidebarContents, 0, re.DOTALL)

        reddit.update_settings(reddit.get_subreddit(settings.SUBREDDIT_NAME), description=sidebarContents)
        print 'Sidebar updated!'
    else:
        print 'Sidebar not updated - statuses not changed.'

if __name__ == "__main__":
    main()

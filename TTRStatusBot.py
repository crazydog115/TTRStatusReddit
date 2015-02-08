import praw
import requests
import time
import collections
import re
import os
import urllib

try:
    import settings
except:
    exit("Unable to pull settings from settings.py.\n")


def main():
    timestamp = str(int(round(time.time())))

    # We only update the sidebar when something has changed,
    # so read in the file that determines when we last updated
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    updateFilePath = scriptPath+'/lastUpdate'
    try:
        updateFile = open(updateFilePath, 'r')
        lastUpdate = updateFile.read()
        updateFile.close()
    except:
        lastUpdate = 0

    doUpdate = False

    print 'Checking service statuses.'
    r = requests.get('http://ttrstat.us/statusReddit.php?'+timestamp, verify=False)
    # This is checking to make sure ttrstat.us is responding correctly
    if r.status_code != 200:
        print 'Error talking to ttrstat.us'
        return
    else:
        statuses = r.json()
        if int(statuses['lastChanged']) > int(lastUpdate):
            doUpdate = True

    if doUpdate:
        updateFile = open(updateFilePath, 'w+')
        updateFile.write(timestamp)
        updateFile.close()
        reddit = praw.Reddit(user_agent=settings.UA)
        reddit.login(urllib.quote_plus(settings.REDDIT_LOGIN), urllib.quote_plus(settings.REDDIT_PASSWORD))

        subSettings = reddit.get_settings(settings.SUBREDDIT_NAME)
        sidebarContents = subSettings['description']

        # Replaces the sidebar with the updated table.
        sidebarContents = re.sub("(\[\]\(#TTRStatusStart\)).*(\[\]\(#TTRStatusEnd\))", r'\1'+'\n\n'+statuses['table']+'\n'+r'\2', sidebarContents, 0, re.DOTALL)

        reddit.update_settings(reddit.get_subreddit(settings.SUBREDDIT_NAME), description=sidebarContents)
        print 'Sidebar updated!'
    else:
        print 'Sidebar not updated - statuses not changed.'

if __name__ == "__main__":
    main()

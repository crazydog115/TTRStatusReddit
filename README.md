#TTR Status
Script to update sidebar in /r/toontown with status of Toontown Rewritten servers. The sidebar is only modified when a status change is detected

## Usage
1. Open settings.py and set the configuration values
 * REDDIT_LOGIN - Username with permission to edit sidebar in SUBREDDIT_NAME
 * REDDIT_PASSWORD - Password for above user
 * SUBREDDIT_NAME - Name of the subreddit having its sidebar updated
 * VERSION - Script version. Does not need to be changed
 * UA - User agent for the bot. Does not need to be changed.
1. Edit your subreddit's sidebar and add the following where you want the table to appear:
1. Ensure the user running the script has permission to write files to the working directory.

        [](#TTRStatusStart)
        [](#TTRStatusEnd)

Run the script on a cron job, as often as you like (at least once per hour).

The sidebar table can be styled using the following pseudo selectors:

        a[href="http://ttrstat.us/#Offline"]
        and
        a[href="http://ttrstat.us/#Online"]

These will style the cells in the right column of the table, depending on that service's status.
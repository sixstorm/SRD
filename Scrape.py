import praw, os, os.path, random, wget, re, json, logging
from jinja2 import Environment, FileSystemLoader
from time import strftime

# Set Logging Params
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)

# Load Settings
with open("/bin/SRD/settings/settings.json", "r") as f:
    config = json.load(f)

subs = []
for s in config['subreddits']:
    subs.append(s)

validimagetypes = ['.png', '.jpg', '.jpeg', '.gif']
tempfolder = config['local_settings']['tempfolder']

reddit = praw.Reddit(
    client_id = config['reddit_api']['clientid'],
    client_secret = config['reddit_api']['clientsecret'],
    user_agent = config['reddit_api']['useragent'],
)


def RenderPage():
    fileLoader = FileSystemLoader('/bin/SRD/templates')
    env = Environment(loader=fileLoader)

    rData = []

    for file in os.listdir(tempfolder):
        ext = os.path.splitext(file)[1]
        if ext.lower() in validimagetypes:
            rData.append(tempfolder+'/'+file)

    # Set current date and time
    now = strftime("%Y-%m-%d %H:%M:%S")

    # Get URLs from Reddit grab
    rendered = env.get_template("all.html").render(rData=rData, now=now, pageTitle="Reddit")

    fileName = "index.html"
    logging.info("Writing to Index HTML page")
    with open(fileName, 'w') as f:
        f.write(rendered)

def RenderSettingsPage():
    fileLoader = FileSystemLoader('/bin/SRD/templates')
    env = Environment(loader=fileLoader)

    # Put settings into HTML
    rendered = env.get_template("settings_temp.html").render(config=config, pageTitle="Settings")
    
    print("Writing to settings HTML file")
    logging.info("Writing to settings HTML file")
    with open("settings.html", "w") as f:
        f.write(rendered)

def UpdateSubs():
    allnewmedia = []

    # Search temp folder in prep for cleaning
    localfiles = [file for file in os.listdir(tempfolder)]
    
    # Grabbing new media URLs from Reddit
    logging.info('Finding acceptable media from selected SubReddits')
    print('Finding acceptable media from selected SubReddits')
    for sub in subs:
        print("Working on %s" % sub)
        for submission in reddit.subreddit(sub).top(time_filter="day"):
            if submission.url.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')):         
                pattern = '\/(\w+.(jpg|png|jpeg|gif))'
                match = re.search(pattern, submission.url.lower())
                allnewmedia.append(match.group(1))

                # See if this file is in the temp directory
                if match.group(1) not in localfiles:
                    print(submission.url)
                    finalfilename = tempfolder+"/"+match.group(1)
                    print("Downloading %s" % finalfilename)
                    wget.download(submission.url, finalfilename)
                else:
                    print("File %s already downloaded" % match.group(1))

    # Get fresh list of local files
    localfiles = [file for file in os.listdir(tempfolder)]
    # Find files for removal - Files in temp folder and not in last download collection
    filestoremove = list(set(allnewmedia) - set(localfiles))

    # Cleanup old files
    print(filestoremove)

    # Output stats to logging and console
    print("Found %s local files to remove" % len(filestoremove))
    logging.info("Found %s local files to remove" % len(filestoremove))
    for file in filestoremove:
        print("Removing %s" % file)
        logging.info("Removing %s" % file)
        # os.remove(tempfolder+"/"+file)



# Main Script

# First container run check
if not os.path.isdir(tempfolder):
    # Create temp folder
    os.makedirs(tempfolder)


if len(os.listdir(tempfolder)) == 0:
    print("Container first run - Scraping!")
    logging.info("Container first run - Scraping!")
    UpdateSubs()
else:
    # Clear temp directory and run another scrape
    UpdateSubs()

# Render HTML/Jinja
RenderPage()

# RenderSettingsPage()


# for submission in reddit.subreddit(sub).top(time_filter="day", limit=5):

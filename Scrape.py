import praw, os, os.path, random, wget, re, json
from jinja2 import Environment, FileSystemLoader

# Load Settings
with open("settings/settings.json", "r") as f:
    config = json.load(f)

subs = []
for sub in config['subreddits']:
    subs.append(sub['sub'])

validimagetypes = ['.png', '.jpg', '.jpeg', '.gif']
tempfolder = config['local_settings']['tempfolder']

reddit = praw.Reddit(
    client_id = config['reddit_api']['clientid'],
    client_secret = config['reddit_api']['clientsecret'],
    user_agent = config['reddit_api']['useragent'],
)


def RenderPage():
    fileLoader = FileSystemLoader('templates')
    env = Environment(loader=fileLoader)

    rData = []

    for file in os.listdir(tempfolder):
        ext = os.path.splitext(file)[1]
        if ext.lower() in validimagetypes:
            rData.append(tempfolder+'/'+file)

    # Get URLs from Reddit grab
    rendered = env.get_template("all.html").render(rData=rData, pageTitle="Reddit")

    fileName = "index.html"
    with open(fileName, 'w') as f:
        f.write(rendered)

def UpdateSubs():
    for sub in subs:
        for submission in reddit.subreddit(sub).top(time_filter="day"):
            if submission.url.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')):
                print(submission.url)
                # rData.append(submission.url)

                # Download image to temp folder
                pattern = '\/(\w+.(jpg|png|jpeg|gif))'
                match = re.search(pattern, submission.url)
                filename = match.group(1)
                finalfilename = tempfolder+"/"+filename
                if not os.path.exists(finalfilename):
                    wget.download(submission.url, finalfilename)


# Update sub downloads
UpdateSubs()

# Render HTML/Jinja
RenderPage()


# for submission in reddit.subreddit(sub).top(time_filter="day", limit=5):

import praw
import re
import csv
import time
import os

# Define a regex pattern for onion links
onion_pattern = re.compile(r'\b[a-z2-7]{16,56}\.(onion|i2p)\b')

# Function to save data to a CSV file
def save_to_csv(data, filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Your Reddit script application credentials
client_id = 'YOUR_REDDIT_CLIENT_ID'
client_secret = 'YOUR_REDDIT_CLIENT_SECRET'
user_agent = 'macos:YOUR_REDDIT_APPLICATION_NAME:v1.0 (by /u/YOUR_REDDIT_ACCOUNT_NAME)'

# Authenticate with Reddit
print("Authenticating with Reddit...")
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# List of subreddits to process
subreddits_to_process = ['onions', ]

# Calculate sleep time for 100 API calls per minute
sleep_time = 65 / 100

# Counter for the number of posts processed
post_count = 0

# Initialize the set for unique onion links
unique_onion_links = set()

# Specify the output CSV file
output_file = 'Reddit_onion_links.csv'

# Check if the output file already exists, if not, create it with headers
if not os.path.exists(output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Onion Link', 'Source Post Name', 'Source URL'])

# Iterate through each subreddit in the list
for subreddit_name in subreddits_to_process:
    print(f"Accessing subreddit: {subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)

    print("Extracting onion links, source post names, and source URLs...")
    for submission in subreddit.new(limit=990):  # You can change the limit
        post_count += 1
        print(f"Processing post {post_count} from subreddit {subreddit_name}...")

        post_title = submission.title
        post_url = submission.url
        post_onion_links = []

        text = submission.selftext
        matches = onion_pattern.findall(text)
        for match in matches:
            if match not in unique_onion_links:
                unique_onion_links.add(match)
                post_onion_links.append((match, post_title, post_url))

        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            text = comment.body
            matches = onion_pattern.findall(text)
            for match in matches:
                if match not in unique_onion_links:
                    unique_onion_links.add(match)
                    post_onion_links.append((match, post_title, post_url))

        save_to_csv(post_onion_links, output_file)
        time.sleep(sleep_time)

print("Extraction completed and data saved to onion_links.csv.")

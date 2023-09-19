import praw
import re
import csv
import time
import os

# Define a regex pattern for onion links
onion_pattern = re.compile(r'\b[a-z2-7]{16,56}\.onion\b')

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'a', newline='') as file:  # Use 'a' to append to the same file
        writer = csv.writer(file)
        # Write the data
        writer.writerows(data)

# Your Reddit script application credentials
client_id = 'YOUR_REDDIT_CLIENT_ID'
client_secret = 'YOUR_REDDIT_CLIENT_SECRET'
user_agent = 'macos:YOUR_REDDIT_APPLICATION_NAME:v1.0 (by /u/YOUR_REDDIT_ACCOUNT_NAME)'

# Authenticate with Reddit
print("Authenticating with Reddit...")
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Access the subreddit
print("Accessing subreddit...")
subreddit = reddit.subreddit('onions')

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
        # Write the header
        writer.writerow(['Onion Link', 'Source Post Name', 'Source URL'])

# Iterate through the posts
print("Extracting onion links, source post names, and source URLs...")
for submission in subreddit.new(limit=10):  # You can change the limit
    post_count += 1
    print(f"Processing post {post_count}...")

    # Extract the title and URL of the post
    post_title = submission.title
    post_url = submission.url
    print(f"Post Title: {post_title}")
    print(f"Post URL: {post_url}")

    # Lists to store data for this post
    post_onion_links = []

    # Check the post text
    text = submission.selftext
    matches = onion_pattern.findall(text)
    for match in matches:
        if match not in unique_onion_links:
            unique_onion_links.add(match)
            post_onion_links.append((match, post_title, post_url))

    # Check the post comments
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        text = comment.body
        matches = onion_pattern.findall(text)
        for match in matches:
            if match not in unique_onion_links:
                unique_onion_links.add(match)
                post_onion_links.append((match, post_title, post_url))

    # Save the data for this post to the same CSV file
    save_to_csv(post_onion_links, output_file)

    # Sleep to avoid hitting API rate limits
    time.sleep(sleep_time)

print("Extraction completed and data saved to onion_links.csv.")

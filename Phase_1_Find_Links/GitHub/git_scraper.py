import requests
import re
import csv

# GitHub Personal Access Token
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'

# Define the User-Agent (required by GitHub API)
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'User-Agent': 'GitHub-Repo-Parser'
}

# Define a regex pattern for onion links
onion_pattern = re.compile(r'\b[a-z2-7]{16,56}\.onion\b')

# Set to store unique onion links, and List to store the links along with source repository URLs
unique_onion_links = set()
onion_links = []

# Fetch the list of repositories under the topic "onion-links"
repos_url = 'https://api.github.com/search/repositories?q=topic:onion-links'
repos_response = requests.get(repos_url, headers=headers)
repos_data = repos_response.json()

# Iterate through each repository
for repo in repos_data['items']:
    # Get the repository's name, URL and README URL
    repo_name = repo['full_name']
    repo_url = repo['html_url']
    readme_url = f"https://raw.githubusercontent.com/{repo_name}/main/README.md"
    
    print(f"Fetching README.md from repository: {repo_name}")
    
    # Fetch the README file
    readme_response = requests.get(readme_url, headers=headers)
    
    # If README.md file exists
    if readme_response.status_code == 200:
        # Parse onion links
        readme_text = readme_response.text
        matches = onion_pattern.findall(readme_text)
        for match in matches:
            if match not in unique_onion_links:
                unique_onion_links.add(match)
                print(f"Found onion link: {match} in repository {repo_name}")
                onion_links.append((match, repo_url))
    else:
        print(f"README.md not found in repository: {repo_name}")

# Write the onion links and source repository URLs to a CSV file
with open('GitHub_onion_links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Onion Link', 'Source Repository URL'])
    # Write the data
    writer.writerows(onion_links)

print("Extraction completed and data written to GitHub_onion_links.csv")

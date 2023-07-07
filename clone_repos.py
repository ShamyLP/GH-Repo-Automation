import requests
import os
import csv
from colorama import Fore, Style

org_name = "HT2-Labs"
team_slug = "read_all"
token = input("Enter your personal access token: ")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Step 1: Make a GET request to fetch the team information
response = requests.get(f"https://api.github.com/orgs/{org_name}/teams/{team_slug}", headers=headers)
team_info = response.json()

# Step 2: Verify if the team exists
if "id" not in team_info:
    print(f"The '{team_slug}' team does not exist in the '{org_name}' organization.")
    exit()

# Step 3: Extract the team ID from the team information
team_id = team_info["id"]

# Step 4: Variables for pagination
page = 1
per_page = 30  # Adjust the number of repositories per page as needed
repos = []

# Step 5: Fetch all repositories by paginating through the results
while True:
    # Make a GET request to fetch the repositories in the team for the current page
    response = requests.get(
        f"https://api.github.com/teams/{team_id}/repos",
        headers=headers,
        params={"page": page, "per_page": per_page}
    )
    current_repos = response.json()

    # Break the loop if there are no more repositories
    if not current_repos:
        break

    # Add the repositories from the current page to the main repos list
    repos.extend(current_repos)

    # Increment the page number for the next request
    page += 1

# Step 6: Verify if any repositories were found
if not repos:
    print(f"No repositories found in the '{team_slug}' team of the '{org_name}' organization.")
    exit()

# Step 7: Create a directory to store the cloned repositories
os.makedirs(org_name, exist_ok=True)

# Step 8: Change the current directory to the parent directory
os.chdir("..")

# Step 9: Create a CSV file to save the repository names and clone status
csv_file_path = "repository_names.csv"
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Repository Name", "Clone Status"])
csv_file.close()  # Close the CSV file before cloning the repositories

# Step 10: Clone each repository
for i, repo in enumerate(repos, 1):
    repo_name = repo["name"]
    repo_url = repo["clone_url"]

    # Perform the clone operation and set the clone status
    clone_status = "Failed"
    clone_command = f"git clone {repo_url}"
    clone_result = os.system(clone_command)
    if clone_result == 0:
        clone_status = "Success"

    # Print the repository name, clone status, and progress in the terminal
    print(f"{Fore.YELLOW}{repo_name}{Style.RESET_ALL} - {Fore.YELLOW}{i}/{len(repos)}{Style.RESET_ALL}", end=": ")
    if clone_status == "Success":
        print(f"{Fore.GREEN}Successfully Cloned{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Failed to Clone{Style.RESET_ALL}")

    # Append the repository name and clone status to the CSV file
    csv_file = open(csv_file_path, "a", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([repo_name, clone_status])
    csv_file.close()

# Step 11: Print a completion message
print("Cloning completed.")
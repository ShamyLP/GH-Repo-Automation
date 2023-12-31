import os
import json
import yaml
import openpyxl
from github import Github
from github import Auth
from github import GithubException, UnknownObjectException
from datetime import datetime, timedelta
from termcolor import colored

# Prompt the user to enter the GitHub API token
github_token = input("Enter your GitHub API token: ")
auth = Auth.Token(github_token)
g = Github(auth=auth)

# Open Excel Workbook
wb = openpyxl.load_workbook('LP GitHub Repos.xlsx')
sheet = wb.active

def get_package_manager(repo):
    """
    Check for 'package-lock.json' or 'yarn.lock' in repo root.
    If neither are found, returns 'No'.
    """
    try:
        # Get the contents of the root directory of the repository
        root_contents = [content.name for content in repo.get_contents('/')]

        # Check if 'package-lock.json' exists in the root contents
        if 'package-lock.json' in root_contents:
            # If 'package-lock.json' is found, return 'Yes (NPM)' as the package manager
            return 'Yes (NPM)'

        # Check if 'yarn.lock' exists in the root contents
        elif 'yarn.lock' in root_contents:
            # If 'yarn.lock' is found, return 'Yes (Yarn)' as the package manager
            return 'Yes (Yarn)'

        # If neither 'package-lock.json' nor 'yarn.lock' is found, return 'No'
        else:
            return 'No'
    except Exception:
        # Return 'No' if any exception occurs (e.g., network error, authentication failure)
        return 'No'

def get_dependency_management(repo):
    """
    Check for dependabot or renovate pull requests in the repo.
    If neither are found, returns 'No'.
    """
    try:
        # Retrieve the total count of pull requests created by dependabot
        dependabot_prs = repo.get_pulls(state='all', creator='dependabot').totalCount

        # Retrieve the total count of pull requests created by renovate
        renovate_prs = repo.get_pulls(state='all', creator='renovate').totalCount

        # Check if either dependabot or renovate pull requests exist
        if dependabot_prs > 0 and renovate_prs > 0:
            return 'Renovate/Dependabot'
        elif dependabot_prs > 0:
            return 'Yes (Dependabot)'
        elif renovate_prs > 0:
            return 'Yes (Renovate)'
        else:
            return 'No'
    except Exception:
        # Return 'No' if any exception occurs (e.g., network error, authentication failure)
        return 'No'

def get_semantic_release(repo):
    """
    Check for 'semantic-release' in devDependencies in package.json in the repo.
    If not found, returns 'No'.
    """
    try:
        # Retrieve the contents of package.json file
        package_json = json.loads(repo.get_contents('package.json').decoded_content)

        # Check if 'semantic-release' is present in the 'devDependencies' section
        if ('semantic-release' or '@ht2-labs/semantic-release' or '@semantic-release/git' or '@semantic-release/github') in package_json.get('devDependencies', {}):
            return 'Yes'
        else:
            return 'No'
        
    except Exception:
        # Return 'No' if any exception occurs (e.g., network error, invalid JSON, absence of package.json)
        return 'No'

def get_gha(workflows, last_year_limit=365):
    """
    Check if any GitHub Actions workflows exist in the repo and have been used within the last year.
    If not found or not used within the last year, returns 'No'.
    """
    if workflows:
        # Get the current date
        today = datetime.now()

        # Calculate the date limit for the last year
        last_year = today - timedelta(days=last_year_limit)

        # Check if any workflow was used within the last year
        for workflow in workflows:
            last_modified_str = workflow.last_modified
            last_modified = datetime.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z")
            if last_modified > last_year:
                return 'Yes'

    return 'No'

def get_workflow_info(workflows):
    """
    Parses the workflows and extracts necessary information like Integration Suite, Concurrency Rule, Mend.
    Returns a tuple containing a list of workflow names and the extracted information as a dictionary.
    """
    workflow_names = []
    workflow_info = {}

    for workflow in workflows:
        # Extract the workflow file name and path
        workflow_name = workflow.name
        workflow_names.append(workflow_name)  # Add the workflow name to the list

        # Perform parsing or extraction logic specific to your requirements
        # Here, you can access the workflow content, parse it using a YAML parser, and extract the desired information

        # Example: Parsing the workflow YAML file using PyYAML
        workflow_content = workflow.decoded_content.decode("utf-8")
        workflow_yaml = yaml.safe_load(workflow_content)

        # Extract Integration Suite
        integration_suite = workflow_yaml.get("env", {}).get("integration", "N/A")

        # Extract Concurrency Rule
        concurrency_rule = workflow_yaml.get("concurrency", {}).get("group", "N/A")

        # Extract Mend
        mend = workflow_yaml.get("steps", {}).get("mend", "N/A")

        # Add the extracted information to the workflow_info dictionary
        workflow_info[workflow_name] = {
            "Integration Suite (GHA)": integration_suite,
            "Concurrency Rule (GHA)": concurrency_rule,
            "Mend (GHA)": mend,
        }
    return workflow_names, workflow_info

def update_excel(repo_name, package_manager="N/A", dependency_management="N/A", semantic_release="N/A", gha="N/A", integration_suite="N/A", concurrency_rule="N/A", mend="N/A"):
    """
    Updates the row for the specified repo in the Excel sheet with the provided values.
    If the repository name is not found, adds a new row with the values.
    """
    for row in sheet.iter_rows(min_row=2):
        if row[0].value == repo_name:
            row[3].value = package_manager
            row[4].value = dependency_management
            row[5].value = semantic_release
            row[6].value = gha
            row[7].value = integration_suite
            row[8].value = concurrency_rule
            row[9].value = mend

            # Print success message in green
            print(colored(f"Updated {repo_name}", "green"))
            break
    else:
        # If the repository name is not found, add a new row with the values
        sheet.append([repo_name, '', '', package_manager, dependency_management, semantic_release, gha, integration_suite, concurrency_rule, mend])
        # print failure message for each column that wasn't updated in red
        if package_manager == "N/A":
            print(colored(f"Failed to update the Package Manager for {repo_name}", "red"))
        if dependency_management == "N/A":
            print(colored(f"Failed to update the Dependency Management for {repo_name}", "red"))
        if semantic_release == "N/A":
            print(colored(f"Failed to update the Semantic Release for {repo_name}", "red"))
        if gha == "N/A":
            print(colored(f"Failed to update the GHA for {repo_name}", "red"))

def process_repo(repo_name):
    """
    Processes a single repo and updates the Excel sheet accordingly.
    """
    try:
        repo = g.get_repo(repo_name)  # Get the repository using the repo_name
        package_manager = get_package_manager(repo)
        dependency_management = get_dependency_management(repo)
        semantic_release = get_semantic_release(repo)

        try:
            workflows = repo.get_contents(".github/workflows")
            gha = get_gha(workflows)
            workflow_names, workflow_info = get_workflow_info(workflows)  # Call get_workflow_info function

            if workflow_info:
                for workflow_name in workflow_names:
                    info = workflow_info[workflow_name]
                    integration_suite = info.get("Integration")
                    concurrency_rule = info.get("Concurrency")
                    mend = info.get("Mend")
                    update_excel(repo.name, package_manager, dependency_management, semantic_release, gha, integration_suite, concurrency_rule, mend)  # Pass individual workflow information to update_excel function
            else:
                update_excel(repo.name, package_manager, dependency_management, semantic_release, gha)  # Pass basic information to update_excel function

        except GithubException as e:
            if isinstance(e, UnknownObjectException) and e.status == 404:
                print(colored(f"Please ensure that the repository {repo_name} exists and has the .github/workflows directory in its root.\nEnsure the repository name is correct and that you have appropriate access permissions to access the repository and its contents.", "red"))
            else:
                raise e

    except GithubException as e:
        error_message = f"Error processing repo {repo_name}: {str(e)}"
        print(colored(error_message, "red"))

# Iterate over the repositories in the directory
repo_dir = "HT2-Labs"
repo_count = len([filename for filename in os.listdir(repo_dir) if os.path.isdir(os.path.join(repo_dir, filename))])
for idx, filename in enumerate(os.listdir(repo_dir), 1):
    if os.path.isdir(os.path.join(repo_dir, filename)):
        repo_name = f"HT2-Labs/{filename}"
        print(colored(f"Processing repo {idx}/{repo_count}: {repo_name}", "white"))
        process_repo(repo_name)

# Save the Excel sheet
wb.save('LP GitHub Repos.xlsx')
print(colored(f"Excel sheet saved successfully!", "yellow"))
import os
import json
import yaml
import openpyxl
from github import Github

# Prompt the user to enter the GitHub API token
github_token = input("Enter your GitHub API token: ")
g = Github(github_token)

# Repository
repo_name = input("Enter the repository name: ")
repo = g.get_repo(repo_name)

# Open Excel Workbook
wb = openpyxl.load_workbook('LP GitHub Repos.xlsx')
sheet = wb.active

def get_package_manager(repo):
    """
    Check for 'package-lock.json' or 'yarn.lock' in repo root.
    If neither are found, returns 'No'.
    """
    try:
        if 'package-lock.json' in [content.name for content in repo.get_contents('/')]:
            return 'NPM'
        elif 'yarn.lock' in [content.name for content in repo.get_contents('/')]:
            return 'Yarn'
        else:
            return 'No'
    except Exception:
        return 'No'

def get_dependency_management(repo):
    """
    Check for dependabot or renovate pull requests in the repo.
    If neither are found, returns 'No'.
    """
    try:
        dependabot_prs = repo.get_pulls(state='all', creator='dependabot').totalCount
        renovate_prs = repo.get_pulls(state='all', creator='renovate').totalCount
        if dependabot_prs > 0:
            return 'Dependabot'
        elif renovate_prs > 0:
            return 'Renovate'
        else:
            return 'No'
    except Exception:
        return 'No'

def get_semantic_release(repo):
    """
    Check for 'semantic-release' in devDependencies in package.json in the repo.
    If not found, returns 'No'.
    """
    try:
        package_json = json.loads(repo.get_contents('package.json').decoded_content)
        return 'Yes' if 'semantic-release' in package_json.get('devDependencies', {}) else 'No'
    except Exception:
        return 'No'

def get_gha(workflows):
    """
    Check if any GitHub Actions workflows exist in the repo.
    If not found, returns 'No'.
    """
    return 'Yes' if workflows else 'No'

def get_workflow_info(workflows):
    """
    To be implemented.
    Parses the workflows and extracts necessary information like Integration Suite, Concurrency Rule, Mend
    """
    pass

def update_excel(repo_name, package_manager, dependency_management, semantic_release, gha):
    """
    Updates the row for the specified repo in the Excel sheet with the provided values.
    """
    for row in sheet.iter_rows(min_row=2):
        if row[0].value == repo_name:
            row[1].value = package_manager
            row[2].value = dependency_management
            row[3].value = semantic_release
            row[4].value = gha
            # To-do: Update more columns as per the Excel sheet structure
            break

def process_repo(repo):
    """
    Processes a single repo and updates the Excel sheet accordingly.
    """
    package_manager = get_package_manager(repo)
    dependency_management = get_dependency_management(repo)
    semantic_release = get_semantic_release(repo)
    workflows = repo.get_contents(".github/workflows")
    gha = get_gha(workflows)
    # To-do: Call get_workflow_info to gather more workflow information
    update_excel(repo.name, package_manager, dependency_management, semantic_release, gha)

# Process the specified repository
try:
    process_repo(repo)
except Exception as e:
    print(f"Error processing repo {repo.name}: {str(e)}")

# Save the Excel sheet
wb.save('LP GitHub Repos.xlsx')
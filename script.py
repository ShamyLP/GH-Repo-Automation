import os
import json
import yaml
import openpyxl
from github import Github
from datetime import datetime, timedelta

# Prompt the user to enter the GitHub API token
github_token = input("Enter your GitHub API token: ")
g = Github(github_token)

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
            # If 'package-lock.json' is found, return 'NPM' as the package manager
            return 'NPM'

        # Check if 'yarn.lock' exists in the root contents
        elif 'yarn.lock' in root_contents:
            # If 'yarn.lock' is found, return 'Yarn' as the package manager
            return 'Yarn'

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
        if dependabot_prs > 0:
            return 'Dependabot'
        elif renovate_prs > 0:
            return 'Renovate'
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
        if 'semantic-release' in package_json.get('devDependencies', {}):
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
            last_run = workflow.last_modified
            if last_run > last_year:
                return 'Yes'

    return 'No'


def get_workflow_info(workflows):
    """
    Parses the workflows and extracts necessary information like Integration Suite, Concurrency Rule, Mend.
    Returns a dictionary containing the extracted information.
    """
    workflow_info = {}

    for workflow in workflows:
        # Extract the workflow file name and path
        workflow_name = workflow.name
        workflow_path = workflow.path

        # Perform parsing or extraction logic specific to your requirements
        # Here, you can access the workflow content, parse it using a YAML parser, and extract the desired information

        # Example: Parsing the workflow YAML file using PyYAML
        workflow_content = workflow.decoded_content.decode("utf-8")
        workflow_yaml = yaml.safe_load(workflow_content)

        # Extract Integration Suite
        integration_suite = workflow_yaml.get("env", {}).get("INTEGRATION_SUITE")

        # Extract Concurrency Rule
        concurrency_rule = workflow_yaml.get("concurrency", {}).get("group")

        # Extract Mend
        mend = workflow_yaml.get("steps", {}).get("mend")

        # Add the extracted information to the workflow_info dictionary
        workflow_info[workflow_name] = {
            "Integration Suite": integration_suite,
            "Concurrency Rule": concurrency_rule,
            "Mend": mend,
        }

    return workflow_info


def update_excel(repo_name, package_manager, dependency_management, semantic_release, gha,
                 integration_suite=None, concurrency_rule=None, mend=None):
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
            break
    else:
        # If the repository name is not found, add a new row with the values
        sheet.append(
            [repo_name, '', '', package_manager, dependency_management, semantic_release, gha,
             integration_suite, concurrency_rule, mend])


def process_repo(repo):
    """
    Processes a single repo and updates the Excel sheet accordingly.
    """
    package_manager = get_package_manager(repo)
    dependency_management = get_dependency_management(repo)
    semantic_release = get_semantic_release(repo)
    workflows = repo.get_contents(".github/workflows")
    gha = get_gha(workflows)
    workflow_info = get_workflow_info(workflows)  # Call get_workflow_info function
    update_excel(repo.name, package_manager, dependency_management, semantic_release, gha, workflow_info)  # Pass workflow_info to update_excel function


def run_get_package_manager():
    """
    Executes the get_package_manager() function and displays the result.
    """
    # Repository
    repo_name = input("Enter the repository name: ")
    repo = g.get_repo(repo_name)

    package_manager = get_package_manager(repo)
    print(f"Package Manager: {package_manager}")


def run_get_dependency_management():
    """
    Executes the get_dependency_management() function and displays the result.
    """
    # Repository
    repo_name = input("Enter the repository name: ")
    repo = g.get_repo(repo_name)

    dependency_management = get_dependency_management(repo)
    print(f"Dependency Management: {dependency_management}")


def run_get_semantic_release():
    """
    Executes the get_semantic_release() function and displays the result.
    """
    # Repository
    repo_name = input("Enter the repository name: ")
    repo = g.get_repo(repo_name)

    semantic_release = get_semantic_release(repo)
    print(f"Semantic Release: {semantic_release}")


def run_get_gha():
    """
    Executes the get_gha() function and displays the result.
    """
    # Repository
    repo_name = input("Enter the repository name: ")
    repo = g.get_repo(repo_name)

    workflows = repo.get_contents(".github/workflows")
    gha = get_gha(workflows)
    print(f"GHA: {gha}")


def run_update_excel():
    """
    Executes the update_excel() function.
    """
    # Repository
    repo_name = input("Enter the repository name: ")
    repo = g.get_repo(repo_name)

    package_manager = get_package_manager(repo)
    dependency_management = get_dependency_management(repo)
    semantic_release = get_semantic_release(repo)
    workflows = repo.get_contents(".github/workflows")
    gha = get_gha(workflows)
    workflow_info = get_workflow_info(workflows)

    # Prompt for additional information
    integration_suite = input("Integration Suite (GHA) [Yes/No]: ")
    concurrency_rule = input("Concurrency Rule (GHA) [Yes/No]: ")
    mend = input("Mend (GHA) [Yes/No]: ")

    update_excel(repo_name, package_manager, dependency_management, semantic_release, gha,
                 integration_suite, concurrency_rule, mend)

    # Save the Excel sheet
    wb.save('LP GitHub Repos.xlsx')


def main():
    """
    Main function to run the program.
    """
    print("LP GitHub Repo Analysis")

    while True:
        print("\nSelect an option:")
        print("1. Get Package Manager")
        print("2. Get Dependency Management")
        print("3. Get Semantic Release")
        print("4. Get GHA")
        print("5. Update Excel")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            run_get_package_manager()
        elif choice == '2':
            run_get_dependency_management()
        elif choice == '3':
            run_get_semantic_release()
        elif choice == '4':
            run_get_gha()
        elif choice == '5':
            run_update_excel()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

    print("Exiting...")


if __name__ == "__main__":
    main()

import os
import json
import yaml
import openpyxl
import subprocess
from datetime import datetime, timedelta
from termcolor import colored

# Open Excel Workbook
wb = openpyxl.load_workbook('LP GitHub Repos.xlsx')
sheet = wb.active


def get_package_manager(repo_name):
    """
    Clone the repository and check for 'package-lock.json' or 'yarn.lock' in repo root.
    If neither are found, returns 'No'.
    """
    # Clone the repository
    os.system(f"git clone https://github.com/{repo_name}.git")

    # Change the directory to the repository
    os.chdir(repo_name)

    try:
        # Check if 'package-lock.json' exists in the repository
        if os.system("find . -name 'package-lock.json'") == 0:
            # Change the directory back to the original location
            os.chdir("..")

            # Delete the cloned repository
            os.system(f"rm -rf {repo_name}")

            # If 'package-lock.json' is found, return 'Yes (NPM)' as the package manager
            return 'Yes (NPM)'

        # Check if 'yarn.lock' exists in the repository
        elif os.system("find . -name 'yarn.lock'") == 0:
            # Change the directory back to the original location
            os.chdir("..")

            # Delete the cloned repository
            os.system(f"rm -rf {repo_name}")

            # If 'yarn.lock' is found, return 'Yes (Yarn)' as the package manager
            return 'Yes (Yarn)'

        # If neither 'package-lock.json' nor 'yarn.lock' is found, return 'No'
        else:
            # Change the directory back to the original location
            os.chdir("..")

            # Delete the cloned repository
            os.system(f"rm -rf {repo_name}")

            return 'No'
    except Exception:
        # Return 'No' if any exception occurs (e.g., network error, authentication failure)
        return 'No'


def clone_repo(repo_name):
    """
    Clone the repository and change directory into it.
    Returns 'True' if successful, 'False' otherwise.
    """
    if os.system(f"git clone https://github.com/{repo_name}.git") == 0:
        os.chdir(repo_name)
        return True
    else:
        return False


def return_to_root(repo_name):
    """
    Change directory back to root and delete the cloned repository.
    """
    os.chdir("..")
    os.system(f"rm -rf {repo_name}")


def get_package_manager(repo_name):
    """
    Checks for 'package-lock.json' or 'yarn.lock' in repo root.
    If neither are found, returns 'No'.
    """
    if not clone_repo(repo_name):
        return 'No'

    if os.system("find . -name 'package-lock.json'") == 0:
        return_to_root(repo_name)
        return 'Yes (NPM)'

    elif os.system("find . -name 'yarn.lock'") == 0:
        return_to_root(repo_name)
        return 'Yes (Yarn)'

    else:
        return_to_root(repo_name)
        return 'No'

# Additional functions


def get_dependency_management(repo_name):
    """
    Check the repository for a dependency management file, such as a 'requirements.txt' or 'Pipfile'.
    """
    if not clone_repo(repo_name):
        return 'No'

    if os.system("find . -name 'requirements.txt'") == 0 or os.system("find . -name 'Pipfile'") == 0:
        return_to_root(repo_name)
        return 'Yes'

    else:
        return_to_root(repo_name)
        return 'No'


def get_semantic_release(repo_name):
    """
    Check the repository for semantic release configuration files.
    """
    if not clone_repo(repo_name):
        return 'No'

    if os.system("find . -name '.releaserc'") == 0 or os.system("find . -name 'release.config.js'") == 0:
        return_to_root(repo_name)
        return 'Yes'

    else:
        return_to_root(repo_name)
        return 'No'


def get_gha(repo_name):
    """
    Check the repository for GitHub Actions configuration files.
    """
    if not clone_repo(repo_name):
        return 'No'

    if os.system("find .github/workflows -name '*.yml'") == 0 or os.system("find .github/workflows -name '*.yaml'") == 0:
        return_to_root(repo_name)
        return 'Yes'

    else:
        return_to_root(repo_name)
        return 'No'


def update_excel(idx, repo_name, package_manager, dependency_management, semantic_release, gha):
    """
    Update the Excel file with the data retrieved.
    """
    sheet.cell(row=idx, column=1, value=repo_name)
    sheet.cell(row=idx, column=2, value=package_manager)
    sheet.cell(row=idx, column=3, value=dependency_management)
    sheet.cell(row=idx, column=4, value=semantic_release)
    sheet.cell(row=idx, column=5, value=gha)


def process_repo(idx, repo_name):
    """
    Process each repo and update the Excel file with the data.
    """
    print(
        colored(f"Processing repo {idx}/{sheet.max_row}: {repo_name}", "white"))

    package_manager = get_package_manager(repo_name)
    dependency_management = get_dependency_management(repo_name)
    semantic_release = get_semantic_release(repo_name)
    gha = get_gha(repo_name)

    update_excel(idx, repo_name, package_manager,
                 dependency_management, semantic_release, gha)

# Include other function definitions (get_dependency_management, get_semantic_release, get_gha, get_workflow_info, update_excel, process_repo) here


# Iterate over the repositories
repos = ["curtar", "conversAI", "insights"]
for idx, repo_name in enumerate(repos, 1):
    process_repo(idx, repo_name)

# Save the Excel sheet
wb.save('LP GitHub Repos.xlsx')
print(colored(f"Excel sheet saved successfully!", "yellow"))

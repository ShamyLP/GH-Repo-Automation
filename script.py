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

# Include other function definitions (get_dependency_management, get_semantic_release, get_gha, get_workflow_info, update_excel, process_repo) here

# TODO: The remaining functions (get_dependency_management, get_semantic_release, get_gha, get_workflow_info, update_excel, process_repo)
# would also need to be updated to not use the GitHub API and instead use command line utilities or other means. The above function is
# just a starting point to demonstrate how you might approach this.


# Iterate over the repositories
repos = ["curtar", "conversAI", "insights"]
for idx, repo_name in enumerate(repos, 1):
    print(colored(f"Processing repo {idx}/{len(repos)}: {repo_name}", "white"))

# Save the Excel sheet
wb.save('LP GitHub Repos.xlsx')
print(colored(f"Excel sheet saved successfully!", "yellow"))

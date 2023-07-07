# GitHub Repository Data Automation

## Overview

This project provides scripts to automate the process of gathering and updating data from GitHub repositories within an organization and populating an Excel spreadsheet with the collected information. The scripts interact with the GitHub API to extract relevant data such as the package manager used, dependency management details, usage of semantic release, GitHub Actions (GHA), and other customizable fields. The project includes the following scripts:

- `script.py`: The main script to gather and update repository data in the Excel spreadsheet.
- `test.py`: The test script containing unit tests for the functions in `script.py`.
- `clone_repos.py`: An additional script to clone repositories from a GitHub organization.

## Features

- **Data Gathering**: The `script.py` script collects specific information from GitHub repositories such as the package manager (NPM or Yarn), dependency management (Dependabot or Renovate), semantic release usage, and the presence of GitHub Actions workflows.
- **Excel Automation**: The gathered data is automatically updated in an Excel spreadsheet to maintain an organized and consolidated record of repository details.
- **Cloning Repositories**: The `clone_repos.py` script allows you to clone repositories from a GitHub organization.
- **Extensibility**: The scripts can be extended to extract additional repository information by implementing custom logic based on specific project requirements.
- **Error Handling**: Appropriate error handling and exception management are implemented to ensure smooth execution and handle unexpected scenarios.
- **Unit Testing**: The `test.py` script contains unit tests for the functions in `script.py` to verify their functionality.

## Requirements

- Python 3.x
- `openpyxl` library (for Excel manipulation)
- `PyGithub` library (for GitHub API interaction)
- `colorama` library (for colored terminal output)

## Usage

1. Clone the repository or download the `script.py`, `test.py`, and `clone_repos.py` files.
2. Install the required libraries by running the following command in your terminal: `pip install openpyxl PyGithub colorama`
3. **Set up your GitHub API token:**
   - Create a personal access token (PAT) on GitHub with appropriate access permissions to the organization and repositories you want to access.
   - Set the token as an environment variable named `GITHUB_TOKEN` to authenticate with the GitHub API.
4. Use the `clone_repos.py` script to clone repositories from a GitHub organization:
   - Update the `org_name` and `team_slug` variables with the appropriate organization and team information.
   - Execute the `clone_repos.py` script: `python clone_repos.py`
   - The script will prompt you to enter your personal access token.
   - It will clone the repositories and provide progress updates in the terminal.
5. Modify the `script.py` file:
   - Update the repository name in the `repo_name` variable to the target repository you want to analyze.
   - Update the path to your Excel spreadsheet in the `wb = openpyxl.load_workbook('LP GitHub Repos.xlsx')` line.
6. Execute the `script.py` script by running the following command in your terminal: `python script.py`
   - The script will prompt you to enter the GitHub API token and repository name.
   - It will gather the required data and update the Excel spreadsheet accordingly.
7. (OPTIONAL) Run the unit tests by executing the `test.py` script: `python test.py`
   - The tests will verify the functionality of the functions in `script.py`.


## Limitations

- **Rate Limits**: The GitHub API has rate limits, so the scripts might encounter limitations depending on the number of repositories and API calls made. Consider implementing rate limit handling and optimization techniques for large repositories or data sets.
- **Authentication**: Ensure that the GitHub API token provided has appropriate access permissions to the organization and repositories being accessed.
- **Environment Setup**: It is assumed that Python and the required libraries are properly installed on the system.

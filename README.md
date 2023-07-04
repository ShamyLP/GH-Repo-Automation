# GitHub Repository Data Automation

## Overview

This project aims to automate the process of gathering and updating data from GitHub repositories within an organization and populating an Excel spreadsheet with the collected information. The script interacts with the GitHub API to extract relevant data such as the package manager used, dependency management details, usage of semantic release, GitHub Actions (GHA), and other customizable fields.

## Features

- Data Gathering: The script collects specific information from GitHub repositories such as the package manager (NPM or Yarn), dependency management (Dependabot or Renovate), semantic release usage, and the presence of GitHub Actions workflows.
- Excel Automation: The gathered data is automatically updated in an Excel spreadsheet to maintain an organized and consolidated record of repository details.
- Extensibility: The script can be extended to extract additional repository information by implementing custom logic based on specific project requirements.
- Error Handling: Appropriate error handling and exception management are implemented to ensure smooth execution and to handle unexpected scenarios.

## Requirements

- Python 3.x
- `openpyxl` library (for Excel manipulation)
- `PyGithub` library (for GitHub API interaction)

## Usage

1. Clone the repository or download the script file.
2. Install the required libraries by running `pip install openpyxl PyGithub` in your terminal.
3. Set up your GitHub API token as an environment variable named `GITHUB_TOKEN`.
4. Modify the script to specify the organization name and the path to your Excel spreadsheet.
5. Execute the script by running `python script.py` in your terminal.

## Limitations

- Rate Limits: The GitHub API has rate limits, so the script might encounter limitations depending on the number of repositories and API calls made. Consider implementing rate limit handling and optimization techniques for large repositories or data sets.
- Authentication: Ensure that the GitHub API token provided has appropriate access permissions to the organization and repositories being accessed.
- Environment Setup: It is assumed that Python and the required libraries are properly installed on the system.

#!/usr/bin/env python3
""" Automatically put github comments using API """
import time
import yaml
import requests


def _Schedule_time(Hour: int, Minute: int):
    """_Schedule_time(15,30). It means 3.30 PM."""
    try:
        if 0 <= Hour < 24 and 0 <= Minute < 60:
            if 0 <= Hour < 10:
                Hour = str(Hour)
                Hour = f"0{Hour}"
            elif 0 <= Minute < 10:
                Minute = str(Minute)
                Minute = f"0{Minute}"
            Schedule = f"{Hour}:{Minute}"
            return Schedule
        else:
            print("Incorrect value")

    except ValueError:
        print("Invalid")


def main_URL(user: str):
    """ Main git hub URL """
    return f"https://api.github.com/users/{user}/repos"


def _response(url, header):
    """ Get the response based on code """
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        api_response = response.json()
    else:
        print(f"Failed Status code: {response.status_code}")
        print(response.text)
    return api_response


def _search_repo(search_name, header):
    """ Find repository in this url """
    repo_check_url = "https://api.github.com/search/repositories"
    query = {'q': search_name}
    response = requests.get(repo_check_url, headers=header, params=query)
    if response.status_code == 200:
        return search_name
    else:
        print("Invalid repository")


def repositories_list(username, header):
    """ List out all repositories """
    url = main_URL(username)
    json_response = _response(url, header)
    if not json_response is None:
        print("Repositories list:\n")
        repos = []
        for repo in json_response:
            print(repo['name'])
            repos.append(repo['name'])
    else:
        print("Invalid repository")

    choose_repo = input("\nEnter repository name [Example:jenkins]: ")
    if choose_repo in repos:
        return repos
    else:
        repos = _search_repo(choose_repo, header)
    return repos


def issues_list(username, header, repository):
    """ list of all issues in particular repository """
    url = f"https://api.github.com/repos/{username}/{repository}/issues"
    json_response = _response(url, header)
    if not json_response is None:
        issues = []
        for _ in json_response:
            print(f"{_['number']}: {_['title']}")
            issues.append(_['number'])
        while len(issues) > 0:
            choose_issue = int(input("Select number of issue[For Ex:18] :"))
            if choose_issue in issues:
                return choose_issue
                break
            else:
                print("Invalid selection number")
                continue
    else:
        print("Invalid repository")


def put_comments(url, api_header, msg):
    """ Response of the put comments """
    comments_payload = {"body": msg}
    response = requests.post(url, json=comments_payload, headers=api_header)
    if response.status_code == 201:
        print("Comment added successfully!")
    else:
        print("Failed to add comment. Status code:", response.status_code)
        print("Response:", response.text)


def banner():
    """ Displayed Software information"""
    print("Version: 1.0.0v\nGithub issues comments put through API\n\n")


def load_config(file_path):
    """ Load the parameter of yaml file """
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


if __name__ == '__main__':
    CONFIG_FILE = 'git_config.yaml'
    git_parameter = load_config(CONFIG_FILE)
    header = {
        "Authorization": f"token {git_parameter.get('API_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
        }
    banner()
    select_repo = repositories_list(git_parameter.get('username'), header)
    issue = issues_list(git_parameter.get('username'), header, select_repo)
    comments_url = (
        f"https://api.github.com/repos/{git_parameter.get('username')}"
        f"/{select_repo}/issues/{issue}/comments"
    )

    current_time = time.localtime()
    Now = time.strftime("%H:%M", current_time)
    print(f"Current time: {Now}")
    message = git_parameter.get('comment')
    schedule = input("Set your schedule Time(For Ex: 1:59): ")
    hour, minute = schedule.split(':')
    hour = int(hour)
    minute = int(minute)
    while True:
        current_time = time.localtime()
        Now = time.strftime("%H:%M", current_time)
        if Now == _Schedule_time(hour, minute):
            put_comments(comments_url, header, message)
            break

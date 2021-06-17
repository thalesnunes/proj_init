import argparse
import os
from typing import Any

from github import Github


def init_parser() -> argparse.ArgumentParser:
    '''Initializes the command line parser.add()

    Returns:
        argparse.ArgumentParser: Command line parser with added arguments
    '''
    parser = argparse.ArgumentParser(prog='create',
                                     description='Automate your workflow with create command.')
    parser.add_argument('-l', '--local', dest='local',
                        action='store_true',
                        help='Creates your repo only locally.')
    parser.add_argument('-p', '--private', dest='private',
                        action='store_true',
                        help='Creates your repo in private mode.')
    parser.add_argument('repo_name', metavar='<repo_name>',
                        help='Name of your repo to be created.')
    return parser

def validate(args: Any, path: str):
    '''Validates the input.

    Args:
        args (Any): Args from the command line.
        path (str): Path where the repo will be created.

    Raises:
        AssertionError: LOCAL and PRIVATE can't be used at same time.
        NameError: Duplicated repos.
    '''
    if args.local == args.private == True:
        raise AssertionError("LOCAL and PRIVATE can't be used at same time.")

    if os.path.isdir(f'{path}/{args.repo_name}'):
        raise NameError('A repo with this name already exists! Please, try another name.')

def create_github_repo(github_token: str, repo_name: str, private: bool = False) -> str:
    '''Creates Github repo.

    Args:
        github_token (str): Token to access Github.
        repo_name (str): Name of the Github repo.
        private (bool, optional): Private or not. Defaults to False.

    Returns:
        str: Returns the github repo link.
    '''
    repo_name_git = repo_name.replace(' ', '-')
    github = Github(github_token)
    user = github.get_user()
    login = user.login
    user.create_repo(repo_name_git, private=private)

    return f'https://github.com/{login}/{repo_name_git}.git'


def run_commands(commands: list):
    '''Runs the commands on shell.

    Args:
        commands (list): List of commands.add()
    '''
    for com in commands:
        os.system(com)

def create_local_repo(repo_name: str, path: str):
    '''Creates a local repo.

    Args:
        repo_name (str): Name of the repo to be created.
        github_token (str): Token to access Github.
        local (bool, optional): If the repo should be created only locally. Defaults to False.
        private (bool, optional): If the repo should be created on private mode. Defaults to False.
    '''
    os.mkdir(f'{path}/{repo_name}')
    os.chdir(f'{path}/{repo_name}')

    os_type = {'posix': ['touch README.md', 'touch .gitignore'],
               'nt': ['cd.> README.md', 'cd.> .gitignore']}

    commands = os_type[os.name] + ['git init',
                                   'git add .',
                                   'git commit -m "Initial commit"']

    run_commands(commands)

def sync_repos(repo_link: str):

    sync_commands = [f'git remote add origin {repo_link}',
                     'git branch -M main',
                     'git push -u origin main']

    run_commands(sync_commands)

def run():

    parser = init_parser()
    args = parser.parse_args()

    path = os.environ.get('PROJECTS')
    validate(args, path)
    github_token = os.environ.get('GIT_AUTOMATION')

    if not args.local:
        repo_link = create_github_repo(github_token, args.repo_name, args.private)

    create_local_repo(args.repo_name, path)

    if not args.local:
        sync_repos(repo_link)
        print('Git repository created and synced successfully!')
    else:
        print('Git repository created successfully!')

    os.system('code .')

if __name__ == "__main__":
    run()

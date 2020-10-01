import sys
import os
from github import Github
from time import sleep

def create_repo():
    '''
    Creates a Github repo and syncs with the local one, if sys.argv[2] is "".
    For a private repo, use: <create name_repo --private> or <create name_repo -p>
    For only a local repo, use: <create name_repo --local> or <create name_repo -l>
    '''
    if not 1 < len(sys.argv) < 4:
        print('Error! To use the create function type: create <repo_name> <l, private>')
        sys.exit(1)

    repo_name = str(sys.argv[1])
    flag = str(sys.argv[2]) if len(sys.argv) == 3 else ''
    path = os.environ.get('mp')
    if os.path.isdir(f'{path}/{repo_name}'):
        print('A repo with this name already exists! Please, try another name.')
        return sys.exit(1)
    git_token = os.environ.get('git')
    login = ''
    repo_name_git = "-".join(repo_name.split())
    if flag == '' or flag == '--private' or flag == '-p':
        github = Github(git_token)
        user = github.get_user()
        login = user.login
        if flag == '':
            user.create_repo(repo_name_git)
        else:
            user.create_repo(repo_name_git, private=True)

    commands = ['git init',
                f'git remote add origin https://github.com/{login}/{repo_name_git}.git',
                'cd.> README.md',
                'cd.> .gitignore',
                'git add .',
                'git commit -m "Initial commit"',
                'git branch -M master',
                'git push -u origin master']

    if flag == '-l' or flag == '--local':
        commands.pop(1)
        commands.pop()
        commands.pop()
    
    os.mkdir(f'{path}/{repo_name}')
    os.chdir(f'{path}/{repo_name}')

    for com in commands:
        os.system(com)
    if flag == '' or flag == '--private' or flag == '-p':
        print('Git repository created and synced successfully!')
    else:
        print('Git repository created successfully!')
    os.system('code .')
    sleep(1)
    os.system('exit')

if __name__ == "__main__":
    create_repo()
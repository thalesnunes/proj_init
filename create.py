import sys
import os
from github import Github

def create_repo():
    '''
    Creates a Github repo and syncs with the local one, if sys.argv[2] is "".
    For a private repo, use: <create name_repo private>
    For only a local repo, use: <create name_repo l>
    '''

    repo_name = str(sys.argv[1])
    flag = str(sys.argv[2])
    path = os.environ.get('mp')
    git_token = os.environ.get('git')
    login = ''

    if flag == '' or flag == 'private':
        github = Github(git_token)
        user = github.get_user()
        login = user.login
        if flag == '':
            user.create_repo(repo_name)
        else:
            user.create_repo(repo_name, private=True)

    commands = ['git init',
                f'git remote add origin https://github.com/{login}/{repo_name}.git',
                'cd.> README.md',
                'git add .',
                'git commit -m "Initial commit"',
                'git push -u origin master']

    if str(sys.argv[2]) == 'l':
        commands.pop(1)
        commands.pop()
    
    os.mkdir(f'{path}/{repo_name}')
    os.chdir(f'{path}/{repo_name}')

    for com in commands:
        os.system(com)
    if str(sys.argv[2]) == '':
        print('Git repository created and synced successfully!')
    elif str(sys.argv[2]) == 'l':
        print('Git repository created successfully!')
    os.system('code .')

if __name__ == "__main__":
    create_repo()
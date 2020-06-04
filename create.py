import sys
import os
from github import Github
from secrets import username, password

def create_repo():
    user = Github(username, password).get_user()
    user.create_repo(str(sys.argv[1]))
    print('Github repository created successfully!')
    
if __name__ == "__main__":
    create_repo()
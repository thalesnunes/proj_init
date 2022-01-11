import argparse
import os
from pathlib import Path
from typing import Any, List, Optional

from github import Github


def init_parser() -> argparse.ArgumentParser:
    """Initializes the command line parser.add()

    Returns:
        argparse.ArgumentParser: Command line parser with added arguments
    """
    parser = argparse.ArgumentParser(
        prog="create",
        description="Automate your workflow with create command."
    )
    parser.add_argument(
        "-l",
        "--local",
        dest="local",
        action="store_true",
        help="Creates your repo only locally.",
    )
    parser.add_argument(
        "-p",
        "--private",
        dest="private",
        action="store_true",
        help="Creates your repo in private mode.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        dest="path",
        action="store",
        help="Path where the repo is going to be created.",
    )
    parser.add_argument(
        "repo_name",
        metavar="<repo_name>",
        help="Name of your repo to be created."
    )
    return parser


def validate(args: Any):
    """Validates the input.

    Args:
        args (Any): Args from the command line.

    Raises:
        AssertionError: LOCAL and PRIVATE can't be used at same time.
        NameError: Duplicated repos.
    """
    if args.local == args.private is True:
        raise AssertionError("LOCAL and PRIVATE can't be used at same time.")

    if (args.path/args.repo_name).is_dir():
        raise NameError(
            "A directory with this name already exists! Please, try another name."  # noqa
        )


def create_github_repo(
        github_token: str,
        repo_name: str,
        private: Optional[bool] = False
) -> str:
    """Creates Github repo.

    Args:
        github_token (str): Token to access Github.
        repo_name (str): Name of the Github repo.
        private (Optional[bool]): Private or not. Defaults to False.

    Returns:
        str: Returns the github repo link.
    """
    repo_name_git = repo_name.replace(" ", "-")
    github = Github(github_token)
    user = github.get_user()
    login = user.login
    user.create_repo(repo_name_git, private=private)

    return f"https://github.com/{login}/{repo_name_git}.git"


def run_commands(commands: List[str]):
    """Runs the commands on shell.

    Args:
        commands (List[str]): List of commands.add()
    """
    for com in commands:
        os.system(com)


def create_local_repo(repo_name: str, path: Path):
    """Create a local repo.

    Args:
        repo_name (str): Name of repo to be created
        path (Path): Path of the repo
    """
    os.mkdir(path/repo_name)
    os.chdir(path/repo_name)

    os_type = {
        "posix": ["touch README.md", "touch .gitignore"],
        "nt": ["cd.> README.md", "cd.> .gitignore"],
    }

    commands = os_type[os.name] + [
        "git init",
        "git add .",
        'git commit -m "Initial commit"',
    ]

    run_commands(commands)


def sync_repos(repo_link: str):
    """Syncs the repo with remote.

    Args:
        repo_link (str): Link of remote repo
    """

    sync_commands = [
        f"git remote add origin {repo_link}",
        "git branch -M main",
        "git push -u origin main",
    ]

    run_commands(sync_commands)


def run():
    """Run cli tool.
    """

    parser = init_parser()
    args = parser.parse_args()

    args.path = Path(args.path or os.environ.get("PROJECTS") or os.getcwd())

    validate(args)
    github_token = os.environ.get("GIT_AUTOMATION")

    if not args.local:
        repo_link = create_github_repo(github_token, args.repo_name, args.private)  # noqa

    create_local_repo(args.repo_name, args.path)

    if not args.local:
        sync_repos(repo_link)
        print("Git repository created and synced successfully!")
    else:
        print("Git repository created successfully!")

    os.system(f"{os.environ.get('EDITOR')} .")


if __name__ == "__main__":
    run()

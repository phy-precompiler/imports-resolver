""" Retrieve top pypi project repositories. """

# imports
import random
from pathlib import Path
from typing import List, Optional
# from pprint import pprint

import requests
import git


# constants
PYPI_STATS_URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
REPO_DIR = Path(__file__).parent.parent.resolve() / 'tmp'


def get_repo_url(package_name: str) -> Optional[None]:
    """ retrieve git repository url of pypi package  """
    package_url = f"https://pypi.org/pypi/{package_name}/json"
    pypi_api_data = requests.get(package_url, timeout=600).json().get('info', {})

    return pypi_api_data.get('project_urls', {}).get('Source', None) or pypi_api_data.get('home_page', None)


def retrieve_top_pypi_packages(sample_n: int = 16, n: int = None) -> List[str]:
    """ retrieve name of most downloaded N pypi packages """
    # get top n package name
    n = n or sample_n

    pypi_stats_data = requests.get(PYPI_STATS_URL, timeout=600).json()
    top_n_data = pypi_stats_data['rows'][0: n]
    return random.sample([row['project'] for row in top_n_data], sample_n)


def clone_repo(package_name: str, repo_url: str = None) -> Optional[Path]:
    """ clone git repository to tmp directory """
    if not repo_url:
        repo_url = get_repo_url(package_name)
        
        if repo_url is None:
            return None

    if repo_url.startswith('https://github.com'):
        if repo_url.endswith('/'):
            repo_url.removesuffix('/')

        if not repo_url.endswith('.git'):
            repo_url += '.git'

        clone_to_dir = REPO_DIR / package_name
        if not clone_to_dir.exists():
            git.Repo.clone_from(repo_url, clone_to_dir)

        return clone_to_dir

    return None


# pylint: disable=missing-function-docstring
def main():
    for package_name in retrieve_top_pypi_packages(32, n=100):
        repo_url = get_repo_url(package_name)

        if repo_url:
            local_repo_dir = clone_repo(package_name, repo_url)
            print(f'Cloned {repo_url} to {local_repo_dir}')


if __name__ == '__main__':
    # main()
    # clone_repo('pandas', repo_url='https://github.com/pandas-dev/pandas')
    clone_repo('django', repo_url='https://github.com/django/django')
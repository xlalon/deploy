# -*- coding: utf8 -*-

import os
from git import Repo


GIT_REPO = os.path.dirname(os.path.dirname(__file__))


class GitProxy:

    def __init__(self):
        pass

    def pull(self):
        pass

    def fetch(self):
        pass

    def checkout(self):
        pass


if __name__ == '__main__':
    print(GIT_REPO)

#!/usr/bin/python3
"""Fabric script to delete out-of-date archives"""

from fabric.api import env, run, local, lcd
from datetime import datetime
from os.path import exists
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number < 1:
        number = 1
    try:
        # Local cleanup
        with lcd('versions'):
            local('ls -t | tail -n +{} | xargs rm -f'.format(number + 1))

        # Remote cleanup
        run('ls -t /data/web_static/releases | tail -n +{} | xargs rm -rf'.format(number + 1))

    except Exception as e:
        print(e)

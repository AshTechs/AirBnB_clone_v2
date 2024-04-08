#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.157.134.237', '54.242.154.151']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """

    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        folder = '/data/web_static/releases/{}'.format(filename.split('.')[0])
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(folder))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}'.format(folder, folder))
        run('rm -rf {}/web_static'.format(folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(folder))
        return True
    except:
        return False

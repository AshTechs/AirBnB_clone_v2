#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, run
from datetime import datetime
import os

env.hosts = ['54.157.134.237', '54.242.154.151']


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        local('mkdir -p versions')
        file_name = 'versions/web_static_{}.tgz'.format(now)
        local('tar -cvzf {} web_static'.format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """

    if not os.path.exists(archive_path):
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


def deploy():
    """
    Deploys an archive to your web servers
    """

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, '/tmp/')

        # Get archive filename without extension
        archive_filename = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/' + archive_filename.split('.')[0]

        # Create directory to uncompress archive
        run('mkdir -p {}'.format(archive_folder))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))

        # Delete the archive
        run('rm /tmp/{}'.format(archive_filename))

        # Delete old symbolic link
        run('rm /data/web_static/current')

        # Create new symbolic link
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        return True

    except Exception as e:
        print(e)
        return False

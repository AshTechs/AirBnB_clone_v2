#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.157.134.237', '54.242.154.151']


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

        # Delete old symbolic link if exists
        if exists('/data/web_static/current'):
            run('rm /data/web_static/current')

        # Create new symbolic link
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        return True

    except Exception as e:
        print(e)
        return False


def do_deploy_with_new_index(archive_path):
    """Distributes an archive to web servers and sets new index"""
    if do_deploy(archive_path):
        try:
            # Remove default index.html
            run('rm /data/web_static/releases/{}/index.html'.format(
                archive_path.split('/')[-1].split('.')[0]))

            # Upload custom index.html
            put('my_index.html', '/data/web_static/releases/{}/'.format(
                archive_path.split('/')[-1].split('.')[0]))

            return True

        except Exception as e:
            print(e)
            return False

    return False


def do_deploy_with_old_index(archive_path):
    """Distributes an archive to web servers and sets old index"""
    if do_deploy(archive_path):
        try:
            # Remove custom index.html if exists
            run('rm /data/web_static/releases/{}/my_index.html'.format(
                archive_path.split('/')[-1].split('.')[0]))

            # Upload default index.html
            put('0-index.html', '/data/web_static/releases/{}/index.html'.format(
                archive_path.split('/')[-1].split('.')[0]))

            return True

        except Exception as e:
            print(e)
            return False

    return False

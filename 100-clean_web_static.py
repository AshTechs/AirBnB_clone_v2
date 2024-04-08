#!/usr/bin/python3
"""Fabric script to clean up outdated archives"""

from fabric.api import env, local, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_clean(number=0):
    """Cleans up outdated archives"""
    number = int(number)
    if number < 1:
        number = 1
    else:
        number += 1

    # Clean local archives
    local("cd versions; ls -t | tail -n +{} | xargs rm -f".format(number))

    # Clean remote archives
    run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf"
        .format(number))


def do_pack():
    """Creates a compressed archive of web_static folder"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = 'versions/web_static_{}.tgz'.format(timestamp)
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(filename))
        return filename
    except Exception:
        return None


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, '/tmp/')

        # Get archive filename without extension
        archive_filename = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/' + \
            archive_filename.split('.')[0]

        # Create directory to uncompress archive
        run('mkdir -p {}'.format(archive_folder))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename,
                                            archive_folder))

        # Delete the archive
        run('rm /tmp/{}'.format(archive_filename))

        # Update symbolic link
        update_symlink(archive_folder)

        return True

    except Exception as e:
        print(e)
        return False


def update_symlink(archive_folder):
    """Updates the symbolic link"""
    current_link = '/data/web_static/current'
    run('rm -f {}'.format(current_link))  # Remove old link
    run('ln -s {} {}'.format(archive_folder, current_link))  # Create new link


def do_clean(number=0):
    """Cleans up outdated archives"""
    number = int(number)
    if number < 1:
        number = 1
    else:
        number += 1

    # Clean local archives
    local("cd versions; ls -t | tail -n +{} | xargs rm -f".format(number))

    # Clean remote archives
    run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs rm -rf"
        .format(number))

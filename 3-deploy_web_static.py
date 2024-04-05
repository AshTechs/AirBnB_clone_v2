#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

from fabric.api import env, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['34.204.61.94', '54.242.154.151']


def do_pack():
    """
    Compresses web_static folder into .tgz format
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
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

        # Update symbolic link
        update_symlink(archive_folder)

        return True

    except Exception as e:
        print(e)
        return False


def update_symlink(archive_folder):
    """
    Updates the symbolic link
    """
    current_link = '/data/web_static/current'
    run('rm -f {}'.format(current_link))  # Remove old link
    run('ln -s {} {}'.format(archive_folder, current_link))  # Create new link


def deploy():
    """
    Deploys the archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

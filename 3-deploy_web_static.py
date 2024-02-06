#!/usr/bin/python3
"""Deploy a new version of the web_static code"""

from fabric.api import local, run, env
from datetime import datetime  # Add this line to import datetime module
import os

env.hosts = ['54.162.37.159', '18.234.169.238']
env.user = 'ubuntu'


def do_pack():
    """Create a tar gzipped archive of the web_static folder"""
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_" + time_now + ".tgz"
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.failed:
        return None
    return file_name


def do_deploy(archive_path):
    """Deploy the archive to the servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, folder_name))
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(folder_name, folder_name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(folder_name))
        return True
    except:
        return False


def deploy():
    """Deploy the archive"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

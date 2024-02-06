#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import *
import os

env.hosts = ["54.162.37.159", "	18.234.169.238"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        print("Error: Archive does not exist")
        return False

    try:
        archive_name = os.path.basename(archive_path)
        dest_path = "/tmp/" + archive_name

        # Upload archive to /tmp directory on each server
        put(archive_path, dest_path)

        # Uncompress archive to /data/web_static/releases/<archive_name>
        folder_name = archive_name.replace('.tgz', '').split('/')[-1]
        remote_path = "/data/web_static/releases/" + folder_name
        run("mkdir -p " + remote_path)
        run("tar -xzf " + dest_path + " -C " + remote_path)

        # Remove archive from /tmp
        run("rm " + dest_path)

        # Move contents from extracted folder to its parent folder
        run("mv " + remote_path + "/web_static/* " + remote_path)

        # Remove symbolic link if exists
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s " + remote_path + " /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        print("Error:", str(e))
        return False

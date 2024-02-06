#!/usr/bin/python3
""" Fabric script to create and distribute an archive to web servers """

from fabric.api import local, env
from os.path import exists

env.hosts = ['ubuntu@54.162.37.159', 'ubuntu@18.234.169.238']

def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder """
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_" + time_now + ".tgz"
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.failed:
        return None
    else:
        return file_name

def deploy():
    """ Creates and distributes an archive to web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

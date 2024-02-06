#!/usr/bin/python3
""" Fabric script to delete out-of-date archives """

from fabric.api import run, env
from os import listdir

env.hosts = ['ubuntu@54.162.37.159', 'ubuntu@18.234.169.238']

def do_clean(number=0):
    """ Deletes out-of-date archives """
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1
    archives = sorted(listdir("versions"))
    archives_to_keep = archives[-number:]
    releases = run("ls /data/web_static/releases").split()
    releases_to_keep = releases[-number:]
    for archive in archives:
        if archive not in archives_to_keep:
            run("rm versions/{}".format(archive))
    for release in releases:
        if release not in releases_to_keep:
            run("rm -rf /data/web_static/releases/{}".format(release))


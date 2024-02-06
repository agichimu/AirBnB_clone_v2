from fabric import Connection

def deploy_html_file():
    with Connection('web-01') as c:
        c.put('0-index.html', '/data/web_static/releases/hbnb_static/')
        c.sudo('chown www-data:www-data /data/web_static/releases/hbnb_static/0-index.html')

    with Connection('web-02') as c:
        c.put('0-index.html', '/data/web_static/releases/hbnb_static/')
        c.sudo('chown www-data:www-data /data/web_static/releases/hbnb_static/0-index.html')

if __name__ == "__main__":
    deploy_html_file()

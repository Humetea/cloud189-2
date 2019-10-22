from flask import Flask, redirect

from cloud import Cloud

app = Flask(__name__)
cloud = Cloud(open('.cookies', 'r').read())


@app.route('/d/<path:path>')
def download(path):
    path = Cloud.path_format(path)

    cloud.cache_files(path)
    if path not in cloud.files:
        return 'File not exist'

    return redirect(cloud.download(path))


if __name__ == '__main__':
    app.run()

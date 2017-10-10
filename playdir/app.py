import os
import math

from flask import Flask, render_template, make_response, request, send_from_directory, redirect

from playdir import utils

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

PLAYLIST_FILENAME = 'playlist.m3u8'
MEDIA_EXTENSIONS = ('.mp3', '.flac', '.ts', '.mp4',)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # Remove any possible base directory
    if 'X-Playdir-Base' in request.headers:
        # Get rid of any leading slash since `path` is relative and will not include it
        relative_path = path.lstrip(request.headers['X-Playdir-Base'].lstrip('/'))
    else:
        relative_path = path

    # The absolute path of the directory on disk
    abs_dir = os.path.normpath(os.path.join(utils.config['media_root'], relative_path))

    print(abs_dir)

    is_playlist = False
    if abs_dir.endswith('/{}'.format(PLAYLIST_FILENAME)):
        is_playlist = True
        abs_dir = '/'.join(abs_dir.split('/')[:-1])

    # If we are listing a directory, always use a trailing slash for relative
    # paths in the template to work in a stateless way
    elif os.path.isdir(abs_dir) and not path.endswith('/'):
        return redirect('{}/'.format(path), 301)

    if os.path.isfile(abs_dir):
        return send_from_directory(
            utils.config['media_root'], relative_path)

    if not os.path.isdir(abs_dir):
        return 'not found', 404

    _, dirs, files = next(os.walk(abs_dir))
    dirs = sorted([d for d in dirs if not d.startswith('.')])
    files = sorted([f for f in files if not f.startswith('.')])

    files = [f for f in files if f.lower().endswith(MEDIA_EXTENSIONS)]

    if is_playlist:
        files = [(f, utils.map_attributes(abs_dir, f)) for f in files]
        max_duration = math.ceil(max([a['duration'] for f, a in files]))
        response = make_response(render_template('playlist.m3u8',
            path=path,
            files=files,
            max_duration=max_duration
        ))
        response.headers['Content-Type'] = 'application/x-mpegURL'

    else:
        response = make_response(render_template('list.html',
            path=path,
            playlist_filename=PLAYLIST_FILENAME,
            files=files,
            dirs=dirs))

    return response


if __name__ == '__main__':
    app.run(port=8005, debug=True)

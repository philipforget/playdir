import os
import re

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

# Any prefix to remove when constructing the relative on disk path. This could
# be empty for servers serving media from the root.
extension_re = re.compile(r'\.(mp3|mp4|flac|wav)$', re.IGNORECASE)

config = {
    'media_root': os.getenv('MEDIA_ROOT', '/media'),
}

def get_duration_for_filepath(filepath, default=0):
    """
    Return a duration for a given filepath or None

    """
    if filepath.endswith('.flac'):
        cls = FLAC
    elif filepath.endswith('.mp3'):
        cls = MP3
    else:
        return default

    try:
        return cls(filepath).info.length
    except Exception:
        pass
    return default


def get_id3_dict_or_none(filepath):
    try:
        return EasyID3(filepath)
    except Exception as e:
        return None


def map_attributes(abs_dir, rel_path):
    """
    Given a filepath and server path, attempt to discern the duration, artist, and title for the song.

    """
    filepath = os.path.join(abs_dir, rel_path)
    duration = get_duration_for_filepath(filepath)
    id3 = get_id3_dict_or_none(filepath)

    return {
        "duration": duration,
        "artist": " & ".join(id3.get('artist', [])) if id3 else None,
        "title": " & ".join(id3.get('title', [])) if id3 else None,
    }

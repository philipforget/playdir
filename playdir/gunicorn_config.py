import os

accesslog = '-'
access_log_format = ' '.join([
    '%(t)s',
    'client=%(h)s',
    'username=%(u)s',
    'request="%(r)s"',
    'method=%(m)s',
    'uri=%(U)s',
    'query="%(q)s"',
    'status=%(s)s',
    'protocol=%(H)s',
    'response_length=%(b)s',
    'referer="%(f)s"',
    'user_agent="%(a)s"',
    'request_time=%(L)s'
])
bind = '0.0.0.0:{}'.format(os.getenv('APP_PORT', 8005))
errorlog = '-'
loglevel = os.getenv('GUNICORN_LOGLEVEL', 'info')
worker_class = 'gevent'

debug = bool(os.getenv('DEBUG', False))
if debug:
    # pdb etc. will only work with one sync worker with a large timeout
    gunicorn_logfile = "/dev/null"
    gunicorn_loglevel = "error"
    timeout = 900000
    workers = 1
    worker_class = "sync"

# Reload gunicorn on file changes, not for production
reload = bool(os.getenv('GUNICORN_RELOAD', True))

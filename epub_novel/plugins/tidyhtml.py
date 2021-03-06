import six
import subprocess
from ebooklib.plugins.base import BasePlugin

# Recommend usage of
# - https://github.com/w3c/tidy-html5

def tidy_cleanup(content, **extra):
    cmd = []

    for k, v in six.iteritems(extra):

        if v:
            cmd.append('--%s' % k)
            cmd.append(v)
        else:
            cmd.append('-%s' % k)

    # must parse all other extra arguments
    try:
        p = subprocess.Popen(['tidy'] + cmd, shell=False,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, close_fds=True)
    except OSError:
        return 3, None

    p.stdin.write(content)

    (cont, p_err) = p.communicate()

    # 0 - all ok
    # 1 - there were warnings
    # 2 - there were errors
    # 3 - exception

    return p.returncode, cont


class TidyPlugin(BasePlugin):
    NAME = 'Tidy HTML'
    OPTIONS = {'char-encoding': 'utf8',
               'tidy-mark': 'no'
               }

    def __init__(self, extra=None):
        if extra is None:
            extra = {}
        self.options = dict(self.OPTIONS)
        self.options.update(extra)

    def html_before_write(self, book, chapter):
        if not chapter.content:
            return None

        (_, chapter.content) = tidy_cleanup(chapter.content, **self.options)

        return chapter.content

    def html_after_read(self, book, chapter):
        if not chapter.content:
            return None

        (_, chapter.content) = tidy_cleanup(chapter.content, **self.options)

        return chapter.content

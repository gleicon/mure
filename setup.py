import sys, os, os.path, subprocess
from setuptools.command import easy_install
import pkg_resources as pkgrsrc

from setuptools import setup
from distutils import log
log.set_threshold(log.INFO)

setup(
        name            = "mure",
        version         = "0.4",

        packages        = ['mure', ],
        zip_safe = False,
        install_requires = ['%s>=%s' % x for x in dict(
            gevent         = "0.13.6",
            kombu          = "1.5.1",
        ).items()],

        # metadata for upload to PyPI
        author          = "Gleicon Moraes",
        author_email    = "gleicon@gmail.com",
        keywords        = "actors kombu gevent queue concurrency workers",
        description     = "gevent/greenlet/kombu based actors for python",
        url             = "https://github.com/gleicon/mure",
    )


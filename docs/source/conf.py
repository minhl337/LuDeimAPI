# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import os
import sys
from configparser import RawConfigParser

import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.dirname(__file__))


sys.path.append(os.path.abspath('_ext'))
extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx'
]
templates_path = ['_templates']

source_suffix = ['.rst']

master_doc = 'index'
project = u'LuDeimAPI'
copyright = '2019 Topl LLC'
version = '0.0.3'
release = version
exclude_patterns = ['_build']
default_role = 'obj'
intersphinx_mapping = {
    'python': ('https://python.readthedocs.io/en/latest/', None),
    'django': ('https://django.readthedocs.io/en/1.9.x/', None),
    'sphinx': ('https://sphinx.readthedocs.io/en/latest/', None),
}
htmlhelp_basename = 'LuDeimAPI'

exclude_patterns = [
    # 'api' # needed for ``make gettext`` to not die.
]

language = 'en'

locale_dirs = [
    'locale/',
]
gettext_compact = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

# Activate autosectionlabel plugin
autosectionlabel_prefix_document = True

# sphinx-notfound-page
# https://github.com/rtfd/sphinx-notfound-page
notfound_context = {
    'title': 'Page Not Found',
    'body': '''
<h1>Page Not Found</h1>
<p>Sorry, we couldn't find that page.</p>
<p>Try using the search box or go to the homepage.</p>
''',
}
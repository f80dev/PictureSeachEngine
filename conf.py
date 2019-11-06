# -*- coding: utf-8 -*-

import sphinx_theme_pd


import sys, os

sys.path.insert(0, os.path.abspath('extensions'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.coverage', 'sphinx.ext.imgmath', 'sphinx.ext.ifconfig',
              ]

todo_include_todos = False
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = []
add_function_parentheses = True
# add_module_names = True
# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

project = u'PSE - Picture Seach Engine API'
copyright = u'2029, Hervé Hoareau'

version = '1.0'
release = ''

# -- Options for HTML output ---------------------------------------------------
html_theme = "sphinx_theme_pd"
html_theme_path = [sphinx_theme_pd.get_html_theme_path()]

html_title = project
# html_short_title = None
# html_logo = None
# html_favicon = None
html_static_path = ['_static']
html_domain_indices = False
html_use_index = False
html_show_sphinx = False
htmlhelp_basename = 'PSEdoc'
html_show_sourcelink = False


# -- Options for Code Examples output ---------------------------------------------------


code_example_dir = "code-example"
code_add_python_path = ["./py"]


################################################################################


def setup(app):
    from sphinx.util.texescape import tex_replacements
    tex_replacements += [(u'♮', u'$\\natural$'),
                         (u'ē', u'\=e'),
                         (u'♩', u'\quarternote'),
                         (u'↑', u'$\\uparrow$'),
                         ]
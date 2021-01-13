import setuptools

import duro

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name=duro.__title__,
    version=duro.__version__,
    description=duro.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=duro.__author__,
    author_email=duro.__author_email__,
    url=duro.__url__,
    license=duro.__license__,
    packages=['duro', 'duro.cmds', 'duro.models', 'duro.ui'],
    install_requires=['PyYAML'],
    entry_points={'console_scripts': ['duro=duro.__main__:run']},
)

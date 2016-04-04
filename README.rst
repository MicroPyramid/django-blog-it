Micro Blog
------------

.. image:: https://readthedocs.org/projects/micro-blog/badge/?version=latest
   :target: http://micro-blog.readthedocs.org/en/latest/?badge=latest

.. image:: https://travis-ci.org/MicroPyramid/micro-blog.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/micro-blog

.. image:: https://coveralls.io/repos/github/MicroPyramid/micro-blog/badge.svg?branch=master
   :target: https://coveralls.io/github/MicroPyramid/micro-blog?branch=master

.. image:: https://landscape.io/github/MicroPyramid/micro-blog/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/micro-blog/master
   :alt: Code Health

Simple blog package developed with Django.

Features:

- Dynamic blog articles
- Blog pages
- Contact us page (configurable)
- google analytics
- SEO compliant

Installation
--------------

1. Install microblog using the following command::

    pip install microblog

    (or)

    git clone git://github.com/micropyramid/microblog.git

    cd microblog

    python setup.py install


2. After installing/cloning this, add the following settings in the virtual env/bin/activate file::

    # Disquss details

    DISQUSSHORTNAME="Your Disquss Short Name"

    export DISQUSSHORTNAME

3. Use virtualenv to install requirements::

    pip install -r requirements.txt

You can try it by hosting on your own or deploy to Heroku with a button click.

Deploy To Heroku:

.. image:: https://www.herokucdn.com/deploy/button.svg
   :target: https://heroku.com/deploy?template=https://github.com/MicroPyramid/micro-blog

We welcome your feedback and support, raise issues if you want to see a new feature or report a bug.

  https://github.com/MicroPyramid/micro-blog/issues


You can view the complete documentation at http://micro-blog.readthedocs.org/en/latest/?badge=latest

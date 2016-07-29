django-blog-it
------------

.. image:: https://readthedocs.org/projects/django-blog-it/badge/?version=latest
   :target: http://django-blog-it.readthedocs.org/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/dm/django-blog-it.svg
    :target: https://pypi.python.org/pypi/django-blog-it
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-blog-it.svg
    :target: https://pypi.python.org/pypi/django-blog-it
    :alt: Latest Release

.. image:: https://travis-ci.org/MicroPyramid/django-blog-it.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/django-blog-it

.. image:: https://coveralls.io/repos/github/MicroPyramid/django-blog-it/badge.svg?branch=master
   :target: https://coveralls.io/github/MicroPyramid/django-blog-it?branch=master

.. image:: https://img.shields.io/github/license/micropyramid/django-blog-it.svg
    :target: https://pypi.python.org/pypi/django-blog-it/

.. image:: https://landscape.io/github/MicroPyramid/django-blog-it/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/django-blog-it/master
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

1. Install django-blog-it using the following command::

    pip install django-blog-it


            (or)

    git clone git://github.com/micropyramid/django-blog-it.git

    cd django-blog-it

    python setup.py install

2. Add app name in settings.py::

    INSTALLED_APPS = [
       '..................',
       'simple_pagination',
       'django_blog_it.django_blog_it',
       '..................'
    ]


3. After installing/cloning this, add the following settings in the virtual env/bin/activate file to start discussions on blog articles ::

    You can create your disqus account at https://disqus.com/profile/login/

    # Disquss details

    DISQUSSHORTNAME="Your Disquss Short Name"

    export DISQUSSHORTNAME
   
   # google api key for short url

    API_KEY="google api key"

    export API_KEY

   # google captcha

    GOOGLE_CAPTCHA_SITE_KEY="Site key"

    export GOOGLE_CAPTCHA_SITE_KEY

    GOOGLE_CAPTCHA_SECRET_KEY="Secret key"

    export GOOGLE_CAPTCHA_SECRET_KEY
   
   # Google Analytics Account

    GOOGLE_ANALYTICS_ID="UA-123456789"

    export GOOGLE_ANALYTICS_ID

   # Google Login
   
    GP_CLIENT_ID="google client id"
   
    export GP_CLIENT_ID

    GP_CLIENT_SECRET="secret key"

    export GP_CLIENT_SECRET
   
   # Facebook Login 
   
    FB_APP_ID="facebook app id"

    export FB_APP_ID

    FB_SECRET="023df180c6d868e76a02aec17134c843"

    export FB_SECRET
   
   # Default E-mail

    DEFAULT_EMAIL="noreply@djangoblogit.com"

    export DEFAULT_EMAIL


4. Use virtualenv to install requirements::

    pip install -r requirements.txt

You can try it by hosting on your own or deploy to Heroku with a button click.

Deploy To Heroku:

.. image:: https://www.herokucdn.com/deploy/button.svg
   :target: https://heroku.com/deploy?template=https://github.com/MicroPyramid/django-blog-it
   

We welcome your feedback and support, raise github ticket if you want to report a bug. Need new features? `Contact us here`_

.. _contact us here: https://micropyramid.com/contact-us/

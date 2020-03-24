django-blog-it's documentation v0.1:
=====================================

Introduction:
=============

django-blog-it is simple and completely customizable blog application. You can integrate it into your project and customise the blog application or just host it to post your articles.

Source Code is available in Micropyramid Repository(https://github.com/MicroPyramid/django-blog-it.git).

Modules used:
	* Pillow
	* Django Simple Pagination


Requirements
======================

======  ====================
Python  >= 3.5
Django  = 2.1
jQuery  >= 3
======  ====================

Installation Procedure
======================

1. Install django-blog-it using the following command::

    pip install django-blog-it

    		(or)

    git clone git://github.com/micropyramid/django-blog-it.git

    cd django_blog_it

    python setup.py install


2. After installing/cloning this, add the following settings in the virtual env/bin/activate file to start discussions on blog articles ::

	You can create/get your disqus account at https://disqus.com/profile/login/

    # Disquss details

    DISQUSSHORTNAME="Your Disquss Short Name"

    export DISQUSSHORTNAME

3. Use virtualenv to install requirements::

    pip install -r requirements.txt


Working modules
===============
* Create Blog Posts.
* A Complete Blog with articles, categories, tags, archievs.
* Blog Post History.
* Blog Post Trash Management.


Planned Modules
===============
* Blog pages
* google analytics
* SEO compliant
* Social Login.

We are always looking to help you customize the whole or part of the code as you like.



.. odbrasil documentation master file, created by
   sphinx-quickstart on Sat Jun 30 12:38:31 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

odbrasil: Open Data Brasil
==========================

Release v\ |version|. (:ref:`installation`)

**odbrasil** is an *Apache 2.0 licensed* Python module to extract Brazilian government open data. The aim of
the project is to provide an unified, organized and well-documented API to extract and parse
(typically into `Pandas <http://pandas.pydata.org>`_ data structures) the government open data.

Today we have some projects doing scraping of the open data, but these projects doesn't offer a parse for
`Pandas <http://pandas.pydata.org>`_ and do not have an unified and organized API, most of them are
just *scripts* created in a hurry on Hackatons and do not have any documentation.

The API we're working on is simple and easy-to-use, intended not only for programmers but also for statisticians
that doesn't have a strong background development.

We **really need** the community support in order to cover a great part of the API available for the
government open data, if you want to help, join us on Github. 

I have chosen the Pandas because it is becoming the *lingua franca* of the Python data analysis toolkits and
because it is integrated with `matplotlib <http://matplotlib.sourceforge.net/>`_ and `scipy/numpy <http://docs.scipy.org/doc/>`_ ecosystem.


Here is an example of what the API can do:

::

    >>> from odbrasil.legislativo import camara
    >>> api = camara.Deputados()
    >>> deputados = api.get_deputados()
    >>> deputados
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 512 entries, 0 to 511
    Data columns:
    anexo              512  non-null values
    email              512  non-null values
    fone               512  non-null values
    gabinete           512  non-null values
    idParlamentar      512  non-null values
    nome               512  non-null values
    nomeParlamentar    512  non-null values
    partido            512  non-null values
    sexo               512  non-null values
    uf                 512  non-null values
    dtypes: object(10)

    >>> vcounts = deputados.partido.value_counts()
    >>> vcounts
    PT       86
    PMDB     80
    PSDB     52
    PSD      48
    PP       39
    PR       36
    PSB      30
    DEM      28
    PDT      26
    PTB      20
    PSC      16
    PCdoB    12
    PV       10
    PRB       9
    PPS       9
    PTdoB     3
    PSOL      3
    PSL       1
    PRTB      1
    PRP       1
    PMN       1
    PHS       1
    >>> vcounts.plot(kind='bar')

.. image:: _static/partido_plot.png

::

    >>> uf_deputados = deputados.uf.value_counts()
    >>> uf_deputados.plot(kind='barh')

.. image:: _static/uf_plot.png    

See the API documentation for more information.

.. _installation:

Installation
============

You can use **pip** to install **odbrasil** module and its dependencies, it is recommended that you
have already installed scipy/numpy and matplotlib from your distro, in Ubuntu for instance:

::

    sudo apt-get install python-numpy python-scipy python-matplotlib

And to install **odbrasil**:

::

    pip install odbrasil

Simple and easy as that.


API Documentation
=================

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 4

   api

.. _license:

License
=======

   Copyright 2012 Christian S. Perone

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Contributors
------------

Christian S. Perone `[twitter] <http://www.twitter.com/tarantulae>`_ 
`[blog] <http://pyevolve.sourceforge.net/wordpress>`_ `[github] <https://github.com/perone>`_.



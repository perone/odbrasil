"""
odbrasil.servidores.scrap
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the methods to extract the information
present on on the government site for open data: 
http://www.portaldatransparencia.gov.br/servidores/index.asp

|
"""

import re
import numpy as np

import requests
from BeautifulSoup import BeautifulSoup

# Reference: http://www.portaldatransparencia.gov.br/servidores/index.asp
URL_BASE_PESQUISA = "http://www.portaldatransparencia.gov.br/servidores/Servidor-ListaServidores.asp"
URL_BASE_REMUNERACAO = "http://www.portaldatransparencia.gov.br/servidores/Servidor-DetalhaRemuneracao.asp"

def get_servidor_id(name):
    """ This function will load the ``IdServidor`` parameter from the government
    site, it will use scraping methods and not a REST API to do that. The ``name``
    parameter must be unique, otherwise an exception will be raised.

    :param name: The servidor name
    :rtype: The id of the servidor on the government database
    """
    params = {
        "bogus" : "1",
        "Pagina" : "1",
        "TextoPesquisa" : name,
    }
    req = requests.get(URL_BASE_PESQUISA, params=params)
    soup = BeautifulSoup(req.content)
    detalha = soup.findAll('a', href=re.compile("^Servidor-DetalhaServidor"))
    
    if len(detalha) > 1:
        raise RuntimeError("More than one detail to %s, len is %d" % (name, len(detalha)))

    if len(detalha) <= 0:
        raise RuntimeError("Unable to find the id for the name %s" % name)

    link = detalha[0]
    regex_idservidor = re.compile('IdServidor=(\d+)')
    id_servidor = regex_idservidor.findall(link["href"])[0]
    return id_servidor

def get_servidor_remuneracao_bruta(servidor_id):
    """ This function will load the month payment for the 'Servidor', it will
    use scraping methods and not a REST API to do that.

    :param servidor_id: The servidor id, returned by :func:`get_servidor_id`
    :rtype: The month payment of that 'Servidor'
    """

    params = {
        "IdServidor" : servidor_id,
        "Op" : "1",
    }
    req = requests.get(URL_BASE_REMUNERACAO, params=params)
    soup = BeautifulSoup(req.content)
    bruta = re.compile("bruta$")
    td_bruta = soup.findAll('td', text=bruta)
    if len(td_bruta) <= 0:
        return np.nan
    remuneracao_bruta = td_bruta[0].previous.nextSibling.next.text
    return float(remuneracao_bruta.replace(".", '').replace(",","."))



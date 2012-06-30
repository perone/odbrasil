"""
odbrasil.legislativo.camara
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the methods to extract the information
present on on the government site for open data:
    http://www2.camara.gov.br/transparencia/dados-abertos

:copyright: (c) 2012 by Christian S. Perone.
:license: Apache, see LICENSE for more details.
"""

import odbrasil

import xml.etree.cElementTree as et

import requests
import pandas

class RESTServiceClient(object):

    odbrasil_headers = {
        'User-Agent' : 'odbrasil/%s' % odbrasil.__version__,
    }

    def get(self, service, **params):
        req = requests.get(self.base_url + service,
            headers=self.odbrasil_headers, **params)

        req.raise_for_status()

        # Check if the data is the correct type
        if self.content_type not in req.headers['content-type']:
            raise RuntimeError('The endpoint didn\'t returned a xml data, returned %s'
                % req.headers['content-type'])

        return req

class Deputados(RESTServiceClient):
    base_url = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
    content_type = 'text/xml'

    def get_deputados(self, format='pandas', **params):
        req_deputados = self.get('ObterDeputados', **params)
        tree = et.fromstring(req_deputados.text.encode(req_deputados.encoding))
        xml_deputado_list = tree.findall('deputado')

        if format=='pandas':
            return pandas_parse_deputados(xml_deputado_list)
        else:
            return xml_deputado_list

def pandas_parse_deputados(xml_deputado_list):
    deputados_list = []

    for deputado in xml_deputado_list:
        deputado_dict = {}
        for child in deputado:
            if child.tag == 'comissoes':
                continue
            deputado_dict[child.tag] = child.text
        deputados_list.append(deputado_dict)

    pandas_frame = pandas.DataFrame(deputados_list)
    return pandas_frame

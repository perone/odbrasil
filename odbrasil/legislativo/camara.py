"""
odbrasil.legislativo.camara
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the methods to extract the information
present on on the government site for open data: 
http://www2.camara.gov.br/transparencia/dados-abertos

|
"""
import odbrasil

import xml.etree.cElementTree as et

import requests
import pandas

class RESTServiceClient(object):
    """ The base class used by other subclasses to retrieve data from 
    the government webservices. If you want to subclass this class, you
    have to define two class variables on your subclass, called ``base_url``
    and the expected ``content_type``. See :class:`Deputados` for reference.

    This class is responsible for keeping the common functionality used
    by the service clients, like using the **User-Agent** as **odbrasil/1.0**
    for instance.

    .. note:: you shouldn't use this :class:`RESTServiceClient` on your application
              except if you really need to customize the internals of the REST client.
    """

    odbrasil_headers = {
        'User-Agent' : 'odbrasil/%s' % odbrasil.__version__,
    }

    def get(self, service, **params):
        """ This method uses the ``baseurl`` parameter and concats the
        ``service`` parameter into it to create the request URL. Any
        extra param passed to this method by the ``params`` parameter will
        be redirected to the Requests request.

        :param service: the service, i.e. 'ObterDeputados'
        :param params: extra parameters to be used by Requests
        :rtype: the Requests request response
        """
        req = requests.get(self.base_url + service,
            headers=self.odbrasil_headers, **params)

        req.raise_for_status()

        # Check if the data is the correct type
        if self.content_type not in req.headers['content-type']:
            raise RuntimeError('The endpoint didn\'t returned a xml data, returned %s'
                % req.headers['content-type'])

        return req

class Deputados(RESTServiceClient):
    """ This class is responsible by accessing, extracting and parsing the data
    from the `Deputados <http://www.camara.gov.br/SitCamaraWS/Deputados.asmx>`_ 
    government endpoint. 
    """

    base_url = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
    content_type = 'text/xml'

    def get_deputados(self, format='pandas', **params):
        """ This method will get a Deputados list in various formats, use the
        ``format`` parameter to define which parameter you want to parse the
        data.

        :param format: "pandas" or "xml"
        :param params: extra parameters will be redirected to Requests
        :rtype: the parsed xml or the pandas `DataFrame`.
        """
        req_deputados = self.get('ObterDeputados', **params)
        tree = et.fromstring(req_deputados.text.encode(req_deputados.encoding))
        xml_deputado_list = tree.findall('deputado')

        if format=='pandas':
            return pandas_parse_deputados(xml_deputado_list)
        else:
            return xml_deputado_list

class Orgaos(RESTServiceClient):
    """ This class is responsible by accessing, extracting and parsing the data
    from the `Orgaos <http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx>`_ 
    government endpoint. 
    """

    base_url = 'http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/'
    content_type = 'text/xml'

    def get_orgaos(self, format='pandas', **params):
        """ This method will get a Orgaos list in various formats, use the
        ``format`` parameter to define which parameter you want to parse the
        data.

        :param format: "pandas" or "xml"
        :param params: extra parameters will be redirected to Requests
        :rtype: the parsed xml or the pandas `DataFrame`.
        """
        req_orgaos = self.get('ObterOrgaos', **params)
        tree = et.fromstring(req_orgaos.text.encode(req_orgaos.encoding))
        xml_orgao_list = tree.findall('orgao')

        if format=='pandas':
            return pandas_parse_only_attributes(xml_orgao_list)
        else:
            return xml_orgao_list
      
    def get_tipos_orgao(self, format='pandas', **params):
        """

        """
        req_tipos_orgao = self.get('ListarTiposOrgaos', **params)
        tree = et.fromstring(req_tipos_orgao.text.encode(req_tipos_orgao.encoding))
        xml_tipo_orgao_list = tree.findall('tipoOrgao')

        if format=='pandas':
            return pandas_parse_only_attributes(xml_tipo_orgao_list)
        else:
            return xml_tipo_orgao_list


def pandas_parse_deputados(xml_deputado_list):
    """ Method used to parse a xml parsed list of ``deputado``
    elements into a pandas `DataFrame`.

    :param xml_deputado_list: the xml parsed data returned by
                              calling :meth:`Deputados.get_deputados` with the
                              ``format`` as 'xml' instead of 'pandas'.
    :rtype: pandas 'DataFrame'
    """
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

def pandas_parse_only_attributes(xml_list):
    """ This method converts a list of xml elements containing only
    attributes (without childs) to a pandas `DatFrame`.

    :param xml_list: 
    :rtype: pandas `DataFrame`
    """

    elements_list = []

    for element in xml_list:
        elements_list.append(element.attrib)

    pandas_frame = pandas.DataFrame(elements_list)
    return pandas_frame


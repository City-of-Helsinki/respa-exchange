import logging

import requests
from lxml import etree
from requests_ntlm import HttpNtlmAuth

from respa_exchange.xml import NAMESPACES


class ExchangeSession(requests.Session):
    encoding = "UTF-8"

    def __init__(self, url, username, password):
        super(ExchangeSession, self).__init__()
        self.url = url
        self.auth = HttpNtlmAuth(username, password)
        self.log = logging.getLogger("ExchangeSession")

    def soap(self, request):
        """
        Send an EWSRequest by SOAP.

        :type request: respa_exchange.base.EWSRequest
        :rtype: lxml.etree.Element
        """
        envelope = request.envelop()
        body = etree.tostring(envelope, pretty_print=True, encoding=self.encoding)
        self.log.debug(
            "SENDING: %s",
            body.decode(self.encoding)
        )
        headers = {
            "Accept": "text/xml",
            "Content-type": "text/xml; charset=%s" % self.encoding
        }
        resp = self.post(self.url, data=body, headers=headers, auth=self.auth)
        return self._process_soap_response(resp)

    def _process_soap_response(self, resp):
        tree = etree.XML(resp.content)
        self.log.debug(
            "RECEIVED: %s",
            etree.tostring(tree, pretty_print=True, encoding=self.encoding).decode(self.encoding)
        )
        fault_nodes = tree.xpath(u'//s:Fault', namespaces=NAMESPACES)
        if fault_nodes:
            raise Exception(etree.tostring(fault_nodes[0]))
        resp.raise_for_status()
        return tree

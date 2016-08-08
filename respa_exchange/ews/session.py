import logging

import requests
from lxml import etree
from requests_ntlm import HttpNtlmAuth

from .xml import NAMESPACES


class SoapFault(Exception):
    def __init__(self, fault_code, fault_string, detail_element=None):
        self.code = fault_code
        self.text = fault_string
        self.detail_element = (detail_element if (detail_element is not None) else None)
        self.detail_text = (
            etree.tostring(self.detail_element, pretty_print=True)
            if (self.detail_element is not None)
            else None
        )
        super(SoapFault, self).__init__("%s (%s)" % (self.text, self.code))


    @classmethod
    def from_xml(cls, fault_element):
        fault_code_el = fault_element.find("faultcode")
        fault_text_el = fault_element.find("faultstring")
        return cls(
            fault_code=(fault_code_el.text if (fault_code_el is not None) else None),
            fault_string=(fault_text_el.text if (fault_text_el is not None) else None),
            detail_element=fault_element.find("detail")
        )


class ExchangeSession(requests.Session):
    """
    Encapsulates an NTLM authenticated requests session with special capabilities to do SOAP requests.
    """

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
        if not resp.content:
            resp.raise_for_status()
        tree = etree.XML(resp.content)
        self.log.debug(
            "RECEIVED: %s",
            etree.tostring(tree, pretty_print=True, encoding=self.encoding).decode(self.encoding)
        )
        fault_nodes = tree.xpath(u'//s:Fault', namespaces=NAMESPACES)
        if fault_nodes:
            raise SoapFault.from_xml(fault_nodes[0])
        resp.raise_for_status()
        return tree

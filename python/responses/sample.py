# -*- coding: utf-8 -*-
import responses
import requests
from werkzeug.urls import url_quote, iri_to_uri


@responses.activate
def test_my_api():
    protcol = 'http://'
    domain = u'ほげ.com'
    query = u'?q=ふが'

    url = protcol + domain
    # idna_url = protcol + domain.encode('idna')
    idna_url = iri_to_uri(url)

    responses.add(responses.GET, idna_url,
                  json={"error": "not found"}, status=404)

    resp = requests.get(url)

    print resp.json()
    assert resp.json() == {"error": "not found"}

    assert len(responses.calls) == 1
    #assert responses.calls[0].request.url == url_quote(u'http://hoge?q=ぐーぐる')
    assert responses.calls[0].response.text == '{"error": "not found"}'

@responses.activate
def test_redirect():

    url1 = 'http://base'
    url2 = 'http://redirect'

    responses.add(responses.GET,
                  url2,
                  json={'msg': 'redirected'},
                  status=200,
                  )

    responses.add(responses.GET,
                  url1,
                  status=302,
                  adding_headers={'Location': url2 + '/'}
                  )


    resp = requests.get(url1)

    assert resp.url == 'http://redirect/'

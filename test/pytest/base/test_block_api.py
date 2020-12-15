import requests
from pybgl import *
import base64


def test_get_block_last(conf):
    r = requests.get(conf["base_url"] + "/rest/block/last")
    assert r.status_code == 200
    d = r.json()["data"]
    assert 'height' in d
    assert 'hash' in d
    assert 'header' in d
    assert 'adjustedTimestamp' in d
    assert d['hash'] == rh2s(sha3_256(base64.b64decode(d["header"])[:80], hex=False))
    r = requests.get("https://api.bitaps.com/bgl/v1/blockchain/block/last")
    d_1 = r.json()["data"]
    assert d_1["block"]["height"] == d["height"]

def test_get_block_pointer(conf):
    r = requests.get(conf["base_url"] + "/rest/block/0")
    assert r.status_code == 200
    d = r.json()["data"]
    assert 'height' in d
    assert 'hash' in d
    assert 'header' in d
    assert 'adjustedTimestamp' in d

    r = requests.get(conf["base_url"] + "/rest/block/" + d["hash"])
    assert r.status_code == 200
    d2 = r.json()["data"]
    assert d['height'] == d2['height']
    assert d['hash'] == "00000018cdcfeeb4dfdebe9392b855cfea7d6ddb953ef13f974b58773606d53d"
    assert d['hash'] == d2['hash']
    assert d['header'] ==d2['header']
    assert d['adjustedTimestamp'] == d2['adjustedTimestamp']

    r = requests.get(conf["base_url"] + "/rest/block/ffff00000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
    assert r.status_code == 404

def test_get_last_n_blocks(conf):
    r = requests.get(conf["base_url"] + "/rest/blocks/last/2016")
    assert r.status_code == 200
    rd = r.json()["data"]
    for d in rd:
        assert 'height' in d
        assert 'hash' in d
        assert 'header' in d
        assert 'adjustedTimestamp' in d
        assert d['hash'] == rh2s(sha3_256(base64.b64decode(d["header"])[:80], hex=False))
    r = requests.get("https://api.bitaps.com/bgl/v1/blockchain/blocks/last/2016")
    rd_1 = r.json()["data"]
    for i in range(2016):
        assert rd_1[i]["height"] == rd[i]["height"]


def test_get_day_blocks(conf):
    r = requests.get(conf["base_url"] + "/rest/blocks/date/20201111")
    assert r.status_code == 200
    rd = r.json()["data"]
    for d in rd:
        assert 'height' in d
        assert 'hash' in d
        assert 'header' in d
        assert 'adjustedTimestamp' in d
        assert d['hash'] == rh2s(sha3_256(base64.b64decode(d["header"])[:80], hex=False))
    r = requests.get("https://api.bitaps.com/bgl/v1/blockchain/blocks/date/20190101")
    rd_1 = r.json()["data"]
    for i in range(len(rd_1)):
        assert rd_1[i]["height"] == rd[i]["height"]

def test_get_today_blocks(conf):
    r = requests.get(conf["base_url"] + "/rest/blocks/today")
    assert r.status_code == 200
    rd = r.json()["data"]
    for d in rd:
        assert 'height' in d
        assert 'hash' in d
        assert 'header' in d
        assert 'adjustedTimestamp' in d
        assert d['hash'] == rh2s(sha3_256(base64.b64decode(d["header"])[:80], hex=False))
    r = requests.get("https://api.bitaps.com/bgl/v1/blockchain/blocks/today")
    rd_1 = r.json()["data"]
    for i in range(len(rd_1)):
        assert rd_1[i]["height"] == rd[i]["height"]

def test_get_last_n_hours_blocks(conf):
    r = requests.get(conf["base_url"] + "/rest/blocks/last/1/hours")
    assert r.status_code == 200
    rd = r.json()["data"]
    for d in rd:
        assert 'height' in d
        assert 'hash' in d
        assert 'header' in d
        assert 'adjustedTimestamp' in d
        assert d['hash'] == rh2s(sha3_256(base64.b64decode(d["header"])[:80], hex=False))
    r = requests.get("https://api.bitaps.com/bgl/v1/blockchain/blocks/last/1/hours")
    rd_1 = r.json()["data"]
    for i in range(len(rd_1)):
        assert rd_1[i]["height"] == rd[i]["height"]

def test_get_block_headers(conf):
    r = requests.get(conf["base_url"] + "/rest/block/headers/10")
    assert r.status_code == 200
    d = r.json()["data"]
    assert len(d) == 2000
    r = requests.get(conf["base_url"] + "/rest/block/headers/10/2")
    assert r.status_code == 200
    d = r.json()["data"]
    assert len(d) == 2
    r = requests.get(conf["base_url"] + "/rest/block/headers/10000000")
    assert r.status_code == 404
    r = requests.get(conf["base_url"] + "/rest/block/0")
    h = r.json()["data"]["hash"]
    r = requests.get(conf["base_url"] + "/rest/block/headers/0/20")
    assert r.status_code == 200
    d = r.json()["data"]
    assert h == rh2s(base64.b64decode(d[0])[4:32+4])

def test_get_block_utxo(conf):
    r = requests.get(conf["base_url"] + "/rest/block/utxo/0")
    assert r.status_code == 200
    r = requests.get(conf["base_url"] + "/rest/block/utxo/100001")
    assert r.status_code == 200

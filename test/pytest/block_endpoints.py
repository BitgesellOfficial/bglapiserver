import unittest
import configparser
from pybgl import *
import base64
import zlib
import requests
from pprint import pprint

config_file =   "../config/bglapi-server.conf"
config = configparser.ConfigParser()
config.read(config_file)


option_transaction = True if config["OPTIONS"]["transaction"] == "on" else False
option_merkle_proof = True if config["OPTIONS"]["merkle_proof"] == "on" else False
option_address_state = True if config["OPTIONS"]["address_state"] == "on" else False
option_address_timeline = True if config["OPTIONS"]["address_timeline"] == "on" else False
option_blockchain_analytica = True if config["OPTIONS"]["blockchain_analytica"] == "on" else False
option_transaction_history = True if config["OPTIONS"]["transaction_history"] == "on" else False
option_block_filters = True if config["OPTIONS"]["block_filters"] == "on" else False

base_url = config["SERVER"]["api_endpoint_test_base_url"]


class BlockAPIEndpointsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nTesting blocks API endpoints:\n")

    def test_get_block_last(self):
        print("/rest/block/last:\n")
        r = requests.get(base_url + "/rest/block/last")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        self.assertEqual('height' in d, True)
        self.assertEqual('hash' in d, True)
        self.assertEqual('header' in d, True)
        self.assertEqual('adjustedTimestamp' in d, True)
        self.assertEqual(d['hash'], rh2s(sha3_256(base64.b64decode(d["header"]), hex=0)))
        print("OK\n")

    def test_get_block_pointer(self):
        print("/rest/block/{block_pointer}:\n")
        r = requests.get(base_url + "/rest/block/0")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        pprint(d)
        self.assertEqual('height' in d, True)
        self.assertEqual('hash' in d, True)
        self.assertEqual('header' in d, True)
        self.assertEqual('adjustedTimestamp' in d, True)
        r = requests.get(base_url + "/rest/block/" + d["hash"])
        self.assertEqual(r.status_code, 200)
        d2 = r.json()["data"]
        self.assertEqual(d['height'], d2['height'])
        self.assertEqual(d['hash'], "00000018cdcfeeb4dfdebe9392b855cfea7d6ddb953ef13f974b58773606d53d")
        self.assertEqual(d['hash'], d2['hash'])
        self.assertEqual(d['header'], d2['header'])
        self.assertEqual(d['adjustedTimestamp'], d2['adjustedTimestamp'])

        r = requests.get(base_url + "/rest/block/00000018cdcfeeb4dfdebe9392b855cfea7d6ddb953ef13f974b58773606d53d")
        self.assertEqual(r.status_code, 404)
        print("OK\n")


    def test_get_block_headers(self):

        print("/rest/block/headers/{block_pointer}:\n")
        r = requests.get(base_url + "/rest/block/headers/10")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        self.assertEqual(len(d), 2000)
        print("OK\n")

        print("/rest/block/headers/{block_pointer}/{count}:\n")
        r = requests.get(base_url + "/rest/block/headers/10/2")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        self.assertEqual(len(d), 2)
        r = requests.get(base_url + "/rest/block/headers/10000000")
        self.assertEqual(r.status_code, 404)
        r = requests.get(base_url + "/rest/block/0")
        h = r.json()["data"]["hash"]
        r = requests.get(base_url + "/rest/block/headers/0/20")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        self.assertEqual(h, rh2s(base64.b64decode(d[0])[4:32+4]))
        print("OK\n")


    def test_get_block_utxo(self):
        print("/rest/block/utxo/{block_pointer}:\n")
        r = requests.get(base_url + "/rest/block/utxo/0")
        self.assertEqual(r.status_code, 200)
        pprint(r.json())
        r = requests.get(base_url + "/rest/block/utxo/100001")
        self.assertEqual(r.status_code, 200)
        pprint(r.json())
        print("OK\n")

    def test_get_block_transactions(self):
        print("/rest/block/transactions/{block_pointer}:\n")
        r = requests.get(base_url + "/rest/block/transactions/100000")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        print("Transactions for block 100000:")
        for t in d:
            print("    ", t)
            if not t["coinbase"]:
                if option_transaction:
                    for i in t["vIn"]:
                        self.assertEqual("scriptPubKey" in  t["vIn"][i], True)
            if option_transaction:
                self.assertEqual(t["fee"] >= 0, True)

        r = requests.get(base_url + "/rest/block/last")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        h = d["height"]

        for k in range(h-10, h):
            q = time.time()
            r = requests.get(base_url + "/rest/block/transactions/" + str(k))
            s = time.time() - q
            self.assertEqual(r.status_code, 200)
            d = r.json()["data"]
            if option_transaction:
                for t in d:
                    if not t["coinbase"]:
                        for i in t["vIn"]:
                            if "scriptPubKey" not in  t["vIn"][i]:
                                print("error:::", t, k)
                                print(t)
                            self.assertEqual("scriptPubKey" in  t["vIn"][i], True)
                    self.assertEqual(t["fee"] >= 0, True)
            print(k, " block transactions %s [%s] OK" % (len(d), round(s,4)), r.json()["time"])


        print("OK\n")

    def test_get_block_filters(self):
        print("/rest/block/utxo/{block_pointer}:\n")
        r = requests.get(base_url + "/rest/block/filters/3/1000/"
                                    "000000000000e18a0f5e1aef936c80d4dd95c67b22cd65bbfa230c8f3dd4c3ac")
        self.assertEqual(r.status_code, 200)
        pprint(r.json())

        print("OK\n")
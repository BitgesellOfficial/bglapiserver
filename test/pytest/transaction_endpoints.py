import unittest
import configparser
from pybgl import *
import requests
from pprint import pprint
import base64
import random

config_file =   "../config/bglapi-server.conf"
config = configparser.ConfigParser()
config.read(config_file)


option_transaction = True if config["OPTIONS"]["transaction"] == "on" else False
option_merkle_proof = True if config["OPTIONS"]["merkle_proof"] == "on" else False
option_address_state = True if config["OPTIONS"]["address_state"] == "on" else False
option_address_timeline = True if config["OPTIONS"]["address_timeline"] == "on" else False
option_blockchain_analytica = True if config["OPTIONS"]["blockchain_analytica"] == "on" else False
option_transaction_history = True if config["OPTIONS"]["transaction_history"] == "on" else False
base_url = config["SERVER"]["api_endpoint_test_base_url"]

class TransactionsAPIEndpointsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nTesting blocks API endpoints:\n")

    def test_get_transaction(self):
        print("/rest/transaction/{tx_pointer}:\n")

        r = requests.get(base_url + "/rest/transaction/a6926608c5ced4254af392d28d7bfc58db131a61153d275efe860b7ee5e6808b")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        pprint(d)
        r = requests.get(base_url + "/rest/transaction/32564:0")
        self.assertEqual(r.status_code, 200)
        d2 = r.json()["data"]
        self.assertEqual(d["txId"], d2["txId"])

        r = requests.get(base_url + "/rest/transaction/79074de189d5d17d0fa5b6ff58f6b1da28248454166a43a4b40e1b79f7cc0543")
        self.assertEqual(r.status_code, 200)
        d = r.json()["data"]
        pprint(d)

    def test_get_transaction_merkleproof(self):
        print("/rest/transaction/merkleproof/{tx_pointer}:\n")

        def check_mpf(tx_id, h, i, calculate = False):

            if option_merkle_proof:
                if calculate:
                    print(h,":", i, "-> ", tx_id, " [get]: ", end="")
                    url = "/rest/transaction/merkle_proof/%s" % tx_id
                else:
                    print(h,":", i, "-> ", tx_id, " [calculate]: ", end="")
                    url = "/rest/transaction/calculate/merkle_proof/%s" % tx_id
                r = requests.get(base_url + url)
                result = r.json()
                d = result["data"]
                r = requests.get(base_url + "/rest/block/%s" % d["blockHeight"])
                self.assertEqual(r.status_code, 200)
                m_root = rh2s(base64.b64decode(r.json()["data"]["header"])[36:36 + 32])
                self.assertEqual(merkle_root_from_proof(base64.b64decode(d["merkleProof"]),
                                                        tx_id, d["blockIndex"]), m_root)
                print("OK", result["time"])
        for i in range(10):
            k = random.randint(0, 600000)
            print("block", k)
            r = requests.get(base_url + "/rest/block/transactions/%s" % k)
            self.assertEqual(r.status_code, 200)
            d = r.json()["data"]

            for i, t in enumerate(d):
                check_mpf(t, k, i, False)
                check_mpf(t, k, i, True)







        print("OK\n")





    # def test_get_transaction_hash_by_pointer(self):
    #     print("/rest/transaction/hash/by/blockchain/pointer/{tx_blockchain_pointer}:\n")
    #     r = requests.get(base_url + "/rest/transaction/hash/by/blockchain/pointer/7:0")
    #     self.assertEqual(r.status_code, 200)
    #     pprint(r.json())
    #     print("OK\n")


    # def test_get_transactions_hash_by_list(self):
    #     print("/rest/transactions/hash/by/blockchain/pointer/list:\n")
    #     r = requests.post(base_url + "/rest/transactions/hash/by/blockchain/pointer/list",
    #                       json=["4:0", "0:5"])
    #     self.assertEqual(r.status_code, 200)
    #     pprint(r.json())
    #     print("OK\n")
    #
    # def test_get_transactions_by_list(self):
    #     print("/rest/transactions/by/pointer/list:\n")
    #     r = requests.post(base_url + "/rest/transactions/by/pointer/list",
    #                       json=["9:0",
    #                             "8:1", "300000:2", "c09e98f862e9f62f6f560a48d4ab1fed0ffceaa64eaa2fdf93196ccec6842a86"])
    #     self.assertEqual(r.status_code, 200)
    #     pprint(r.json())
    #     print("OK\n")
    #
    #
    # def test_get_transactions_merkle_proof(self):
    #     if not option_merkle_proof: return
    #
    #     print("/rest/transaction/merkle_proof/{tx_pointer}:\n")
    #     r = requests.get(base_url + "/rest/transaction/merkle_proof/"
    #                                 "c09e98f862e9f62f6f560a48d4ab1fed0ffceaa64eaa2fdf93196ccec6842a86")
    #     self.assertEqual(r.status_code, 200)
    #     pprint(r.json())
    #     print("OK\n")

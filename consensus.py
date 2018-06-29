'''
Oasis Chain

'''

import requests
from bson import json_util
import json

from block import Block
import datetime as date
import config


# Data structures
CONSENSUS = "proof-of-service"
blockchain = []
this_nodes_transactions = []		# Store the txs
miner_address = "c924da40248d517045a700f41a2fe1468f09e8ed67775c205fb5f2ff9da34bb7"

# Let there be light
def create_genesis_block():
  print("Creating genesis block.")
  blockchain.append(Block(0, date.datetime.now(), {CONSENSUS: 9, "transactions": None}, "0"))
  print(str(blockchain[0].hash))

def get_chain():
	return blockchain

# TODO: delegate anvio_io service
def proof_of_service(last_proof):
	# Create a variable that we will use to find our next proof of work
	incrementor = last_proof + 1

	# check if divisible by 9
	while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
		incrementor += 1

	return incrementor


def _find_new_chains():
  # Get the blockchains from every other node
  other_chains = []
  for node_url in config.PEER_NODES:
    blocks = requests.get(node_url + "/blocks").content
    chain = json.loads(blocks)
    other_chains.append(chain)
  return other_chains

def find_longest_chain():
  global blockchain
  msg = "Current chain is the longest one.<br>" + str(len(blockchain)) + "<----<br>"
  # Get the blocks from other nodes
  other_chains = _find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  new_longest_chain = blockchain
  for chain in other_chains:
    if len(new_longest_chain) < len(chain):
      msg = "Found longer chain. Reset done.<br>"
      new_longest_chain = chain
      #reset_chain(new_longest_chain)
      blockchain[:] = []
      for aBlock in new_longest_chain:
          #msg += json.dumps(aBlock,default=json_util.default)
          anIndex = aBlock['index']
          aTimestamp = aBlock['timestamp']
          aData = aBlock['data']
          aPreviousHash = aBlock['previous_hash']
          aHash = aBlock['hash']

          blockchain.append(Block(anIndex, aTimestamp, aData, aPreviousHash, aHash))	
      msg += str(len(blockchain)) + "<----<br>"
  # If the longest chain isn't ours,
  # then we stop mining and set
  # our chain to the longest one
  return (msg, new_longest_chain)
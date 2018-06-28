'''
Oasis Chain

'''
from flask import Flask
from flask import request

import json
from bson import json_util

import datetime as date

from block import Block
import consensus
from consensus import blockchain, CONSENSUS, this_nodes_transactions, miner_address

node = Flask(__name__)

debug = True

# Flask Routing functions 
@node.route('/', methods=['GET'])
def index():
  return '''<h1>/**** OASIS CHAIN ****/</h1>
            <h2>Avaiable API commands:</h2>
            <h3>/txion</h3>
            Method: Post, E.g. curl "url:5000/txion" -H "Content-Type:applicaiton/json" -d '{"from":"tai","to":"chris","amount":3}' <br>
            <h3>/blocks</h3>
            Method: Get, list currenct blocks <br>
            <h3>/test</h3>
            Method: Test consensus function, if found longer chain, reset current<br>
          '''
  

# Flask URL-funciton mappings
@node.route('/txion', methods=['POST'])
def transaction():

  new_txion = json.loads(request.data.decode("utf-8"))
  print "DEBUG: new json:", str(new_txion)

  # Then we add the transaction to our list
  this_nodes_transactions.append(new_txion)

  if debug:
      print "New transaction"
      print "FROM: {}".format(new_txion['from'].encode('ascii','replace'))
      print "TO: {}".format(new_txion['to'].encode('ascii','replace'))
      print "AMOUNT: {}\n".format(new_txion['amount'])
  
  return "Server: Transaction submission successful\n"
  

@node.route('/blocks_raw', methods=['GET'])
def get_blocks_raw():
  a_cur_chain = consensus.get_chain()
  
  msg = ""
  for aBlock in a_cur_chain:
    msg += str(aBlock)
  
  return msg

@node.route('/blocks', methods=['GET'])
def get_blocks():
  
  chain_to_send = []

  a_cur_chain = consensus.get_chain()
  
  for aBlock in a_cur_chain:
    chain_to_send.append({
      "index": str(aBlock.index),
      "timestamp": str(aBlock.timestamp),
      "data": str(aBlock.data),
      "hash": aBlock.hash
    })

  msg = json.dumps(chain_to_send,default=json_util.default)
  return msg


@node.route('/test', methods=['GET'])
def test():
    # global blockchain
  
    msg,lchain = consensus.find_longest_chain()
    
    msg = "test:" + msg + "<br><hr>NEW LONGEST CHAIN<br>" + str(len(lchain)) +  "<br><hr>CURRENT CHAIN<br>" + str(len(blockchain))
    return msg


# This funciton should not be exposed
@node.route('/mine', methods = ['GET'])
def mine(): 
  last_block = blockchain[-1] # Get last element

  if debug:
    print "Dump data from last block", str(last_block.data)

  last_proof = last_block.data[CONSENSUS]
 
  # The program will hang here until a new POW is found
  proof = consensus.proof_of_service(last_proof)
  # Once we find a valid proof of work,
  # we know we can mine a block so 
  # we reward the miner by adding a transaction
  this_nodes_transactions.append(
    { "from": "Oasis Network", "to": miner_address, "amount": 1 }
  )
  # Gather data 
  new_block_data = {
    CONSENSUS: proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # Empty transaction list
  this_nodes_transactions[:] = []
  
  # Create new block
  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)
  # Let the client know we mined a block
  return json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "\n"
#--------------------------------------------------------


def setup_app(node):
   # All your initialization code
   print "Welcome to Oasis Chain"
   consensus.create_genesis_block()
   
setup_app(node)

if __name__ == '__main__':
  node.run(host='0.0.0.0', port=5555)

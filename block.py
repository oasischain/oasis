'''
Oasis Chain

Definition of a Block
'''
import hashlib as hasher

class Block:
  def __init__(self, index, timestamp, data, previous_hash, self_hash = None):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    
    if self_hash is None:
      self.hash = self.hash_block()
    else:
      self.hash = self_hash
  
  def hash_block(self):
    sha = hasher.sha256() # Yep
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()
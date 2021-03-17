# My First Bitcoin Miner
For the people who are curious to understand in a simplified setup:
- **How the Bitcoin blockchain works**
- **How mining works**

For a complete implementation (that can actually mine!), please browse this repository https://github.com/jgarzik/pyminer.

This miner is not connected to the bitcoin network and is a very simplified version of what would be a real bitcoin miner. The purpose of this implementation is to provide a basic comprehension of the mining logic.

## What are bitcoin miners really solving?

### Step 1

At a high level, the miner software takes a list of active transactions, and then groups them together in something called a "block".

Or more *accurately stated*: The miner software converts all the transactions into a summary view called a "merkle root", and hashes it, which is representative of the transactions.

### Step 2

The mining software then converts this to into a binary format called a Block Header, which also references the previous blocks (also called a chain).

```
Field           Purpose                          Updated when...               Size (Bytes)
Version         Block version number             You upgrade the software and   4
                                                 it specifies a new version 

hashPrevBlock   256-bit hash of the previous     A new block comes in          32
                block header    
hashMerkleRoot  256-bit hash based on all        A transaction is accepted     32
                the transactions in the block       

Time            Current timestamp as seconds     Every few seconds              4
                since 1970-01-01T00:00 UTC  

Bits            Current target in compact format   The difficulty is adjusted   4

Nonce           32-bit number (starts at 0)       A hash is tried (increments)  4
```

### Step 3

The miner hardware changes a small portion of this block called a "nonce".

### Step 4

The block header is hashed and compared to the Target as if it were simply a large number like 10,000,000 > 7,000,000 (the real numbers are much bigger, and in hex). The target is compressed and stored in each block in a field called bits.

An expanded target looks like this:

```
  Target   0000000000000083ef00000000000000000000000000000000000000000000000
```

And the goal is to make sure the SHA256 hash of the block is less than this value. In the example below "83ee" is smaller than "83ef"

To simplify this concept, you can ballpark the target by counting the leading zeros (as the other answer here explains). Here is an example:

Here is a sample block with transactions you can view on BlockChain.info. Look in the upper right hand corner of the webpage for this hash:

```
   Hash 0000000000000083ee9371ddff055eed7f02348e4eda36c741a2fc62c85bc5cf
```

That previous hash was from today and has 14 leading zeroes. Let's compare that to what was needed 3 years ago with block 100 which has 8 leading zeros.

```
   Hash 00000000a8ed5e960dccdf309f2ee2132badcc9247755c32a4b7081422d51899
```

### Summary

So at the end of the day, all a miner does is:

- Take a block header as input.
- Change the nonce.
- Test if the Block Header hash is less than the Target. If it is, you win.
- Go to step 2 (or go to step 1 if someone else won the block).


## References
- https://bitcoin.stackexchange.com/questions/8031/what-are-bitcoin-miners-really-solving
- https://en.bitcoin.it/wiki/Difficulty
- https://en.bitcoin.it/wiki/Target
- https://bitcoin.stackexchange.com/questions/30467/what-are-the-equations-to-convert-between-bits-and-difficulty
- https://stackoverflow.com/questions/22059359/trying-to-understand-nbits-value-from-stratum-protocol/22161019#22161019
- https://en.bitcoin.it/wiki/Nonce

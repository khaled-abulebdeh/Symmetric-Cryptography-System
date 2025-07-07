# README

## Project: DES Implementation and Meet-in-the-Middle Attack on 3DES

### Overview

This project demonstrates the design, implementation, and cryptanalysis of symmetric key cryptosystems using the Data Encryption Standard (DES) and Triple DES (3DES).  

It includes a full DES implementation built from scratch, as well as a practical cryptanalytic attack on a reduced-strength variant of 3DES using a Meet-in-the-Middle (MITM) approach.

---

## DES Implementation

### Description

The DES module provides a complete implementation of the standard 64-bit block cipher algorithm. All cryptographic primitives were implemented manually, without using external libraries, to ensure a deep understanding of each transformation.

Key features:

- **Initial and Final Permutations**  
- **16-round Feistel network**, with:
  - Expansion permutation
  - XOR with subkeys
  - S-Box substitutions
  - P-Box permutation
- **Key schedule** for generating 16 unique round keys

All operations are implemented at the bit level to accurately reproduce the behavior of DES and allow precise control and analysis.


### Usage

- Encrypt and decrypt 64-bit data blocks using 56-bit keys (excluding parity bits).
- All functions can be reused or integrated into higher-level cryptographic applications.
- The codebase is structured to facilitate future extensions and analyses, such as avalanche effect studies or key schedule visualization.

---

## Meet-in-the-Middle Attack on 3DES

### Description

This module implements a cryptanalytic Meet-in-the-Middle (MITM) attack against a variant of 3DES. In this system, two DES keys are used in the following structure:


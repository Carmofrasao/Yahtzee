# Yahtzee
Work for the Networking 1 subject in the Computer Science course at the Federal University of Paraná.

Done by Anderson Frasão and Eduardo Gobbo.

Objective

To implement the game developed in class (a variant of Yahtzee) with a Ring Network communication structure with baton passing.

Implementation

Due to the use of variables that require less than 8 bits for their representation, a python library was used to manipulate values with n bits in the fields of the message package. To install this package, simply install the latest version of pip and type

> pip install bitstring

With the library installed, just run

> python pcx.py

Where x represents the machine number of each player, i.e. integers from 1 to 4.

# Golay 24 encoder and decoder

A python implementation of a extended binary Golay code. A binary Golay code (G<sub>24</sub>) whose parameters are (24,12,8), codified word length, source word length and minimum distance, respectively.

His generator matrix is of the form *G* = (*I<sub>12</sub>A*) . *I<sub>12</sub>* is the identity matrix of order 12 and *A* is a 12 x 12 square matrix.

For more information about Golay codes check this sources:

[insert sources here]

# Description

The program will take an input from the user which will be the source word to encode with Golay, then user will have the opportunity to introduce errors. Once the errors are introduced two things will happen:

- If the errors are odd and equals or larger than 5 the code will ask for retransmission since is impossible to correct.
- If there are no errors or the errors are less than 5 it will be decoded.
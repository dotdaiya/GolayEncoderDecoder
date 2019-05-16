# Golay 24 encoder and decoder


[Description](https://github.com/adelfuns/GolayEncoderDecoder#description)

[Encoding](https://github.com/adelfuns/GolayEncoderDecoder#encoding)

[Decoding](https://github.com/adelfuns/GolayEncoderDecoder#decoding)

[Running the app](https://github.com/adelfuns/GolayEncoderDecoder#running-the-app)

___

A python implementation of a extended binary Golay code. A binary Golay code (G<sub>24</sub>) whose parameters are (24,12,8), codified word length, source word length and minimum distance, respectively.

His generator matrix is of the form *G* = (*I<sub>12</sub>A*) . *I<sub>12</sub>* is the identity matrix of order 12 and *A* is a 12 x 12 square matrix.

For more information about Golay codes check this sources:


[Encoding-Decoding](https://www.maplesoft.com/applications/view.aspx?SID=1757&view=html)

[In-depth explanation](http://www.math.ualberta.ca/~hongchen/m422/Chap%205.pdf)

## Description

The program will take an input from the user which will be the source word to encode with Golay, then user will have the opportunity to introduce errors. Once the errors are introduced two things will happen:

- If the errors are larger than 4 the code will ask for retransmission since is impossible to correct.
- If there are no errors or the errors are less than 3 it will be decoded.


## Encoding 

To encode a given source of 12 bits you need the generator Matrix for a binary Golay code (G<sub>24</sub>). Once you have the matrix, you just have to multiply the given word and the generator matrix of the form G* = (*I<sub>12</sub>A*).

## Decoding

To decode a received word we need to check errors that may have been introduced in a noisy channel. Then the code will run the decodification algorithm that will check for errors. As already stated in the description, with more that 3 errors the code will ask for retransmission. If it is less or equals that three the algorithm will decode the word correcting the errors. 



## Running the app

To execute the app you need Python 3. To run in just type from your OS command line interface: `python app.py`

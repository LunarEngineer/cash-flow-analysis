# Cash Flow Analysis

This sets up a simple cash flow analysis application using Numpy and Streamlit.

## Transactional Simulator

This is by no stretch of the imagination a replacement for a true simulation software. I built this because:
1. My wife wanted me to run some analyses with 'what if' style questions.
2. I wanted to play with streamlit and Polars.
3. I wanted to play around some more with Ray and Numpy and build a distributed computation engine.
4. I love to over-engineer things.

You should not be using this to replace something like SimPy.
This is just a labor of love.

## How does this work?

Every transaction is a custom class which undertands:

1. How to read a vector that represents 'current state' (1 x simulation width).
2. How to appropriately update either the 'current state' or another simulation object.

## Custom CSS

Jordan, please make me awesome custom CSS?
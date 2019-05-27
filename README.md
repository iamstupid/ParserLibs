# ParserLibs
A few hand-made utilities for building a parser.

## DFAGen

DFAGen is a simple DFA Generator to read a DFA Descriptor and generate a simple DFA Lexer(CPP). The lexer generated is almost dependency-free (only c stdlib and C++ vector) and pretty short (1-3 kilobytes).

An example is provided, which should be quite self-explanatory.

Usage: `python DFAGen.py DFADescriptionFile OutputCode.cpp`

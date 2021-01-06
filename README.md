<h1> Jack- Compiler</h1>
<p>The Jack-Compiler compiles a program written in Jack and generatets VM code.</p>

## Table of Contents

1. [Language](#Language)
2. [Introduction](#introduction)
5. [Supported OS](#supported-os)
6. [Internal tools](#Internal-tools)

---

## Language

This program is written in Python
<br>

## Introduction

The first step the program does is to lexically analyzes a Jack program into a stream of tokens.<br>
Then, it parses it into it's formal structure. It's done by recursively creates a "derivation tree".<br>
The program creates a symbol-table and generates VM code.
<br>


## Supported OS

I'm developing on Linux and macOS, and the library was tested on Linux.

## Internal tools

- The program uses 'sys' and 'os' libraries
    

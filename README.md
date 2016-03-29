# TeXDown - Markdown inspired LaTeX solution

## Introduction

I created this small script to hopefully improve my quality of life while
typesetting things with LaTeX. I found writing TeX to be annoying in many ways
that modern markdown-style languages try to address - Once you're used to TeX,
it's easy to write, but it never becomes easy to read, especially when writing
formulas. See this example, from a graph theory course I took recently:
```
\[
\sum_{v \in V}(\text{deg$v$})^{2} \geq \frac{\left(
\sum_{v\in V}\text{deg}v\right)^{2}}{n} = \frac{(2m)^{2}}{n}
\]
```

This produces much simpler output, but it's quite difficult to parse what the
code is supposed to do. The end goal of this project would look simpler, but
so far only a few minor changes have been implemented.

## Usage

Currently, the script texstream.py takes in a header .tex file,
a .td input file and outputs a .tex file, processing with the following rules:

- Backticks are used as math mode delimiters, both inline and in blocks
- The title and author are specified in the first two lines of the .td file
- Imports and other metadata are specified in a header .tex file, which will
  commonly be shared between a few .tex files

## Planned features

A couple other things I'd like to implement:

- Unicode characters converted into things like \in or \geq
- Packages imported based on whether or not their commands are used

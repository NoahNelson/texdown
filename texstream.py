import sys

class Texstream:

    def __init__(self, inf, headf):
        self.inHeader = True
        self.inBlockMath = False
        self.ended = False
        self.beginning = 0 
        # beginning is nonzero when streaming the inner lines in above dict
        self.lineno = 0
        self.inFile = open(inf, 'r')
        self.headFile = open(headf, 'r')
        self.title = ""
        self.author = ""
        self.pnumber = None # Problem number, if available
        # get title, author, problem set number if available.
        for line in self.inFile:
            if line.startswith("# "):
                self.title = line[2:-1]
            elif line.startswith("## "):
                self.author = line[3:-1]
            elif line.startswith("### "):
                self.pnumber = int(line[4:-1])
        self.inFile.seek(0, 0) # return to beginning of input file
        self.usedtitle = False
        self.usedauthor = False

    def __del__(self):
        self.inFile.close()
        self.headFile.close()

    def __iter__(self):
        return self

    def next(self):
        if self.inHeader:
            # attempt to read a line from the header file
            line = next(self.headFile, None)
            if line is None:
                self.inHeader = False
                return "\n" # New line between header and content
            else:
                # Check if it's time to insert a name or title
                if line.startswith("\\newcommand{\\name}") \
                        and self.author != "":
                    self.usedauthor = True
                    return "\\newcommand{\\name} {%s}\n" % self.author
                elif line.startswith("\\newcommand{\\settitle}") \
                        and self.title != "":
                    self.usedtitle = True
                    return "\\newcommand{\\settitle} {%s}\n" % self.title
                elif line.startswith("\\newcommand{\\pnumb}") \
                        and self.pnumber is not None:
                    return "\\newcommand{\\pnumb} {%d}\n" % self.pnumber
                # otherwise, pass along the line the way it was.
                return line
        elif self.beginning > 0 and self.beginning < 5:
            line = innerlines[self.beginning]
            self.beginning += 1
            return line
        else: # in the input .td file
            line = next(self.inFile, None)
            if line == None:
                if self.ended:
                    raise StopIteration()
                else:
                    self.ended = True
                    return "\\end{document}\n"
            if line.startswith("# "):
                if not self.usedtitle:
                    # Pass along the title
                    self.lineno += 1
                    return "\\title{%s}\n" % line[2:-1]
                else:
                    return "\n"
            elif line.startswith("## "):
                if not self.usedauthor:
                    # Pass along the author
                    self.lineno += 1
                    self.beginning += 1
                    return "\\author{%s}\n" % line[3:-1]
                else:
                    return "\n"
            elif line.startswith("#"):
                # Can't pass any hashtag meta-lines
                return "\n"
            elif line == '`\n' and not self.inBlockMath: # begin block math
                self.inBlockMath = True
                return '\\[\n'
            elif line == '`\n' and self.inBlockMath: # end block math
                self.inBlockMath = False
                return '\\]\n'
            else:
                return line.replace('`', '$')


def write_to_file(instream, outf):
    outFile = open(outf, 'w') # Should check if already exists
    for line in instream:
        outFile.write(line)
    outFile.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage: %s <infile> <headerfile> <outfile>" % sys.argv[0]
        exit()
    print "Running test of texstream."
    inf = sys.argv[1]
    headf = sys.argv[2]
    outf = sys.argv[3]
    stream = Texstream(inf, headf)
    write_to_file(stream, outf)

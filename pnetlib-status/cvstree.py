#! /usr/bin/python
# change if you like

# GPL--need I say more? (C)2002 Stephen Compall.

from os.path import isfile, abspath, join

import os, os.path, re, time

lineparse = re.compile(r'^/(?P<filename>.+?)/.*?/(?P<date>.+?)//$', re.M)

"""cvsmoddate--a class for looking up the date of a file in a CVS tree.

I used bad programming design to create this class, but it works."""

def appendentries(dict, dir, ls):
    entryfile = os.path.join(dir, "CVS", "Entries")
    if isfile(entryfile):
        readfromthis = open(entryfile, "r")
        for line in readfromthis.readlines():
            try:
                entry = lineparse.search(line).groupdict()
                dict[abspath(join(dir, entry["filename"]))] = entry["date"]
            except AttributeError:
                pass
        # fix 1: close the Entries file
        readfromthis.close()

class cvsmoddate:
    def __init__(self, root):
        """It doesn't really matter where you choose, as long as there are CVS directories underneath. root is the directory to parse. BTW, this parses the whole thing in one pass, using os.path.walk"""
        self.list = { }
        self.root = root
        os.path.walk(root, appendentries, self.list)
        return None

    # fix 2: more efficient
    def getDateStr(self, file):
        """Use this function instead of the list attribute. It implements some convenience (you can either pass the full path, or relative path to root.) Also, if some optimizations are done later, it will be very good. Throws KeyError if the file can't be found"""
        try:
            return self.list[file]
        except KeyError:
            return self.list[join(self.root, file)]

    def getDate(self, file):
        """Convenience...returns the 9-int time tuple used by the time module. Throws ValueError if it can't be parsed (unlikely), and KeyError if the file can't be found."""
        return time.strptime(self.getDateStr(file))

if __name__=='__main__':
    import sys
    cvslist = cvsmoddate(sys.argv[1])
    print cvslist.list



#!/usr/bin/env python
import xml.dom.minidom
from xml.dom import Node
import sys
def _tostr(node):
	str=""
	for each in node.childNodes:
		str=str+each.data
	return str
def _a_an(str):
	import string
	str=string.strip(str)
	if (string.find("aeiou",str[0])!=-1):
		return "an"
	else:
		return "a"

#xml header
header="""
"""
def _shorten(url):
	import string
	if(url[0:7]=="http://"):
		url=url[7:]
	if(len(url)>10):
		url=string.split(url,"/")[0]
	return url
class StringWriter:
	def __init__(self,fp=sys.stdout):
		self.fp=fp
		self.str=""
	def write(self,str):
		self.str=self.str+str
	def writeline(self,str):
		self.str=self.str+str+"\r\n"
	def flush(self):
		self.fp.write(self.str)
	def close(self):
		self.fp.close()

def reverse(str):
	rev=""
	for each in str:
		rev=each+rev
	return rev

def spam_protect(str):
	return reverse(str)+" (backwards)"

class Developer:
	def __init__(self,node):
		self.node=node
		node.normalize()
		self.data={}
		
		for each in node.childNodes:
			if each.nodeType == Node.ELEMENT_NODE:
				if(each.tagName=="chat"):
					self.data["chat"]={}
					for nick in each.childNodes:
						if nick.nodeType == Node.ELEMENT_NODE:
							self.data["chat"][nick.tagName]=_tostr(nick)
				elif (each.tagName=="tasks"):
					self.data["tasks"]=[]
					for task in each.childNodes:
						if task.nodeType == Node.ELEMENT_NODE:
							self.data["tasks"].append(_tostr(task))
				else:
					self.data[each.tagName]=_tostr(each)
		print "reading %s.........." % self.name
	
	def __getattr__(self,attr):
		if(self.data.has_key(attr)):
			return self.data[attr]
		else:
			return None
	def toHtml(self,w):
		w.writeline("""<foaf:Person>""" )	
		w.writeline("""<foaf:name>%s</foaf:name>""" %self.name )
#		w.writeline("""<foaf:interest rdf:resource=\"http://www.dotgnu.org/\"/>""")
		w.writeline("""<foaf:currentProject rdf:resource=\"http://www.dotgnu.org/\"/>""")
#		w.writeline("""<dc:contributor rdf:resource=\"http://www.dotgnu.org/\"/>""")


		if(self.homepage):
			w.writeline("""<foaf:homepage rdf:resource="%s"/> """ % self.homepage)

		for each in self.tasks:
			w.writeline("""<dotgnu:task>%s</dotgnu:task>""" % each)

		if(self.occupation):
			w.writeline("""<dotgnu:occupation>%s</dotgnu:occupation>""" % self.occupation)
		if(self.location):
			w.writeline("""<dotgnu:location>%s</dotgnu:location>"""   % self.location)
			
		if(len(self.chat.keys())!=1):
			first = 1
			for mode in self.chat.keys():
				foaf = "dotgnu:" + mode
				if (mode == "jabber"):
					foaf = "foaf:jabberID"
				elif (mode == "irc"):
					foaf = "dotgnu:ircID"
				elif (mode == "yahoo"):
					foaf = "dotgnu:yahooChatID"
				elif (mode == "aim"):
					foaf = "foaf:aimChatID"

				w.writeline("""<%s>%s</%s>"""  % (foaf,self.chat[mode],foaf))

		w.writeline("""</foaf:Person>""")

def processTree(tree):
	data=tree.getElementsByTagName("developer")
	developers={}
	for each in data:
		dev=Developer(each)
		developers[dev.name]=dev
	sorted=developers.keys()
	sorted.sort()
	fp=open("../src/people.foaf","w")
	w=StringWriter(fp)
	w.writeline("""<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- DotGNU People FOAF -->
<rdf:RDF
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dotgnu="http://dotgnu.org/2003/06/dotgnu.rdfs"
	xmlns:rss="http://purl.org/rss/1.0/"
	xmlns:foaf="http://xmlns.com/foaf/0.1/">
]>
<dotgnu:DevelopersList rdf:about="http://dotgnu.org/2003/06/developers.foaf">
""")
#       xmlns:cc="http://web.resource.org/cc/"
#	xmlns:wn="http://xmlns.com/wordnet/1.6/"
# 	xmlns:air="http://www.megginson.com/exp/ns/airports#"
# 	xmlns:contact="http://www.w3.org/2000/10/swap/pim/contact#"
# 	xmlns:rel="http://www.perceive.net/schemas/20021119/relationship/relationship.rdf"
# 	xmlns:trust="http://www.perceive.net/schemas/20020725/trust/trust.rdf#"
# 	xmlns:wot="http://xmlns.com/wot/0.1/"
	
	for each in sorted:
		print "processing %s .........." % each
#		w.writeline( """<rdf:Seq>""")
		developers[each].toHtml(w)
#		w.writeline( """</rdf:Seq>""")
	w.writeline( """
</dotgnu:DevelopersList>
</rdf:RDF>""")
	w.flush()
	w.close()
	print "wrote result to ../src/people.foaf"
				
if __name__=="__main__":
	tree=xml.dom.minidom.parse("developers.xml")
	processTree(tree)

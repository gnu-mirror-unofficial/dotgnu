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
header="""<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE content
[
<!--======================================== modify but don't delete ========================================-->
 <!ENTITY base "./">
 <!ENTITY title	"DotGNU People">
 <!ENTITY this "people.html">
 <!ENTITY maintainer "&lt;a href=&quot;http://norbert.ch/&quot;&gt;Norbert Bollow&lt;/a&gt; &lt;a href=&quot;mailto:nb@cisto.com&quot;&gt;&_lt_;nb@cisto.com&_gt_;&lt;/a&gt;">
 <!ENTITY modtime "%s">
<!--======================================== modify but don't delete ========================================-->

<!--======================================== add custom entities here ========================================-->
<!--======================================== add custom entities here ========================================-->

<!--======================================== declared here, defined elsewhere ========================================-->
 <!ENTITY nav.snapshots "">
 <!ENTITY nav.rationale "">
 <!ENTITY nav.info "">
 <!ENTITY nav.debs "">
 <!ENTITY nav.faq "">
 <!ENTITY nav.essays "">
 <!ENTITY nav.proposals "">
 <!ENTITY nav.patent "">
 <!ENTITY nav.projects "">
 <!ENTITY nav.proposals.active "">
 <!ENTITY nav.arch "">
 <!ENTITY nav.see "">
 <!ENTITY nav.phpgw "">
 <!ENTITY nav.pnet "">
 <!ENTITY nav.pnet.lib.status "">
 <!ENTITY nav.pnet.lib.docs "">
 <!ENTITY nav.web_services "">
 <!ENTITY nav.auth "">
 <!ENTITY nav.mail.lists "">
 <!ENTITY nav.mail.pipermail "">
 <!ENTITY nav.mail.announce "">
 <!ENTITY nav.mail.developers "">
 <!ENTITY nav.mail.auth "">
 <!ENTITY nav.mail.arch "">
 <!ENTITY nav.mail.biz "">
 <!ENTITY nav.mail.website "">
 <!ENTITY misc.freedev "">
 <!ENTITY misc.gnu "">
 <!ENTITY misc.dotgnu "">
 <!ENTITY mail.gnu "">
 <!ENTITY mail.dotgnu "">
 <!ENTITY mail.rhysw "">
 <!ENTITY mail.gopal "">
 <!ENTITY mail.minten "">
 <!ENTITY mail.dnicol "">
 <!ENTITY _lt_ "">
 <!ENTITY _gt_ "">
 <!ENTITY _quot_ "">
 <!ENTITY _apos_ "">
 <!ENTITY _amp_ "">
 <!ENTITY nbsp "">
 <!ENTITY copy "">
 <!ENTITY root "">
<!--======================================== declared here, defined elsewhere ========================================-->

<!--======================================== don't touch this stuff ========================================-->
 <!ELEMENT ul (li)+>
 <!ELEMENT ol (li)+>
 <!ELEMENT dl (dt|dd)+>
 <!ELEMENT dt (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT li (#PCDATA | include | br | em | strong | code | a | img | ul | ol | dl)*>
 <!ELEMENT dd (#PCDATA | include | br | em | strong | code | a | img | ul | ol | dl)*>
 <!ELEMENT blockquote (#PCDATA | include | br | em | strong | code | a | img | ul | ol | dl)*><!--no nesting blockquotes-->
 <!ELEMENT pre (#PCDATA | include | br | em | strong | code | a)*><!--no images in pre-->
 <!ELEMENT a (#PCDATA | include | br | em | strong | code | img)*><!--no nesting anchors-->
 <!ELEMENT content (#PCDATA | include | p | h1 | h2 | h3 | h4 | pre | blockquote)*><!--block elements only in top level-->
 <!ELEMENT p (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT em (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT strong (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT code (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT h1 (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT h2 (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT h3 (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT h4 (#PCDATA | include | br | em | strong | code | a | img)*>
 <!ELEMENT br EMPTY>
 <!ELEMENT img EMPTY>
 <!ELEMENT include EMPTY>
 <!ATTLIST a title CDATA #IMPLIED name NMTOKEN #IMPLIED href CDATA #IMPLIED>
 <!ATTLIST img src CDATA #REQUIRED alt CDATA #REQUIRED align (top|middle|bottom|left|right) #IMPLIED>
 <!ATTLIST include file CDATA #REQUIRED entry NMTOKEN #IMPLIED overwrite (true|false) #IMPLIED>
<!--======================================== don't touch this stuff ========================================-->
]>

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
		w.writeline("""<h3 class="subheading">%s</h3>""" % self.name)
		w.writeline("""<p class="maincontent">""")
		w.writeline("""Hi, My name is %s.""" % self.name) 
		w.writeline("""You can contact me via email with %s """	% self.email)
		if(self.homepage):
			w.writeline("""Or you could visit my website at
							[<a class="linksbody" href="%s">%s</a>]. """ 
							%	(self.homepage,self.homepage))
		else:
			w.writeline(". ")
		if(self.dotgnusince):
			w.writeline("I've been dotgnu'ing since %s." % self.dotgnusince)
		if(self.tasks):
			w.writeline("So far I've been helping dotgnu with these.")
			w.writeline("""<ul class="maincontent">""")
			for each in self.tasks:
				w.writeline("""<li><p>%s</p></li>""" % each)
			w.writeline("</ul>")
		w.writeline("<p class=\"maincontent\">")
		if(self.occupation):
			w.writeline("I'm %s %s. " % (_a_an(self.occupation),self.occupation))
		if(self.location):
			w.writeline("And &quot;%s&quot; is where I am most likely found. "
				% self.location)
		if(self.chat):
			w.writeline("I usually visit IRC under the nick &lt;%s&gt;. " % self.chat["irc"])
			if(len(self.chat.keys())!=1):
				w.writeline("I can also be found with ")
				first = 1
				for mode in self.chat.keys():
					if mode!="irc":
						if(not first):
							w.writeline(",%s (%s) " % (self.chat[mode],mode))
						else:
							first=0
							w.writeline("%s (%s) " % (self.chat[mode],mode))
				w.writeline(".")
		w.writeline("</p>")
		w.writeline("</p>")
		w.writeline("<hr/>")

def processTree(tree):
	data=tree.getElementsByTagName("developer")
	developers={}
	for each in data:
		dev=Developer(each)
		developers[dev.name]=dev
	sorted=developers.keys()
	sorted.sort()
	fp=open("../src/people.xml","w")
	w=StringWriter(fp)
	import time
	lastd=time.gmtime(time.time());
	lastmod=`lastd[2]`+"-"+`lastd[1]`+"-"+`lastd[0]`
	w.writeline(header % lastmod)
	w.writeline("""
		<content>
		<h1>DotGNU People</h1>
		<p class="maincontent">
			A project , especially a free software project , is all about
			the community. DotGNU , following the tradition of all the 
			GNU projects ,aims at creating a community where the freedom
			is provided,enjoyed and utilized. The DotGNU community effort
			moves up to build a strong foundation for the pillars of a
			new free internet.
		</p>
		<p class="maincontent">
			Listed below is a brief and alphabetical list of the DotGNU people 
			who	are involved with the project . The list includes people working
			on the various projects as well as people who are using DotGNU
			for their work. If you belong to either category and want your
			name listed here , please contact the dotgnu WEBSITE mailing 
			list at (website@dotgnu.org).
		</p>
	""")
	for each in sorted:
		print "processing %s .........." % each
		developers[each].toHtml(w)
	w.writeline( """
		</content>
	""")
	w.flush()
	w.close()
	print "wrote result to ../src/people.xml"
if __name__=="__main__":
	tree=xml.dom.minidom.parse("developers.xml")
	processTree(tree)

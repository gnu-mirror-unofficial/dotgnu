#!/usr/bin/python
##############################################
# This is released under the GNU GPL license #
# Copyright (c) FSF India                    #
# Author        Gopal.V                      #
##############################################
import xml.dom.minidom
import string
import sys
from cvstree import *
cvs_entries=cvsmoddate("/opt/cvs/dotgnu/pnetlib/runtime")
cvs_sys_entries=cvsmoddate("/opt/cvs/dotgnu/pnetlib/")
#################TODO#####################
#                                        #
# * implement error messages             #
# * implement classes for html           #
# * implement xml validation             #
# * implement command line options       #
# * implement theme/template support     #
# * implement maintainer ids             #
# * implement this whole thing in C#     #
##########################################
class classnode:
	def __init__(self,node):
		self.node=node
		self.fqname=node.getAttribute("name")
		self.ns=string.join(string.split(self.fqname,".")[0:-1],".")
		self.name=string.split(self.fqname,".")[-1]
		self.methods=node.getElementsByTagName("method")
		self.fields=node.getElementsByTagName("field")
		self.ctors=node.getElementsByTagName("ctor")
		self.events=node.getElementsByTagName("event")
		self.props=node.getElementsByTagName("property")
		print "reading...."+self.fqname
	def __repr__(self):
		return "<class name=\""+self.fqname+"\">"

class filewrapper:
	def __init__(self,fname,mode):
		self.fp=open(fname,mode)
	def write(self,data):
		self.fp.write(data)
	def writeline(self,data):
		self.fp.write(data+"\n")
	def writespecial(self,url): # escaped
		hex=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
		for each in url:
			val=ord(each)
			if ((val >= ord('a') and val <= ord('z')) or (val >= ord('A') and val <= ord('Z'))):
				self.fp.write(each)
			elif each=='.':
				self.fp.write(each)
			else:
				self.fp.write("%%%c%c" % (hex[val /16],hex[val % 16]))
	def close(self):
		self.fp.close()
#########################helper functions#########################
# I had to write these because the minidom is not flexible enough#
# well that's why it's called `mini' dom                         #
# These could be improved upon, but I'm too lazy                 #
##################################################################
def hasChildNode(parent,name):
	for node in parent.childNodes:
		if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
			if(name=="*" or node.tagName == name):
				return node
	return 0

def get_prev_next(list,element):
	i=list.index(element)
	maxi=len(list)-1 #
	if(i==0):
		prev="index.html"
	else:
		prev=list[i-1]+".html"
	if(i==maxi):
		next="index.html"
	else:
		next=list[i+1]+".html"
	return (prev,next)

def get_last_active(name):
	fname=name
	if(name[0:10]=="System.Xml"):
		fname=name[0:10]+string.replace(name[10:],".","/")
	else:
		fname=string.replace(name,".","/")
	try:
		retval="<i> on "+cvs_entries.getDateStr(fname+".cs")+"</i>"
		return retval;
	except KeyError:
		try:
			retval="<i> on "+cvs_sys_entries.getDateStr(fname+".cs")+"</i>"
			return retval;
		except KeyError:
			return ""
#########################end helper functions####################
#status functions
def get_status(node,prefix=""):
	child_error=len(node.getElementsByTagName("missing"))+\
				len(node.getElementsByTagName("todo"))+\
				len(node.getElementsByTagName("msg"))+\
				len(node.getElementsByTagName("extra"))
	if(hasChildNode(node,"todo")):
		return (1,"<b>"+prefix+"TODO</b>")
	if(hasChildNode(node,"missing")):
		return (2,"<font color=\"#FF1000\">"+prefix+"Missing</font>")
	if (hasChildNode(node,"msg")):
		msg=hasChildNode(node,"msg")
		msg.normalize()
		return (3,"<i>"+prefix+msg.childNodes[0].data+"</i>")
	if(hasChildNode(node,"extra")):
		return (4,"<i>"+prefix+"Extra</i>")
	if(hasChildNode(node,"attribute")):
		errnode=hasChildNode(node,"attribute")
		return get_status(errnode,errnode.getAttribute("name")+" is ")
	if(child_error!=0):
		return (0,"")
	return (0,"csdocvalil goofed up")

def split_signature(sig):
	name=string.split(sig,"(")[0]
	prefix=string.join(string.split(name)[0:-1]," ")
	name=string.split(name)[-1]
	params=string.split(sig,"(")[-1]
	#remember ignore prefix for ctors
	return (prefix,name,params)
#format functions
####MOST OF THIS STUFF HAS BEEN REVERSE ENGINEERED FROM PHPHNUKE's HTML####
##########################SO ALL CREDIT TO THEM############################
def print_curved_header(fp,header=""):
	fp.writeline("""<table bgcolor="#cfcfbb"  width="90%" cellpadding="0" cellspacing="0" align="center" border="0" bordercolor="#dedebb">""")
	fp.writeline("""<tr><td bgcolor="#cfcfbb" valign="top"><img src="corner-top-left.jpg"></td>""")
	fp.writeline("<td bgcolor=\"#cfcfbb\">"+header+"</td>")
	fp.writeline("<td bgcolor=\"#cfcfbb\" align=\"right\" valign=\"top\"><img src=\"corner-top-right.jpg\"></td></tr>")
	fp.writeline("</td></tr>")
	
def print_curved_footer(fp):
	fp.writeline("<tr><td valign=\"bottom\" align=\"left\"><img src=\"corner-bottom-left.jpg\"></td>")
	fp.writeline("<td>&nbsp;</td>")
	fp.writeline("<td valign=\"bottom\" align=\"right\"><img src=\"corner-bottom-right.jpg\"></td></tr>")
	fp.writeline("</td></tr>")
	fp.writeline("</table>")
	
def print_curved_title(fp,title=""):
	fp.writeline("<tr><td>&nbsp;</td>")
	fp.writeline("<td bgcolor=\"#cfcfbb\">"+title+"</td>")
	fp.writeline("<td>&nbsp;</td></tr>")

def write_pnetlib_header(fp):
	#print_curved_header(fp,"""<h1 align="center"><underline>Pnetlib Class Status<underline></h1>""")
	##ADDED A COOL LOGO, 
	print_curved_header(fp,"""<p align="center"><img src="logo.jpg"></p>""")
	print_curved_title(fp,"""Portable.NET""")
def write_pnetlib_footer(fp):
	fp.writeline("<br><br>")
	import time
	lastd=time.gmtime(time.time());
	print_curved_header(fp,"&nbsp;")
	print_curved_title(fp,"""<p align="center">
	This document is licensed under the GNU FDL.<br>
	"""+"Last Updated on <i>"+`lastd[2]`+"-"+`lastd[1]`+"-"+`lastd[0]`+"</i>"
	+"""
							</p>
							<p align="center">
								Visit <a href="http://www.dotgnu.org">
								http://www.dotgnu.org</a> for more details
							</p>
							<p align="center">
							<table border="0" cellspacing="10" align="center">
							<tr align="center">
								<td><a href="http://www.fsf.org">
								<img src="powered-by-fs.jpg" 
								alt="[Powered by Free Software]"></a></td>
								
								<td><a href="http://www.gimp.org">
								<img src="graphics-by-gimp.jpg" 
								alt="[Graphics by Gimp]"></a>
								</td>
								
								<td><a href="http://www.gnu.org">
								<img src="powered-by-gnu.jpg" 
								alt="[Powered by GNU]"></a>
								</td>
							</tr>
							<tr>
							<td></td>
							<td><font size="-5">Maintained by Gopal.V </font></td>
							<td></td>
							</tr>
							</table>
							</p>
							""")
	print_curved_footer(fp)
#end format functions


def print_namespace_list(nslist,ctor,method,field,prop,event):
	#nslist=nsdict.keys()
	#nslist.sort()
	fp=filewrapper("index.html","w")
	fp.writeline("""<html><body bgcolor="#505050" text="#000000" link="#121212"
			 vlink="#0c0c0a" >""")
		
	fp.writeline("""<head><title>Portable.Net Status Page</title></head>""")
	write_pnetlib_header(fp)
	print_curved_title(fp,"""<h1>Namespaces</h1> """)
	print_curved_title(fp,"<p align=\"right\"><a href=\""+nslist[0]+".html\"><img alt=\"Next&gt;\" src=\"rarrow.jpg\" border=\"0\"></a></p>")
	fp.writeline("<tr><td>&nbsp;</td><td>")	
	#nested tabling is *so* difficult
	fp.writeline("""<table align="left" width="100%" bordercolor="#dedebb">""")
	fp.writeline("<tr><td border=\"3\">")
	fp.writeline("<!--LEFT BLOCKS-->")
	fp.writeline("""	<table align="left" bordercolor="#050505">""")
	fp.writeline("""	<tr><td>Namespaces</td></tr>""")
	fp.writeline("""	<tr><td>""")
	for each in nslist:
		fp.writeline("&nbsp;&middot;&nbsp;<b><a href=\""+each+".html\">"+each+"</a></b><br>")
	fp.writeline("""	</td></tr>""")
	fp.writeline("""	<tr><td>""")
	fp.writeline("""	</td></tr>""")
	fp.writeline("""	</table>""")
	fp.writeline("<!--CENTER BLOCKS-->")
	fp.writeline("""</td><td valign="top" border="2">""")
	fp.writeline("""	<table align="center">""")
	fp.writeline("""	<tr><td>""")
	fp.writeline("<p>In the <b>"+`len(nslist)`+"</b> namespaces</p>")
	fp.writeline("<p>we are missing:</p>")
	fp.writeline("<b>"+`ctor`+"</b> constructors, ")
	fp.writeline("<b>"+`method`+"</b> methods, ")
	fp.writeline("<b>"+`field`+"</b> fields, ")
	fp.writeline("<b>"+`prop`+"</b> properties, and ")
	fp.writeline("<b>"+`event`+"</b> events. ")
	fp.writeline("""	</td></tr>""")
	fp.writeline("""	</table>""")
	fp.writeline("</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td><td>&nbsp;</td></tr>")
	fp.writeline("""<tr><td>&nbsp;</td><td align="right"><font size="-3">[<a href="status.xml.gz">XML</a> | <a href="status2html.py">PYTHON</a>]</font></td><td>&nbsp;</td></tr>""");
	print_curved_footer(fp)
	write_pnetlib_footer(fp)
	fp.writeline("</body></html>")
	fp.close()
#Namespace functions....
##########################SUMMARY FUNCTIONS#################################
def print_method_summary(fp,parent,methods):
	fp.writeline("<tr><td>")
	fp.writeline("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.writeline("""<tr><td><font size="+2">Method Summary</h3></td></tr>""")
	fp.writeline("</table>")
	fp.writeline("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	method_count_dict={}
	for each in methods:
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		if(method_count_dict.has_key(name)):
			method_count_dict[name]=method_count_dict[name]+1
		else:
			method_count_dict[name]=1

	for each in methods:
		(status,msg)=get_status(each)
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		fp.writeline("<tr border=\"1\"><td><tt>"+prefix+"</tt><b> ")
		#write doc filename
		#due to rhys simpilifying documentation, I'm forced to 
		#complicate my program, to make it simpler to access
		fp.write("<a class=\"nounderline\" href=\"../pnetlib-doc/"+string.replace(parent.fqname,".","/")+".html#"+parent.name+"."+name)
		newparams=params[:-1] # skip the last ')'
		if method_count_dict[name]!=1: # fully qualify stuff
			first=1
			fp.writespecial('(')
			for eachparam in string.split(newparams,", "):
				if(not first):
					fp.writespecial(", ")
				first=0
				type=string.split(eachparam," ")[0]
				fp.writespecial(type)
			fp.writespecial(")")
		fp.write("%20Method\">"+name+"</a>")
		fp.writeline("</b><i>("+params+"</i></td><td align=\"right\" width=\"\">"+msg+"</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td></tr>")
##clone  the above code for all the summaries	

def print_field_summary(fp,parent,fields):
	fp.writeline("<tr><td>")
	fp.writeline("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.writeline("""<tr><td><font size="+2">Field Summary</h3></td></tr>""")
	fp.writeline("</table>")
	fp.writeline("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in fields:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		type=each.getAttribute("type")
		fp.writeline("<tr border=\"1\"><td><i>"+type+"</i> <b>")
		#write doc filename
		#due to rhys simpilifying documentation, I'm forced to 
		#complicate my program, to make it simpler to access
		fp.writeline("<a class=\"nounderline\" href=\"../pnetlib-doc/"+string.replace(parent.fqname,".","/")+".html#"+parent.name+"."+name+"%20Field\">")
		fp.writeline(name);
		fp.writeline("</a></b>");
		fp.writeline("</td><td align=\"right\" width=\"\">"+msg+"</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td></tr>")

def print_ctor_summary(fp,parent,ctors):
	fp.writeline("<tr><td>")
	fp.writeline("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.writeline("""<tr><td><font size="+2">Constructor Summary</h3></td></tr>""")
	fp.writeline("</table>")
	fp.writeline("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	ctor_count_dict={}
	for each in ctors:
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		if(ctor_count_dict.has_key(name)):
			ctor_count_dict[name]=ctor_count_dict[name]+1
		else:
			ctor_count_dict[name]=1
	for each in ctors:
		(status,msg)=get_status(each)
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		fp.writeline("<tr border=\"1\"><td><b>")
		#write doc filename
		#due to rhys simpilifying documentation, I'm forced to 
		#complicate my program, to make it simpler to access
		fp.write("<a class=\"nounderline\" href=\"../pnetlib-doc/"+string.replace(parent.fqname,".","/")+".html#"+string.split(name,'.')[-1])
		newparams=params[:-1] # skip the last ')'
		if ctor_count_dict[name]!=1: # fully qualify stuff
			first=1
			fp.writespecial('(')
			for eachparam in string.split(newparams,", "):
				if(not first):
					fp.writespecial(", ")
				first=0
				type=string.split(eachparam," ")[0]
				fp.writespecial(type)
			fp.writespecial(")")
		fp.write("%20Constructor\">"+name+"</a>")
		fp.writeline("</b><i>("+params+"</i></td><td align=\"right\" width\"\">"+msg+"</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td></tr>")
	
def print_prop_summary(fp,parent,props):
	fp.writeline("<tr><td>")
	fp.writeline("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.writeline("""<tr><td><font size="+2">Property Summary</h3></td></tr>""")
	fp.writeline("</table>")
	fp.writeline("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in props:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		type=each.getAttribute("type")
		fp.writeline("<tr border=\"1\"><td><i>"+type+"</i> <b>");
		#write doc filename
		#due to rhys simpilifying documentation, I'm forced to 
		#complicate my program, to make it simpler to access
		fp.writeline("<a class=\"nounderline\" href=\"../pnetlib-doc/"+string.replace(parent.fqname,".","/")+".html#"+parent.name+"."+name+"%20Property\">")
		fp.writeline(name);
		fp.writeline("</a></b>");
		fp.writeline("</td><td align=\"right\" width\"\">"+msg+"</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td></tr>")



def print_event_summary(fp,events):
	fp.writeline("<tr><td>")
	fp.writeline("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.writeline("""<tr><td><font size="+2">Event Summary</h3></td></tr>""")
	fp.writeline("</table>")
	fp.writeline("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in events:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		fp.writeline("<tr border=\"1\"><td><b>"+name+"</b></td><td width=\"\" align=\"right\">"+msg+"</td></tr>")
	fp.writeline("</table>")
	fp.writeline("</td></tr>")
	


###################################END SUMMARY##############################	
def print_each_class(fp,cnode):
#	fp.writeline("<br>")
	fp.writeline("<a name=\""+cnode.name+"\">")
	fp.writeline("<table bordercolor=\"#dedebb\" border=\"1\" width=\"90%\">")
	fp.writeline("<tr><td><h2>"+"<a class=\"nobold\" href=\"../pnetlib-doc/"+string.replace(cnode.fqname,'.','/')+".html\">"+cnode.fqname+"</a></h2>")
	fp.writeline("</td></tr>")
	(status,msg)=get_status(cnode.node)
	fp.writeline("""<tr><td>Status : """)
	fp.writeline(msg)
	last_active=get_last_active(cnode.fqname)	
	fp.writeline(last_active)
	fp.writeline("</td></tr>")
	#summary
	if(len(cnode.ctors)!=0):
		print_ctor_summary(fp,cnode,cnode.ctors)
	if(len(cnode.methods)!=0):
		print_method_summary(fp,cnode,cnode.methods)
	if(len(cnode.fields)!=0):
		print_field_summary(fp,cnode,cnode.fields)
	if(len(cnode.props)!=0):
		print_prop_summary(fp,cnode,cnode.props)
	if(len(cnode.events)!=0):
		print_event_summary(fp,cnode.events)
	fp.writeline("</table>")
	fp.writeline("<br>")
	fp.writeline("</a>")

def print_namespace_inner(fname,classlist,prev,next):
	fp=filewrapper(fname+".html","w")
	print "writing....."+fname+".html"
	fp.writeline("""<html><body bgcolor="#505050" link="#0A0A0A" vlink="#303030">""")
	fp.writeline("""<head><title>%s</title>
		<style>
   		.nounderline
		  {
		  	text-decoration:none;
		  }
   		.nobold
		  {
		  	text-decoration:none;
			font-weight: normal;
		  }
		</style>
	</head>"""%(fname))
	write_pnetlib_header(fp)
	print_curved_title(fp,"<h2 align=\"left\">"+fname+" Namespace</h2>")
	links="<p align=\"right\">"
	if(prev!="index.html"):
		links=links+"<a href=\""+prev+"\"><img alt=\"<< Prev\" src=\"larrow.jpg\" border=\"0\"></a>"
	links=links+"<a href=\"index.html\"><img alt=\"Up\" src=\"uarrow.jpg\" border=\"0\"></a>"
	if(next!="index.html"):
		links=links+"<a href=\""+next+"\"><img alt=\"Next >>\"src=\"rarrow.jpg\" border=\"0\"></a>"
	links=links+"</p>"	
	print_curved_title(fp,links)
	fp.writeline("<tr><td>&nbsp;</td><td>")
	fp.writeline("<!--DATA REGION-->")
	fp.writeline("""<table bordercolor="#dedebb">""")
	fp.writeline("""<tr><td border="1">""")
	fp.writeline("<!--LEFT BLOCK-->")
	fp.writeline("""	<table align="center" bgcolor="#cfcfbb">""")
	fp.writeline("""	<tr><td>Classes </td></tr>""")
	fp.writeline("""	<tr><td>""")
	
	methodcount=0
	ctorcount=0
	eventcount=0
	fieldcount=0
	propcount=0
	for each in classlist:
		fp.writeline("&nbsp;&middot;&nbsp;<b><a href=\"#"+each.name+"\">"+each.name+"</a></b><br>")
		ctorcount=ctorcount+len(each.ctors)
		methodcount=methodcount+len(each.methods)
		fieldcount=fieldcount+len(each.fields)
		eventcount=eventcount+len(each.events)
		propcount=propcount+len(each.props)
	fp.writeline("""	</td></tr>""")
	fp.writeline("""	</table>""")
	fp.writeline("""</td><td valign="top">""")
	fp.writeline("<!--CENTER BLOCK-->")
	fp.writeline("	<table><tr><td>")
	fp.writeline("<p>There are <b>"+`len(classlist)`+"</b> incomplete classes in this namespace</p>")
	fp.writeline("<p>In total we are missing :</p>")
	fp.writeline("&nbsp;&nbsp;<b>"+`ctorcount`+" </b>constructors, ")
	fp.writeline("<b>"+`methodcount`+"</b> methods, ")
	fp.writeline("<b>"+`fieldcount`+"</b> fields, ")
	fp.writeline("<b>"+`propcount`+"</b> properties, and ")
	fp.writeline("<b>"+`eventcount`+"</b> events.")
	fp.writeline("</td></tr></table>")
	fp.writeline("""	</td></tr>""")
	fp.writeline("""	</table>""")
	fp.writeline("</td><td>&nbsp;</td></tr>")
#classwise printing starts
	for each in classlist:
		fp.writeline("""<tr><td>&nbsp;</td><td>&nbsp;<hr color="#dedebb">&nbsp;</td><td>&nbsp;</td></tr>""")
		fp.writeline("""<tr><td>&nbsp;</td><td>""")
		print_each_class(fp,each)
		fp.writeline("</td><td>&nbsp;</td></tr>")
	print_curved_footer(fp)
	write_pnetlib_footer(fp)
	fp.writeline("</body></html>")
	fp.close()
	return (ctorcount,methodcount,fieldcount,propcount,eventcount)

if __name__=="__main__":
	root=xml.dom.minidom.parse('status.xml')
	classes=root.getElementsByTagName("class")
	classnodes=[]
	nsdict={}
	for each in classes:
		c=classnode(each);
		classnodes.append(c)
		if (nsdict.has_key(c.ns)):
			a=nsdict.get(c.ns)
		else:
			a=[]
		a.append(c)
		nsdict.update({c.ns:a})
	ctorcount=0
	methodcount=0
	propcount=0
	eventcount=0
	fieldcount=0
	nslist=nsdict.keys()
	nslist.sort()
	for each in nslist:
		#print nsdict.get(each)
		(prev,next)=get_prev_next(nslist,each)
		(ctor,method,field,prop,event)=print_namespace_inner(each,nsdict.get(each),prev,next)
		ctorcount=ctorcount+ctor
		propcount=propcount+prop
		fieldcount=fieldcount+field
		eventcount=eventcount+event
		methodcount=methodcount+method
	print_namespace_list(nslist,ctorcount,methodcount,fieldcount,propcount,eventcount)	

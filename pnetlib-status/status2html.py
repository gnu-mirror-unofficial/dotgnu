#!/usr/bin/env python1.5
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
		self.attrs=node.getElementsByTagName("attribute")
		print "reading...."+self.fqname
	def __repr__(self):
		return "<class name=\""+self.fqname+"\">"

# of internal call documentation
class iclassnode:
	def __init__(self,node):
		self.node=node
		self.name=node.getAttribute("name")
		self.ns=node.getAttribute("namespace")
		self.fqname=self.ns+"."+self.name
		self.icalls=node.getElementsByTagName("internalcall")
		print "reading...."+self.ns+self.name
	def __repr__(self):
		return "<class name=\""+self.fqname+"\">"
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
	fname=string.replace(name,".","/")
	try:
		retval="<i> on "+cvs_entries.getDateStr(fname+".cs")+"</i>"
		return retval;
	except KeyError:
		return ""
#########################end helper functions####################
#status functions
def get_status(node):
	child_error=len(node.getElementsByTagName("missing"))+\
				len(node.getElementsByTagName("todo"))+\
				len(node.getElementsByTagName("msg"))+\
				len(node.getElementsByTagName("extra"))
	if(hasChildNode(node,"todo")):
		return (1,"<b>TODO</b>")
	if(hasChildNode(node,"missing")):
		return (2,"<font color=\"#FF1000\">Missing</font>")
	if (hasChildNode(node,"msg")):
		msg=hasChildNode(node,"msg")
		msg.normalize()
		return (3,"<i>"+msg.childNodes[0].data+"</i>")
	if(hasChildNode(node,"extra")):
		return (4,"<i>Extra</i>")
	if(child_error!=0):
		return (0,"<b>TODO ?</b>")
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
	fp.write("""<table bgcolor="#cfcfbb"  width="90%" cellpadding="0" cellspacing="0" align="center" border="0" bordercolor="#dedebb">""")
	fp.write("""<tr><td bgcolor="#cfcfbb" valign="top"><img src="corner-top-left.jpg"></td>""")
	fp.write("<td bgcolor=\"#cfcfbb\">"+header+"</td>")
	fp.write("<td bgcolor=\"#cfcfbb\" align=\"right\" valign=\"top\"><img src=\"corner-top-right.jpg\"></td></tr>")
	fp.write("</td></tr>")
	
def print_curved_footer(fp):
	fp.write("<tr><td valign=\"bottom\" align=\"left\"><img src=\"corner-bottom-left.jpg\"></td>")
	fp.write("<td>&nbsp;</td>")
	fp.write("<td valign=\"bottom\" align=\"right\"><img src=\"corner-bottom-right.jpg\"></td></tr>")
	fp.write("</td></tr>")
	fp.write("</table>")
	
def print_curved_title(fp,title=""):
	fp.write("<tr><td>&nbsp;</td>")
	fp.write("<td bgcolor=\"#cfcfbb\">"+title+"</td>")
	fp.write("<td>&nbsp;</td></tr>")

def write_pnetlib_header(fp):
	#print_curved_header(fp,"""<h1 align="center"><underline>Pnetlib Class Status<underline></h1>""")
	##ADDED A COOL LOGO, 
	print_curved_header(fp,"""<p align="center"><img src="logo.jpg"></p>""")
	print_curved_title(fp,"""Portable.NET""")
def write_pnetlib_footer(fp):
	fp.write("<br><br>")
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


def print_namespace_list(nslist,ctor,method,field,prop,event,attr):
	#nslist=nsdict.keys()
	#nslist.sort()
	fp=open("index.html","w")
	fp.write("""<html><body bgcolor="#505050" text="#000000" link="#121212"
			 vlink="#0c0c0a" >""")
	
	write_pnetlib_header(fp)
	print_curved_title(fp,"""<h1>Namespaces</h1> """)
	print_curved_title(fp,"<p align=\"right\"><a href=\""+nslist[0]+".html\"><img alt=\"Next&gt;\" src=\"rarrow.jpg\" border=\"0\"></a></p>")
	fp.write("<tr><td>&nbsp;</td><td>")	
	#nested tabling is *so* difficult
	fp.write("""<table align="left" width="100%" bordercolor="#dedebb">""")
	fp.write("<tr><td border=\"3\">")
	fp.write("<!--LEFT BLOCKS-->")
	fp.write("""	<table align="left" bordercolor="#050505">""")
	fp.write("""	<tr><td>Namespaces</td></tr>""")
	fp.write("""	<tr><td>""")
	for each in nslist:
		fp.write("&nbsp&middot;&nbsp;<b><a href=\""+each+".html\">"+each+"</a></b><br>")
	fp.write("""	</td></tr>""")
	#fp.write("""	Runtime Methods<br>""")
	#for each in inslist:
	#	fp.write("&nbsp&middot;&nbsp;<b><a href=\"icall."+each+".html\">"+each+"</a></b><br>")
	fp.write("""	<tr><td>""")
	fp.write("""	</td></tr>""")
	fp.write("""	</table>""")
	fp.write("<!--CENTER BLOCKS-->")
	fp.write("""</td><td valign="top" border="2">""")
	fp.write("""	<table align="center">""")
	fp.write("""	<tr><td>""")
	fp.write("<p>In the <b>"+`len(nslist)`+"</b> namespaces</p>")
	fp.write("<p>we are missing:</p>")
	fp.write("<b>"+`ctor`+"</b> constructors, ")
	fp.write("<b>"+`method`+"</b> methods, ")
	fp.write("<b>"+`field`+"</b> fields, ")
	fp.write("<b>"+`prop`+"</b> properties, ")
	fp.write("<b>"+`event`+"</b> events and ")
	fp.write("<b>"+`attr`+"</b> attributes.")
#	fp.write("<b>"+`icall`+"</b> internal calls")
	fp.write("""	</td></tr>""")
	fp.write("""	</table>""")
#	fp.write("""</td><td align="right" valign="top" border="2">""")
#	fp.write("<!--RIGHT BLOCKS-->")
#	fp.write("""	<table width="100px" style="overflow:scroll;">""")
#	fp.write("""<tr><td>Contact Rhys</td></tr>""")
#	fp.write("""	</table>""")
	fp.write("</td></tr>")
	fp.write("</table>")
	fp.write("</td><td>&nbsp;</td></tr>")
	fp.write("""<tr><td>&nbsp;</td><td align="right"><font size="-3">[<a href="status.xml.gz">XML</a> | <a href="status2html.py">PYTHON</a>]</font></td><td>&nbsp;</td></tr>""");
	print_curved_footer(fp)
	write_pnetlib_footer(fp)
	fp.write("</body></html>")
	fp.close()
#Namespace functions....
##########################SUMMARY FUNCTIONS#################################
def print_method_summary(fp,methods):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Method Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in methods:
		(status,msg)=get_status(each)
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		fp.write("<tr border=\"1\"><td><tt>"+prefix+"</tt><b> "+name+"</b><i>("+params+"</i></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")
##clone  the above code for all the summaries	

def print_field_summary(fp,fields):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Field Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in fields:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		type=each.getAttribute("type")
		fp.write("<tr border=\"1\"><td><i>"+type+"</i> <b>")
		#write doc filename
		fp.write("<a href=\"../pnetlib-doc/"+string.replace(name,".","/")+".html")
		#due to rhys simpilifying documentation, I'm forced to 
		#complicate my program, to make it simpler to access
		fp.write(name+" Property\">")
		fp.write(name+"</b></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")

def print_ctor_summary(fp,ctors,cnode):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Constructor Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in ctors:
		(status,msg)=get_status(each)
		sig=each.getAttribute("signature")
		(prefix,name,params)=split_signature(sig)
		fp.write("<tr border=\"1\"><td><b>")
		fp.write(name+"</b></a><i>("+params+"</i></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")
	
def print_prop_summary(fp,props):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Property Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in props:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		type=each.getAttribute("type")
		fp.write("<tr border=\"1\"><td><i>"+type+"</i> <b>"+name+"</b></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")



def print_event_summary(fp,events):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Event Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in events:
		(status,msg)=get_status(each)
		name=each.getAttribute("name")
		fp.write("<tr border=\"1\"><td><b>"+name+"</b></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")
	


def print_attr_summary(fp,attrs):
	fp.write("<tr><td>")
	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
	fp.write("""<tr><td><font size="+2">Attribute Summary</h3></td></tr>""")
	fp.write("</table>")
	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
	for each in attrs:
		(status,msg)=get_status(each)
		sig=each.getAttribute("name")
		(prefix,name,params)=split_signature(sig)
		fp.write("<tr border=\"1\"><td><b>"+name+"</b> (<i>"+params+"</i></td><td align=\"right\">"+msg+"</td></tr>")
	fp.write("</table>")
	fp.write("</td></tr>")
###################################END SUMMARY##############################	
def print_each_class(fp,cnode):
#	fp.write("<br>")
	fp.write("<a name=\""+cnode.name+"\">")
	fp.write("<table bordercolor=\"#dedebb\" border=\"1\" width=\"90%\">")
	fp.write("<tr><td><h2>"+cnode.fqname+"</h2></td></tr>")
	(status,msg)=get_status(cnode.node)
	fp.write("""<tr><td>Status : """)
	fp.write(msg)
	last_active=get_last_active(cnode.fqname)	
	fp.write(last_active)
	fp.write("</td></tr>")
	#summary
	if(len(cnode.ctors)!=0):
		print_ctor_summary(fp,cnode.ctors,cnode)
	if(len(cnode.methods)!=0):
		print_method_summary(fp,cnode.methods)
	if(len(cnode.fields)!=0):
		print_field_summary(fp,cnode.fields)
	if(len(cnode.props)!=0):
		print_prop_summary(fp,cnode.props)
	if(len(cnode.events)!=0):
		print_event_summary(fp,cnode.events)
	if(len(cnode.attrs)!=0):
		print_attr_summary(fp,cnode.attrs)
	fp.write("</table>")
	fp.write("<br>")
	fp.write("</a>")

def print_namespace_inner(fname,classlist,prev,next):
	fp=open(fname+".html","w")
	print "writing....."+fname+".html"
	fp.write("""<html><body bgcolor="#505050" link="#0A0A0A" vlink="#303030">""")
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
	fp.write("<tr><td>&nbsp;</td><td>")
	fp.write("<!--DATA REGION-->")
	fp.write("""<table bordercolor="#dedebb">""")
	fp.write("""<tr><td border="1">""")
	fp.write("<!--LEFT BLOCK-->")
	fp.write("""	<table align="center" bgcolor="#cfcfbb">""")
	fp.write("""	<tr><td>Classes </td></tr>""")
	fp.write("""	<tr><td>""")
	
	methodcount=0
	ctorcount=0
	eventcount=0
	fieldcount=0
	propcount=0
	attrcount=0	
	for each in classlist:
		fp.write("&nbsp;&middot;&nbsp<b><a href=\"#"+each.name+"\">"+each.name+"</a></b><br>")
		ctorcount=ctorcount+len(each.ctors)
		methodcount=methodcount+len(each.methods)
		fieldcount=fieldcount+len(each.fields)
		eventcount=eventcount+len(each.events)
		propcount=propcount+len(each.props)
		attrcount=attrcount+len(each.attrs)
	fp.write("""	</td></tr>""")
	fp.write("""	</table>""")
	fp.write("""</td><td valign="top">""")
	fp.write("<!--CENTER BLOCK-->")
	fp.write("	<table><tr><td>")
	fp.write("<p>There are <b>"+`len(classlist)`+"</b> incomplete classes in this namespace</p>")
	fp.write("<p>In total we are missing :</p>")
	fp.write("&nbsp;&nbsp;<b>"+`ctorcount`+" </b>constructors, ")
	fp.write("<b>"+`methodcount`+"</b> methods, ")
	fp.write("<b>"+`fieldcount`+"</b> fields, ")
	fp.write("<b>"+`propcount`+"</b> properties, ")
	fp.write("<b>"+`eventcount`+"</b> events and ")
	fp.write("<b>"+`attrcount`+"</b> attributes.")
	fp.write("</td></tr></table>")
#	fp.write("""</td><td>""")
#	fp.write("<!--RIGHT BLOCK-->")
#	fp.write("""	<table></table>""")
	fp.write("""	</td></tr>""")
	fp.write("""	</table>""")
	fp.write("</td><td>&nbsp;</td></tr>")
#classwise printing starts
	for each in classlist:
		fp.write("""<tr><td>&nbsp;</td><td>&nbsp;<hr color="#dedebb">&nbsp;</td><td>&nbsp;</td></tr>""")
		fp.write("""<tr><td>&nbsp;</td><td>""")
		print_each_class(fp,each)
		fp.write("</td><td>&nbsp;</td></tr>")
	print_curved_footer(fp)
	write_pnetlib_footer(fp)
	fp.write("</body></html>")
	fp.close()
	return (ctorcount,methodcount,fieldcount,propcount,eventcount,attrcount)
#########################################################################################################
#def print_icall_method_summary(fp,methods):
#	fp.write("<tr><td>")
#	fp.write("""<table cellspacing="0" width="100%" bgcolor="#b2b297" border="1">""")
#	fp.write("""<tr><td><font size="+2">InternalCall Summary</h3></td></tr>""")
#	fp.write("</table>")
#	fp.write("""<table cellpadding="4" cellspacing="0" width="100%" bordercolor="#99997e" border="1">""")
#	for each in methods:
#		msg="<font color=\"#ff1212\">"+each.getAttribute("status")+"</font>"
#		sig=each.getAttribute("signature")
#		(prefix,name,params)=split_signature(sig)
#		fp.write("<tr border=\"1\"><td><tt>"+prefix+"</tt><b> "+name+"</b><i>("+params+"</i></td><td align=\"right\">"+msg+"</td></tr>")
#	fp.write("</table>")
#	fp.write("</td></tr>")
#	
#def print_icall_each_class(fp,cnode):
#	fp.write("<a name=\""+cnode.name+"\">")
#	fp.write("<table bordercolor=\"#dedebb\" border=\"1\" width=\"90%\">")
#	fp.write("<tr><td><h2>"+cnode.fqname+"</h2></td></tr>")
#	fp.write("</td></tr>")
#	#summary
#	print_icall_method_summary(fp,cnode.icalls)
#	fp.write("</table>")
#	fp.write("<br>")
#	fp.write("</a>")
#	
#def print_icall_ns_inner(fname,classlist,prev,next):
#	missing=0
#	fp=open("icall."+fname+".html","w")
#	print "writing.....icall."+fname+".html"
#	fp.write("""<html><body bgcolor="#505050" link="#0A0A0A" vlink="#303030">""")
#	write_pnetlib_header(fp)
#	print_curved_title(fp,"<h2 align=\"left\">"+fname+" Namespace</h2>")
#	links="<p align=\"right\">"
#	if(prev!="index.html"):
#		links=links+"<a href=\"icall."+prev+"\"><img src=\"larrow.jpg\" border=\"0\"></a>"
#	links=links+"<a href=\"index.html\"><img src=\"uarrow.jpg\" border=\"0\"></a>"
#	if(next!="index.html"):
#		links=links+"<a href=\"icall."+next+"\"><img src=\"rarrow.jpg\" border=\"0\"></a>"
#	links=links+"</p>"	
#	print_curved_title(fp,links)
#	fp.write("<tr><td>&nbsp;</td><td>")
#	fp.write("<!--DATA REGION-->")
#	fp.write("""<table bordercolor="#dedebb">""")
#	fp.write("""<tr><td border="1">""")
#	fp.write("<!--LEFT BLOCK-->")
#	fp.write("""	<table align="center" bgcolor="#cfcfbb">""")
#	fp.write("""	<tr><td>Classes </td></tr>""")
#	fp.write("""	<tr><td>""")
#	for each in classlist:
#		fp.write("&nbsp;&middot;&nbsp<b><a href=\"#"+each.name+"\">"+each.name+"</a></b><br>")
#		missing=missing+len(each.icalls)
#	fp.write("""	</td></tr>""")
#	fp.write("""	</table>""")
#	fp.write("""</td><td valign="top">""")
#	fp.write("<!--CENTER BLOCK-->")
#	fp.write("	<table><tr><td>")
#	fp.write("<p>There are <b>"+`len(classlist)`+"</b> classes with missing InternalCalls in this namespace</p>")
#	fp.write("<b>"+`missing`+"</b> internal calls missing")
#	fp.write("</td></tr></table>")
#	fp.write("""	</td></tr>""")
#	fp.write("""	</table>""")
#	fp.write("</td><td>&nbsp;</td></tr>")
##classwise printing starts
#	for each in classlist:
#		fp.write("""<tr><td>&nbsp;</td><td>&nbsp;<hr color="#dedebb">&nbsp;</td><td>&nbsp;</td></tr>""")
#		fp.write("""<tr align="center"><td>&nbsp;</td><td>""")
#		print_icall_each_class(fp,each)
#		fp.write("</td><td>&nbsp;</td></tr>")
#	print_curved_footer(fp)
#	write_pnetlib_footer(fp)
#	fp.write("</body></html>")
#	fp.close()
#	return missing
#
#def process_icall():
#	missing=0
#	inodes=[]
#	insdict={}
#	iroot=xml.dom.minidom.parse('icall.xml')
#	icalls=iroot.getElementsByTagName('class');
#	for each in icalls:
#		c=iclassnode(each);
#		inodes.append(c);
#		if(insdict.has_key(c.ns)):
#			a=insdict.get(c.ns)
#		else:
#			a=[]
#		a.append(c)
#		insdict.update({c.ns:a})
#	inslist=insdict.keys()
#	inslist.sort()
#	for each in inslist:
#		(prev,next)=get_prev_next(inslist,each)
#		missing=missing+print_icall_ns_inner(each,insdict.get(each),prev,next)
#	return (inslist,missing)

if __name__=="__main__":
	root=xml.dom.minidom.parse('status.xml')
#	(inslist,icall)=process_icall()
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
	attrcount=0
	fieldcount=0
	nslist=nsdict.keys()
	nslist.sort()
	for each in nslist:
		#print nsdict.get(each)
		(prev,next)=get_prev_next(nslist,each)
		(ctor,method,field,prop,event,attr)=print_namespace_inner(each,nsdict.get(each),prev,next)
		ctorcount=ctorcount+ctor
		propcount=propcount+prop
		fieldcount=fieldcount+field
		eventcount=eventcount+event
		methodcount=methodcount+method
		attrcount=attrcount+attr
	print_namespace_list(nslist,ctorcount,methodcount,fieldcount,propcount,eventcount,attrcount)
	

DGW_SRC=../html/xml/src/
DGW_DST=../html

all: index.html release.html screenshots.html acronyms.html free-software.html freedom.html danger.html \
 competition.html pnet.html pnet-install.html pnet-packages.html pnet-trackers.html pnet-cvs.html pnet-samples.html pnet-links.html \
 c-and-csharp.html functionality.html freedom.html web-services.html jabber.html arch.html auth.html stereo.html \
 testimonials.html win.html dgee.html see.html dee.html dgee-install.html dgee-packages.html dgee-run.html \
 dgee-samples.html dgee-faq.html vrs.html downloads.html lists.html irc.html join.html posters.html linking.html \
 projects.html patent-analysis.html ethics.html pubkeys.html snapshots.html manifesto.html html2.0/toc.html

html2.0/toc.html: xml/src/toc.xml
	(cd ../xml2html; ilrun dghtml.exe -i ${DGW_SRC}/toc.xml -o ${DGW_DST}/html2.0/toc.html -t ${DGW_SRC}/template_html2.xml -p ./${DGW_SRC}/ -r ../)

%.html : xml/src/%.xml xml/src/navlinks.xml xml/src/template_html2.xml xml/src/template_html4.xml 
	(cd ../xml2html; ilrun dghtml.exe -i ../html/$< -o ../html/$@ -t ${DGW_SRC}/template_html4.xml -p ./${DGW_SRC}/; ilrun dghtml.exe -i ../html/$< -o ${DGW_DST}/html2.0/$@ -t ${DGW_SRC}/template_html2.xml -p ./${DGW_SRC}/ -r ../)

index.html: xml/src/index.xml xml/src/navlinks.xml xml/src/template_html2.xml xml/src/template_html4.xml xml/src/news.xml
	(cd ../xml2html; ilrun dghtml.exe -i ../html/$< -o ../html/$@ -t ${DGW_SRC}/template_html4.xml -p ./${DGW_SRC}/; ilrun dghtml.exe -i ../html/$< -o ${DGW_DST}/html2.0/$@ -t ${DGW_SRC}/template_html2.xml -p ./${DGW_SRC}/ -r ../)

commit: all
	(export CVS_RSH=ssh; cvs commit)


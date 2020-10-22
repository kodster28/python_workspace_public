from bs4 import BeautifulSoup as bs
import os
import sys

#pull in path information from Flare. Triggered by post-build event on the Target
outputDestination = sys.argv[1]
initialSitemap = os.path.join(outputDestination, 'sitemap.xml')

#Open and get out the xml content into a string
with open(initialSitemap, "r") as file:
    sitemapContent = file.readlines()
    sitemapContent = "".join(sitemapContent)
    sitemap_bs_content = bs(sitemapContent, "html.parser")

#format the string into proper sitemap .html format
urls = [element.text for element in sitemap_bs_content.findAll('loc')]
urls.sort()
htmlElements = ["<ul style='list-style:none'>"]
for element in urls:
    htmlElements.append("<li><a href=" + element + ">" + element.split('/')[-1] + "</a></li>")
htmlElements.append("</ul>")
htmlPage = '\r\n'.join(htmlElements)

#create and save the new file in the output
updatedSitemap = open(os.path.join(outputDestination, "searchkb.html"), 'w')
updatedSitemap.write(htmlPage)
updatedSitemap.close()

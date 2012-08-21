from lxml import etree
import cStringIO
import pycurl

def add_elems_in_xml_tree ( tree, text, root_name):
 xml = etree.XML ( text)
# print root_name

 find=etree.XPath(root_name)
 lst=find(xml)
# print len(lst)
 root=tree.getroot()
 root.extend (lst)
 

def get_all_products ( log,pas,domen):
 page=""
 root=etree.Element("products")
 tree =etree.ElementTree(root)
 #tree.Element("products") 
 for i in range(1,100000):
  buf = cStringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.WRITEFUNCTION, buf.write)
  page="page="+str(i)
  url ="http://"+log+":"+pas+"@"+domen+"/admin/products.xml?"+page 
  print url
  c.setopt(c.URL,url )
  c.perform()
  tmp = buf.getvalue()
  buf.close()
#  print c.getinfo(pycurl.HTTP_CODE)
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
   print pycurl.HTTP_CODE
   return None
  if ( tmp.find('nil-classes') > -1):
   break
  add_elems_in_xml_tree ( tree, tmp, "product")
#  if i>0:
#   break
 tree.write("prods.txt")
 return tree
 
def get_collects (log,pas,domen ): 
 page=""
 root=etree.Element("collects")
 tree =etree.ElementTree(root)
 #tree.Element("products")
 for i in range(1,100000):
  buf = cStringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.WRITEFUNCTION, buf.write)
  page="page="+str(i)
  url ="http://"+log+":"+pas+"@"+domen+"/admin/collects.xml?"+page
  print url
  c.setopt(c.URL,url )
  c.perform()
  tmp = buf.getvalue()
  buf.close()
# print c.getinfo(pycurl.HTTP_CODE)
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
   print pycurl.HTTP_CODE
   return None
  if ( tmp.find('nil-classes') > -1):
    break
  add_elems_in_xml_tree ( tree, tmp, "collect")
 tree.write("collects.txt")
 return tree  

def get_collections (log,pas,domen ):
 root=etree.Element("collections")
 tree =etree.ElementTree(root)
 buf = cStringIO.StringIO()
 c = pycurl.Curl()
 c.setopt(c.WRITEFUNCTION, buf.write)
 url ="http://"+log+":"+pas+"@"+domen+"/admin/collections.xml"
 print url
 c.setopt(c.URL,url )
 c.perform()
 tmp = buf.getvalue()
 buf.close()
# print c.getinfo(pycurl.HTTP_CODE)
 if  c.getinfo(pycurl.HTTP_CODE)!=200 :
  print pycurl.HTTP_CODE
  return None
 add_elems_in_xml_tree ( tree, tmp, "collection")
 tree.write("collections.txt")
 return tree


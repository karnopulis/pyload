# -*- coding: cp1251 -*-
from lxml import etree
import cStringIO
import pycurl
import os
import httplib2

def post_product_in_collection ( product_id, collection_id ,log,pas,domen ):
 xml = '<?xml version="1.0" encoding="UTF-8"?><collect><collection-id type="integer">'+collection_id+'</collection-id><product-id type="integer">'+product_id+'</product-id></collect>'
# print xml
 buf = cStringIO.StringIO()
 headers = [ "Content-Type: text/xml; " ]
 try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/collects.xml" )
   c.setopt(c.HTTPHEADER, headers)
   c.setopt(pycurl.POST, 1)
   c.setopt(pycurl.POSTFIELDS, xml)
   c.perform()
#   print "post_product in collection"+collection_id,": status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
   tmp = buf.getvalue()
#   print xml
#   print tmp.decode('koi8-r')
 except pycurl.error, e:
  e
  return False
#   print "exception while adding products in collecions"+str(e[0])+"\n"
 if  c.getinfo(pycurl.HTTP_CODE) == 201:
  tmp = buf.getvalue()
  buf.close()
  tm = etree.XML(tmp)
  find = etree.XPath('id')
  tm =find ( tm )
  return True
#  print tm[0].text
 else :
  print "error posting product "+product_id+" in collection"+collection_id+ " status code" + str(c.getinfo(pycurl.HTTP_CODE))
  tmp = buf.getvalue()
  return False
#  print tmp.decode('koi8-r')  
#  print unicode(tmp,'cp1251')

def add_collection_to_site ( id,title,log,pas,domen ) :
  xml = '<collection><parent-id type="integer">'+id+'</parent-id><title>'+title.encode('utf-8')+'</title></collection>'
  buf = cStringIO.StringIO()
  headers = [ "Content-Type: text/xml; " ]
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/collections.xml" )
#   print "http://"+log+":"+pas+"@"+domen+"/admin/collections.xml"
   c.setopt(c.HTTPHEADER, headers)
   c.setopt(pycurl.POST, 1)
   c.setopt(pycurl.POSTFIELDS, xml)
   c.perform()
   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
   print "exception while adding collection "+str(e[0])+"\n"
   return None
  if  c.getinfo(pycurl.HTTP_CODE)!=201 :
   print "error at creating "+ title + str(c.getinfo(pycurl.HTTP_CODE))
#   print unicode(xml,'cp1251')
   return None
  tmp = buf.getvalue()
  print tmp
  tmp = etree.XML(tmp)
  find = etree.XPath('id')
  tmp =find ( tmp )  
  buf.close()
  return tmp[0].text

def add_product_in_products ( xml,log,pas,domen ) :
  buf = cStringIO.StringIO()
  headers = [ "Content-Type: text/xml; " ]
#  print xml
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/products.xml" )
#   print "http://"+log+":"+pas+"@"+domen+"/admin/products.xml"
   c.setopt(c.HTTPHEADER, headers)
   c.setopt(pycurl.POST, 1)
   c.setopt(pycurl.POSTFIELDS, xml)
   c.perform()
#   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
#   print "exception while adding collection "+str(e[0])+"\n"
   return None
#  if  c.getinfo(pycurl.HTTP_CODE)!=201 :
#   print "error at creating product " + str(c.getinfo(pycurl.HTTP_CODE))
#   return None
  tmp = buf.getvalue()
#  print tmp
  tmp = etree.XML(tmp)
  find = etree.XPath('//product/id')
  tmp =find ( tmp )
  if len(tmp) ==1:
   buf.close()
#   print tmp[0].text
   return tmp[0].text
  return None

def add_image_to_product ( xml,id,log,pas,domen ):
  buf = cStringIO.StringIO()
  headers = [ "Content-Type: text/xml; " ]
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/products/"+str(id)+"/images.xml" )
#   print "http://"+log+":"+pas+"@"+domen+"/admin/products/"+str(id)+"/images.xml" 
   c.setopt(c.HTTPHEADER, headers)
   c.setopt(pycurl.POST, 1)
   c.setopt(pycurl.POSTFIELDS, xml)
   c.perform()
#   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
#   print "exception while adding collection "+str(e[0])+"\n"
   return None
#  print pycurl.HTTP_CODE
#  if  c.getinfo(pycurl.HTTP_CODE)!=201 :
#   print "error adding image " + str(c.getinfo(pycurl.HTTP_CODE))
#   return None
  tmp = buf.getvalue()
#  print tmp
#  print tmp.decode('koi8-r')
  tmp = etree.XML(tmp)

def remove_collect ( collect, log,pas,domen ):
  buf = cStringIO.StringIO()
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/collects/"+collect+".xml" )
   c.setopt(c.CUSTOMREQUEST, "DELETE")
   c.perform()
   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
   print "exception deleting collect "+str(e[0])+"\n"
   return False
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
   print "error deleting collect"+ collect + " with error"+str(c.getinfo(pycurl.HTTP_CODE))
   return False
#  tmp = buf.getvalue()
#  print tmp
  return True

def remove_image( product_id,image_id, log,pas,domen ):
  buf = cStringIO.StringIO()
  try :
   xml ="http://"+log+":"+pas+"@"+domen+"/admin/products/"+ product_id+"/images/"+image_id+".xml"
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,xml)
   c.setopt(c.CUSTOMREQUEST, "DELETE")
   c.perform()
#   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
#   print "exception deleting image "+str(e[0])+"\n"
   return None
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
#   print "error deleting image"+ image_id+" product: "+product_id + " with error"+str(c.getinfo(pycurl.HTTP_CODE))
   return None
#  tmp = buf.getvalue()
#  print tmp

def remove_product_from_products ( product, log,pas,domen ):
  buf = cStringIO.StringIO()
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/products/"+product+".xml")
   c.setopt(c.CUSTOMREQUEST, "DELETE")
   c.perform()
#   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
#   print "exception deleting product "+str(e[0])+"\n"
   return None
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
#   print "error deleting product"+ product + " with error"+str(c.getinfo(pycurl.HTTP_CODE))
   return None
  tmp = buf.getvalue()
#  print tmp

def remove_collection ( coll_id, log,pas,domen ):
  buf = cStringIO.StringIO()
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   url ="http://"+log+":"+pas+"@"+domen+"/admin/collections/"+coll_id+".xml"
#   print url
   c.setopt(c.URL,url)
   c.setopt(c.CUSTOMREQUEST, "DELETE")
   c.perform()
   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
   print "exception deleting collection "+str(e[0])+"\n"
   return None
  if  c.getinfo(pycurl.HTTP_CODE)!=200 :
   return None
  return True

def post_product_in_collections ( product, colls , log, pas,domen ) :
 for col in colls :
#  print "___________"+col
  xml = '<?xml version="1.0" encoding="UTF-8"?><collect><collection-id type="integer">'+col+'</collection-id><product-id type="integer">'+product+'</product-id></collect>'
  buf = cStringIO.StringIO()
  headers = [ "Content-Type: text/xml; " ]
  try :
   c = pycurl.Curl()
   c.setopt(c.WRITEFUNCTION, buf.write)
   c.setopt(c.URL,"http://"+log+":"+pas+"@"+domen+"/admin/collects.xml" )
   c.setopt(c.HTTPHEADER, headers)
   c.setopt(pycurl.POST, 1)
   c.setopt(pycurl.POSTFIELDS, xml)
   c.perform()
#   print "status code: %s" %   c.getinfo(pycurl.HTTP_CODE)
  except pycurl.error, e:
   e
#   print "exception posting production in collection "+str(e[0])+"\n"

 if  c.getinfo(pycurl.HTTP_CODE) == 201:
  tmp = buf.getvalue()
  buf.close()
 else :
#  print "error posting product in collections "+product+ " status code" + str(c.getinfo(pycurl.HTTP_CODE))
  tmp = buf.getvalue()
#  print tmp.decode('koi8-r')


def post_seo_in_collection (  colls,seo, log, pas,domen ) :
  root=etree.Element("collection")
  tree =etree.ElementTree(root)
  mk= etree.SubElement( root,"meta-keywords")
  md= etree.SubElement( root,"meta-description")
  mk.text=seo
  md.text=seo
  tree.write("temp.xml")
  filesize = os.path.getsize("temp.xml")
  f=open("temp.xml", "r")
  s=f.read()
  
  http = httplib2.Http()
  http.add_credentials(log, pas)
  leen = {"Content-Type": "text/xml;charset=UTF-8"}
  ur="http://"+domen+"/admin/collections/"+colls+".xml"
  resp, content = http.request(ur, 'PUT', body=s, headers=leen)
 # print resp["status"]
  f.close()
 # if  resp["status"] != "200":
#   print "error posting in " +colls+ " status code" + str(resp["status"])

def edit_product_in_catalog (  xml, id_im, log, pas,domen ) :
  fi =open("temp.xml", "w")
  fi.write (xml)
  fi.close()
  filesize = os.path.getsize("temp.xml")
  f=open("temp.xml", "r")
  s=f.read()
  http = httplib2.Http()
  http.add_credentials(log, pas)
  leen = {"Content-Type": "text/xml;charset=UTF-8"}
  ur="http://"+domen+"/admin/products/"+id_im+".xml"
  #print ur
  (resp, content) = http.request(ur, 'PUT', body=s, headers=leen)
  #print resp["status"]

  f.close()
#  if  resp["status"] != "200":
#   print "error editing product" +id_im+ " status code" + str(resp["status"])
  (resp, content) = http.request(ur, 'GET', headers=leen)
  #print content
  tmp = etree.XML(content)
  find = etree.XPath ("//product/variants/variant/id")
  tmp = find (tmp)
  return tmp[0].text

def edit_variant (  xml, pr_id,var_id, log, pas,domen ) :
  fi =open("temp.xml", "w")
  fi.write (xml)
  fi.close()
  filesize = os.path.getsize("temp.xml")
  f=open("temp.xml", "r")
  s=f.read()
  http = httplib2.Http()
  http.add_credentials(log, pas)
  leen = {"Content-Type": "text/xml;charset=UTF-8"}
  #print pr_id
  #print var_id
  #print "_______"
  ur="http://"+domen+"/admin/products/"+pr_id+"/variants/"+var_id+".xml"
#  print ur
  (resp, content) = http.request(ur, 'PUT', body=s, headers=leen)
#  print resp["status"]
#  print content
  f.close()
#  if  resp["status"] != "201":
#   print "error editing variant " +pr_id+ " status code" + str(resp["status"])


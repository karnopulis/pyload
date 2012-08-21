from lxml import etree
import api_set
import ftplib

def find_collects_by_p_and_c ( tree, product_id,collection_id ):
 find = etree.XPath('//collect[product-id = \"'+product_id+'\" and collection-id=\"'+collection_id+'\"]')
 temp= find(tree);
 if len (temp)==0 :
  return None
 t= temp[0].find("id").text
 return t


def post_collects ( new_collects,log,pas,domen ):
 m=0
 for n in new_collects:
#  print n[0],n[1]
  rez = api_set.post_product_in_collection ( n[0].encode('utf8'),n[1].encode('utf8'), log,pas,domen )
#  print rez
  if rez:
   m=m+1
 return m

def remove_collects ( tree,old_collects,log,pas,domen ):
 m=0
 for n in old_collects:
  cl= find_collects_by_p_and_c ( tree,n[0],n[1] )
#  print cl
  rez = api_set.remove_collect ( cl.encode('utf8'),log,pas,domen )
  if rez:
   m=m+1
 return m


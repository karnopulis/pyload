from lxml import etree
import api_set
import ftplib

def create_collection_in_tree ( tree, title,id,parent_id):
 t_c= etree.SubElement ( tree,"collection" )
 t_c_i=etree.SubElement ( t_c,"id" )
 t_c_i.text=id
 t_c_p=etree.SubElement ( t_c,"parent-id" )
 t_c_p.text=parent_id
 t_c_t=etree.SubElement ( t_c,"title" )
 t_c_t.text=title

def find_collection_id_by_name ( tree,parent_id,name):
 if (parent_id):
  find = etree.XPath ('//collection[title = \"'+name+'\" and parent-id=\"'+parent_id+'\"]')
 else:
  find = etree.XPath ('//collection[title = \"'+name+'\"]')
 temp= find (tree)
 if ( len(temp)>0 ):
  temp = temp[0].find("id")
  return temp.text
 return None

def find_collection_name_by_id ( tree,id):
 find = etree.XPath ('//collection[id= \"'+id+'\"]')
 temp= find (tree)
 if ( len(temp)>0 ):
  temp = temp[0].find("title")
  return temp.text
 return None


def check_void_collection (  collection_id,tree ):
 find = etree.XPath('//collect[collection-id=\"'+collection_id+'\"]')
 temp= find(tree);
 if len (temp)==0 :
  return None
 else: 
  return True



def post_collections ( new_collections, old_collections,parent,collections_tree,log,pas,domen ):
  n=0
  print parent
  for nc in new_collections:
   to_do=list()
   suffix=nc
   while (1): 
    (first_part,delim,suffix)=suffix.partition("|")
    if suffix =="":
     to_do.append([first_part,suffix,parent])
     break
    if suffix in old_collections:
     id=old_collections[suffix]
    else:
     id=""
    to_do.append([first_part,suffix,id])
   to_do2=list()
   for td in to_do:
    to_do2.append (td)
    if td[2]!="":
     break
   to_do=to_do2 
   for i in range(0,len(to_do)):
    td=to_do.pop()
    if td[2]!="":
     id = td[2]
    id= api_set.add_collection_to_site ( id,td[0],log,pas,domen)
    if (id):
     create_collection_in_tree ( collections_tree.getroot(),td[0],id,td[2])
     old_collections[td[0]+'|'+td[1]]=id
     print [td[0]+'|'+td[1],id]
     n=n+1
    else:
     break
  return n

def remove_collections ( old_collections, log,pas,domen ):
 m=0
 for cl in old_collections:
   status = api_set.remove_collection (cl,log,pas,domen)
   if status:
    m=m+1
 return m

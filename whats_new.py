import csv
from operator import itemgetter
from horosho_volga import *
from codecs import iterdecode
from lxml import etree
import api_set
import copy
import time
import pprint

def acn_seqs (acn):
 rez=list()
 temp=list()
 for t in range (0,len(acn)-1):
  if acn[t]!="":
   temp.append (acn[t])
 for t in range (0,len(temp)):
  rez.append("|".join(temp))
  temp.pop(0)
 return rez
 
def colls_list ( table_new, colls_index ):
 if len (table_new)==0:
  return list()
 collects_new=list()
 ci=colls_index+[0]
 art_colls_new = map(itemgetter(*ci),table_new )
 art_colls_new=list ( set(art_colls_new))
 clls=list()
 for acn in art_colls_new:
  clls.extend(acn_seqs(acn))
 return list(set(clls ))

def prods_colls_dict ( table_new,prods_tree,collecions_old_style, colls_index, arts_index,arts_dict ):
 if len (table_new)==0:
  return list()
 collects_new=list()
 m= range(0,len(colls_index))
 ci=colls_index+[arts_index]
 art_colls_new = map(itemgetter(*ci),table_new )
 last =len(art_colls_new[0])-1
 pcd= dict()
 pcd2=dict()
 for acd in art_colls_new:
  temp =acn_seqs(acd)
  if acd[last] in arts_dict:
   prod_id = arts_dict[acd[last]]
   if prod_id == None :
    continue
  for t in temp:
   if t not in collecions_old_style:
    continue
   tt=collecions_old_style[t]
   if tt in pcd:
    tl=pcd[tt]
    tl.append(prod_id)
    tl2=pcd2[t]
    tl2.append(acd[last])
   else:
    new_list= list()
    new_list.append(prod_id)
    new_list2= list()
    new_list2.append(acd[last])
    pcd[tt]=new_list
    pcd2[t]=new_list2
# print len(pcd) 
# vk = pcd.iterkeys()
# for v in vk:
#  print v
# print "__________"
 strings=list()
 for ik in pcd2.iterkeys():
  temp= ik+": "+";".join(pcd2[ik])+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("acd.txt", 'w')
 output.writelines(strings)
 output.close()
 strings=list()
 for ik in pcd.iterkeys():
  temp= ik+": "+";".join(pcd[ik])+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("acd_num.txt", 'w')
 output.writelines(strings)
 output.close()

 return pcd,pcd2 

 
def read_rows_from_file (file):
 f=open(file)
 return f.readlines()
 
def minus(o1,o2):
 s1=set(o1)
 s2=set(o2)
 return s1-s2

def inter(o1,o2):
 s1=set(o1)
 s2=set(o2)
 return s1&s2

def outer(o1,o2):
 s1=set(o1)
 s2=set(o2)
 s=s1&s2

 s=(s1-s)|(s2-s)
 return s

def complex(o1,o2):
 m1=minus(o1,o2)
 m2=minus(o2,o1)

 return m1&m2

def subtree_in_tree_clause ( subtree ,tree ):
 n=len(subtree) - subtree.count('')
 m=len(tree) - tree.count('')
 for i in range (0,m-n+1):
  lyes=0
  for j in range(0,n):
   if subtree[j]==tree[j+i]:
    lyes=lyes+1
  if lyes==n:
   return True
 return False

def find_product_id_by_artikul ( tree, art ):
 find=etree.XPath ('//*/variant[sku = \"'+art+'\"]')
 temp=find(tree.getroot())
 if len (temp)>1:
  print "Two products with same sku:" +art
 if len(temp)==0:
  return None
# print "finded product by artikul:"+temp[0].find("product-id").text
 return temp[0].find("product-id").text


def find_new_artikuls_by_collection( colle,art_colls_new,prods_tree):
 arts=list()
 for acn in art_colls_new:
  temp=copy.copy(list(acn))
  temp.pop()
  if subtree_in_tree_clause(colle,temp):
   id =find_product_id_by_artikul (prods_tree,acn[len(acn)-1])
   if id:
    arts.append(id)
# print n
 return arts

def old_colls_dict ( collections, collects_tree ):
 rez=dict()
 for col  in collections.itervalues() :
  find = etree.XPath('//collect[collection-id = \"'+col+'\"]')
  temp= find(collects_tree)
  prom=list()
  if len (temp)>0:  
   for tm in temp:
    t= tm.find("product-id").text
    prom.append(t)
  rez[col]=prom
 strings=list()
 for ik in rez.iterkeys():
  temp= ik+": "+";".join(rez[ik])+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("old_acd.txt", 'w')
 output.writelines(strings)
 output.close()

 return rez 

 


def find_old_artikuls_by_collection (col_id,collects_tree ):
 arts=list()
# print col_id
 find = etree.XPath('//collect[collection-id = \"'+col_id+'\"]')
 temp= find(collects_tree)
 if len (temp)==0:
  return list()
 for tm in temp:
  t= tm.find("product-id").text
  arts.append( t )
# artss=list()
# for a in arts:
#  find = etree.XPath('//product[id = \"'+a+'\"]')
#  temp= find(arts_tree);
#  if (len(temp))>0:
#   artss.append (temp[0].find("title").text)
# ttt=""
# for co in artss:
#  ttt=ttt+co+","
# print ttt

 return arts 

def new_artikuls ( table_new,table_old,art_index ):
# new=read_rows_from_file("site.csv")
# old=read_rows_from_file("site_old.csv")
 #arts_old = map(itemgetter(art_index),table_old)
 if len ( table_new) ==0:
  print "len of table_new=0"
  return  list()

 arts_new = map(itemgetter(art_index),table_new)
 if len ( table_old) ==0:
  print "len of table_old=0"
  return  list(arts_new) 
 arts_old=table_old.iterkeys()
 new_arts = set(arts_new)-set(arts_old)
 return list(new_arts)

def new_collections ( colls_new,dict_old ):
 strings=list()
 for ik in colls_new:
  temp= ik+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("colls_csv.txt", 'w')
 output.writelines(strings)
 output.close()
 colls_old = list(dict_old.iterkeys())
 strings=list()
 for ik in list(colls_old):
  temp= ik+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("colls_site.txt", 'w')
 output.writelines(strings)
 output.close()
 new_colls = set(colls_new) - set(colls_old)
 old_colls = set(colls_old) - set(colls_new)

 strings=list()
 for ik in list(new_colls):
  temp = ik+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("new-colls.txt", 'w')
 output.writelines(strings)
 output.close()
 strings=list()
 for ik in list(old_colls):
  temp= ik+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("old-colls.txt", 'w')
 output.writelines(strings)
 output.close()
 colls_to_delete=list()
 for o in old_colls:
  colls_to_delete.append(dict_old[o])
# ttt=""
# for co in colls_new:
#  ttt=""
#  for tt in co:
#   ttt=ttt+tt+","
#  print ttt
 return list(new_colls),colls_to_delete
 
def new_collects ( new_colls_dict,old_colls_dict ):
 collects_new=list()
 collects_old=list()
 i=len(old_colls_dict)
 for col in new_colls_dict.iterkeys():
  new_arts = new_colls_dict[col]
  if col in old_colls_dict:
   old_arts = old_colls_dict[col] 
  else:
   i=i-1
   print i
   continue
  arts_new = set(new_arts)-set(old_arts)
  arts_old = set(old_arts)-set(new_arts)
  for a in list(arts_new):
   row=[a,col]
   collects_new.append(row)
  for a in list(arts_old):
   row=[a,col]
   collects_old.append(row)
 strings=list()
 for ik in list(collects_new):
  temp= ";".join(ik)+"\n"
  temp=temp.encode("utf8")
  strings.append(temp)
 output = open("collects-new.txt", 'w')
 output.writelines(strings)
 output.close()
 #print len (collects)
 return collects_new,collects_old

def old_artikuls ( table_new,table_old,art_index ):
# new=read_rows_from_file("site.csv")
# old=read_rows_from_file("site_old.csv")
# arts_old = map(itemgetter(art_index),table_old)
 arts_old = table_old.iterkeys()
 arts_new = map(itemgetter(art_index),table_new)
 new_arts = set(arts_old)-set(arts_new)
 return list(new_arts)


def edited_artikuls ( arts_old,table_new, pa_prod, pr_prod, pr_var  ):
 if len ( table_new) ==0:
  print "len of table_new=0"
  return  list()
 n = len ( table_new[0])
 n = pa_prod + pr_prod + pr_var
 #print n
 arts_new = map(itemgetter(*n),table_new)

 if len ( arts_old) ==0:
  print "len of table_old=0"
  return  list()

 m= range(0,len(arts_old[0]))
 arts_old = map(itemgetter(*m),arts_old)
 new_arts = set(arts_new)-set(arts_old)
 edited_arts = map(itemgetter(len(pa_prod+pr_prod)),list(new_arts))

 return edited_arts

def noimage_artikuls ( prods_tree,table_new_decoded,im ):
 prods=prods_tree.findall("//product")
 n=list()
 for p in prods:
  image=False
  pp=p.find("id")
  t=p.findall("images/image")
  a=p.find("variants/variant/sku")
  print len (t)
  if len (t)==0:
   n.append(a.text)
  else:
   for j in range(0,len(t)):
    tt=t[j].find("original-url")
    if  tt.text.find ("no_image_original")>-1:
     ii=t[j].find("id")
     #print "removing void image from: "+ pp.text
     api_set.remove_image( pp.text,ii.text, log,pas,domen )
    else:
     if image ==True:
      ii=t[j].find("id")
      #print "removing duplicate image from: "+ pp.text
      api_set.remove_image( pp.text,ii.text, log,pas,domen )
     else:
      image=True
   if image==False:
     n.append(a.text)
   

#   print a.text 
 return n
#print "n-o"+ str(len(new))+":"+ str(len(old))
#print "unik n-o"+ str(len(set(new)))+":"+ str(len(set(old)))
#print "minus o-n:"+ str(len(minus( old,new )))
#print "minus n-o:"+ str(len(minus( new,old )))
#print "inter"+ str(len(inter( new,old )))
#print "outer"+ str(len(outer( new,old )))
#print "complex"+ str(len(complex( new,old )))
#list = list(complex( new,old ))


 # -*- coding: utf-8 -*-
from lxml import etree
import csv
import pprint
import pycurl
import cStringIO
import api_get
import api_set
from ftplib import FTP
import post_product
import post_collection
import post_collects
from codecs import iterdecode
#import my_xml
import sys
from horosho_volga import *
import whats_new

def connect_ftp (host_name,ftp_log,ftp_pas):
 ftph = FTP(host_name)
 try: ftph = FTP(host_name)
 except:
	print "Host could not be resolved."
	raw_input()
	sys.exit()
 else: pass
 try:
	ftph.login(ftp_log,ftp_pas)
 except Exception:
		print "Invalid login combination."
		raw_input()
		sys.exit()
 else:
	print "Successfully connected!\n"
 print ftph.getwelcome()
 return ftph

def download_ftp(handle,filename):
	f2 = open(filename,"wb")
	try:
		handle.retrbinary("RETR " + filename,f2.write)
	except Exception:
		print "Error in downloading the remote file."
		return
	else:
		print "Successful download!"
	f2.close()
	return

def list_decode ( list_d, cp ):
 ls =[]
 for l in list_d:
  ls.append (l.decode( cp ))
 return ls

def table_decode ( table_d, cp ):
 tb=[]
 for t in table_d:
  li=[]
  for l in t:
   li.append( l.decode (cp))
  tb.append(li)
 return tb 


def index_of_column ( columns,name ):
 try:
  temp = columns.index(name.decode('utf-8').encode('cp1251'))
 except:
  print name
 return  temp

def index_of_catalog ( columns, col_names ):
 tmp=[]
 for col in col_names:
#  print col
  tmp.append( index_of_column (columns,col) )
 return tmp

def categories ( columns, indexes,top_s ):
 tmp=[]
 for i in indexes:
  if columns[i]!="":
   if columns[i]!=top_s.decode('utf-8').encode('cp1251'):
    tmp.append(columns[i])
 return tmp      

def find_collects_by_product ( tree, product_id,except_collection ):
 find = etree.XPath('//collect[product-id = \"'+product_id+'\" and collection-id!=\"'+except_collection+'\"]')
 temp= find(tree);
 if len (temp)==0 :
  return None
 tmp=[]
 for tm in temp:
  t= tm.find("id").text
  tmp.append( t )
 return tmp

def find_dublicates_in_products ( prods_tree ):
 fh = open("prods.txt", 'r')
 st = fh.read()
 st=st.decode('cp1251').encode('utf-8')
 prods_tree1=etree.XML(st)
 temp=prods_tree1.findall("product") 
 if len ( temp )==0:
  print "Error: no products"
 deleted=[]
 for tmp in temp:
  cur =tmp.find("variants/variant/sku")
  if cur.text==None:
   continue
#  print cur.text
#  print cur.text.decode('utf-8').encode('cp1251')
  find=etree.XPath ('//product/variants/variant[sku = \"'+cur.text+'\"]')
  sim=find(prods_tree1)
  if len (sim)==1 :
   continue
  else:
   try:
    ttt=deleted.index( cur.text )
    #print deleted[ttt]   
   except: 
    #print "finded duplicated sku:"+cur.text+"Number dubles:"+str(len(sim))
    q=len(sim)
    for i in range(0,len(sim)):
     if q> len(sim)-i :
      #print "removed product"+ sim[i].find("product-id").text
      api_set.remove_product_from_products ( sim[i].find("product-id").text,log,pas,domen )
      deleted.append(cur.text)
      q=q-1
     else:
      if sim[i].find("quantity").text=="0":
       #print "removed product"+ sim[i].find("product-id").text
       api_set.remove_product_from_products ( sim[i].find("product-id").text,log,pas,domen )
       deleted.append(cur.text) 
       q=q-1
    #print deleted 
 return temp
  

def find_product_id_by_artikul ( tree, art ):
 find=etree.XPath ('//*/variant[sku = \"'+art.decode('cp1251')+'\"]')
 temp=find(tree.getroot())
# if len (temp)>1:
  #print "Two products with same sku:" +art.decode('cp1251').encode('cp1251')
# if len(temp)==0:
  #print " Product not finded in products:"+ art.decode('cp1251').encode('cp1251')
#  return None
# print "finded product by artikul:"+temp[0].find("product-id").text
 return temp[0].find("product-id").text

def find_parent_collections ( tree, collection_id ):
 try :
  find = etree.XPath('//collection[id = \"'+collection_id+'\"]')
  temp= find(tree);
 except :
  return None
# print collection_id,len (temp)
 if len (temp)==0 :
  return None
 tmp=temp[0].find("parent-id")
# print tmp
 try :
  tmp.attrib["nil"]
 except :
#  print "+++++"+tmp.text
  return tmp.text
 return None


def if_product_in_collection ( tree,product_id, collection_id):
 find=etree.XPath ('//collect[product-id=\"'+product_id+'\" and collection-id=\"'+collection_id+'\"]')
 temp=find(tree.getroot())
 if len(temp)==0:
  return False
 else :
#  print "product" + product_id+" allready in collection " + collection_id
  return True

def art_tree_to_table ( tree, art_index, pa_prod,parametri_produkta_site,
 pr_prod,priznaki_produkta_site,
 pr_var,priznaki_varianta):
  cs=dict()
  s=tree.findall("//product")
  for i in range(0,len(s)):
   art=s[i].find("variants/variant/sku")
   id =s[i].find("id")
   if art.text is not None:
    cs[art.text]=id.text
  #print " products in tree" + str (len (cs) )
  return cs
#  print cs

def collections_tree_to_table(tree,cat_index,parent):
 table=list()
 style=dict()
 tmp=tree.findall("//collection")
 for t in tmp:
  cp=t.find("id").text
  temp=[""]*(len(cat_index)+1)
  if cp!=parent:
   temp[0]=t.find("title").text
   temp[len(temp)-1]=cp
#  print temp 
  for i in range (1,1000):
    cp=find_parent_collections ( tree, cp )
#    print cp
    if cp==None:
     if parent not in temp:
      temp[0]=None
      break
    if cp==parent:
     break
    temp[i]=post_collection.find_collection_name_by_id(tree,cp)
  if temp[0]:
   table.append(temp)
   nt=list()
   for t in temp:
    if t!="" and t!=temp[len(temp)-1]:
     nt.append(t)
   style["|".join(nt)]=temp[len(temp)-1]
#   ttt=""
#   for tt in temp:
#    ttt=ttt+","+tt
#   print ttt

 #print "number of collections: "+str(len(table))
 return table,style
 
def prods_tree_to_table ( tree, parametri_produkta_site,
  priznaki_produkta_site,priznaki_varianta,key_fields_site):
  cs=[]
  s=tree.findall("//product")
  for i in range(0,len(s)):
   c=[]
   for pa in parametri_produkta_site:
#    print pa
    t=s[i].find(pa)
    if t.text is None:
     c.append("")
    else:
     c.append(t.text)
     
#     print t.text
   for pp in priznaki_produkta_site:
#    print pp
    find = etree.XPath("properties/property[title=\'"+pp.decode("utf-8")+"\']")
    t=find(s[i])
    if len(t) !=0 :   
     t=t[0].find("id").text
 #   print t
     find1 = etree.XPath("characteristics/characteristic[property-id=\'"+t+"\']")
     t=find1(s[i])
     t=t[0].find("title")
     if t is None:
      c.append("")
     else:
#      print t.text
      c.append(t.text)
    else:
     c.append("")
   for pv in priznaki_varianta:
#    print pv
    t=s[i].find("variants/variant/"+pv)
    if t != None:     
     if t.text is None:
      c.append("")
     else:
      if pv.find("price")>-1:
       c.append(t.text)
      else:
       c.append(t.text)
    else:
       c.append("")
   cs.append(c)
 #  if  ";".join(c).find("03.051")!=-1:
 #    print ";".join(c)
 #    return
    
  #print " products in tree" + str (len (cs) )
  f = open("pttt.txt","w") 
  for st in cs:
   res=""
   for sst in st:
    res= res+ sst +";"
   f.write((res+"\n").encode('utf-8'))
  f.close
  return cs



def remove_product_from_products ( tree, product_id ):
 find= etree.XPath ( '//product[id= \"'+product_id +'\"]')
 temp = find(tree.getroot())
# len1 = tree.getroot().findall("product")
 if len (temp) == 0:
   #print "product" + product_id +" not finded in products "
   return 
 tree.getroot().remove(temp[0])
# len2 = tree.getroot().findall("product")
# print len (len1)
# print len (len2)

def remove_collections(tree,log,pas,domen):
 tmp=tree.findall("//collection/id")
 #print "collections"+ str(len (tmp))
# for t in tmp:
#  print t.text
#  api_set.remove_collection(t.text,log,pas,domen)
#  print "_________"
def remove_collects(tree,log,pas,domen):
 tmp=tree.findall("//collect/id")
 #print "collects"+str(len (tmp))
# for t in tmp:
#  print t.text
#  api_set.remove_collect(t.text,log,pas,domen)
#  print "___________"


def kroshki (collections_tree,collects_tree,cols,prod_id,log,pas,domen):
 if (prod_id==None):
  return
 colls = []
 while True :
  if ( if_product_in_collection (collects_tree, prod_id, cols) == False ):
   colls.append (cols)
   #print "add kroshka: "+str(cols)
  cols = find_parent_collections ( collections_tree, cols )
  #print "parent: "+str(cols)

  if cols == None  :
   break
 try :
  colls.remove(colls[len(colls)-1])
  colls.remove(colls[len(colls)-1])
 except:
  True
 if colls :
  #print "kroshki quantity:"+str(len(colls))
  api_set.post_product_in_collections ( prod_id ,colls,log, pas,domen )
 
def initial_load( table,art_new,art_edited,art_old,art_noimage,prods_tree,
 art_index,top_level_category_id, pa_prod,parametri_produkta_site,
 pr_prod,priznaki_produkta_site,
 pr_var,priznaki_varianta_site,im,log,pas,domen):
 n=len (art_new)
 o=len (art_old)
 e=len (art_edited)
 ni=len (art_noimage)
 for i in range(0,len(table)):
  art = table[i][art_index].decode('cp1251')
  if art in art_new :
   n=n-1
#   print "new__" + art.encode('utf-8')+"___ "+str(art_new.index(art))+"______" + str (n)   
   id = post_product.post_product_in_catalog ( table[i],prods_tree,top_level_category_id,
    pa_prod,parametri_produkta_site,pr_prod,priznaki_produkta_site,
    pr_var,priznaki_varianta_site,im,log,pas,domen)
   if id is not None:
    post_product.add_image_to_product (id,table[i][im],log,pas,domen)
  else:
   if art in art_edited:
    e=e-1
#    print "edited___" + art.encode('utf-8')+"___ "+str(art_edited.index(art))+"______" + str (e)
    prod_id = find_product_id_by_artikul ( prods_tree, art.encode('cp1251'))
    post_product.edit_product_in_catalog ( table[i],prod_id,top_level_category_id,
     pa_prod,parametri_produkta_site,pr_prod,priznaki_produkta_site,
     pr_var,priznaki_varianta_site,im,log,pas,domen)
   if art in art_noimage:
    ni=ni-1
#    print "noimage : " + art.encode('utf-8')+"___ "+str (ni)
    prod_id = find_product_id_by_artikul ( prods_tree, art.encode('cp1251'))
    if prod_id is not None:
     post_product.add_image_to_product (prod_id,table[i][im],log,pas,domen)
 for oo in art_old :
  o=o-1
#  print " old : " + oo.encode('utf-8')+"___ "+str (o)
  prod_id = find_product_id_by_artikul ( prods_tree, oo.encode('cp1251') )
  api_set.remove_product_from_products ( prod_id,log,pas,domen )
   
 return None 
def check_and_repair ( table_new, pa_prod,pr_prod,pr_var,priznaki_varianta_site):
# check prices format
 table_new.pop(0)
 n= list()
 i=0
 for pv in priznaki_varianta_site:
  if pv.find("price")>-1 :
   try:
    n.index(pr_var[i])
   except:
    n.append(pr_var[i])
  i=i+1 
 for row in table_new:
  for pric in n:
   if row[pric]=="":
    continue
   temp=row[pric].replace(',','.')
#   print row[pric]
#   print temp
#   print row
   if temp==row[pric]:
    row[pric]=str(float(int(temp)))
   else:
    row[pric]=str(float(temp))
 #print n
 return table_new

prods_tree= api_get.get_all_products(log,pas,domen)
prods_tree=etree.parse("prods.txt")
collects_tree = api_get.get_collects ( log,pas,domen )
collects_tree=etree.parse("collects.txt")
collections_tree = api_get.get_collections ( log,pas,domen )
collections_tree=etree.parse("collections.txt")

ftph = connect_ftp (ftp_host_name.decode("utf-8"),ftp_log,ftp_pas)
ftph.cwd(ftp_dir)
download_ftp (ftph,ftp_file)
new_file = open(ftp_file, 'r')
print "reading file: "+ftp_file
table_new = [row for row in csv.reader(new_file,delimiter=';')]
#old_file = open('soshi_old.csv', 'r')
#table_old = [row for row in csv.reader(old_file,delimiter=';')]
table = table_new
cat_index = index_of_catalog ( table[0], catalog )
art_index = index_of_column ( table[0], artikul )
pa_prod = index_of_catalog ( table[0],parametri_produkta_csv )
pr_prod = index_of_catalog ( table[0],priznaki_produkta_csv )
pr_var = index_of_catalog ( table[0],priznaki_varianta_csv )
key_fields = index_of_catalog ( table[0],key_fields_csv )
im = index_of_column ( table[0],image_csv )
table_new =check_and_repair ( table_new, pa_prod,pr_prod,pr_var,priznaki_varianta_site)

fh = open("collections.txt", 'r')
cts = fh.read()
collections = etree.XML (cts)
parent = post_collection.find_collection_id_by_name( collections, None , top_level_dest_name.decode('utf-8') )
if parent==None:
 print "error finding root object :"+ top_level_dest_name
 sys.exit()
id=parent
spec = post_collection.find_collection_id_by_name( collections, None , special_dest_name.decode('utf-8') )
print "morphing input information"
arts_old_table = art_tree_to_table ( prods_tree, art_index, pa_prod,
        parametri_produkta_site,
        pr_prod,priznaki_produkta_site,
        pr_var,priznaki_varianta_site)
arts_old= prods_tree_to_table ( prods_tree, parametri_produkta_site,
  priznaki_produkta_site,priznaki_varianta_site,key_fields_site)
collections_old,collections_old_style= collections_tree_to_table(collections_tree,cat_index,parent)
#table_old_decoded = table_decode ( table_old,'cp1251' )
table_new_decoded = table_decode ( table_new,'cp1251' )
acd,acd2= whats_new.prods_colls_dict ( table_new_decoded,prods_tree,collections_old_style, cat_index, art_index, arts_old_table)
new_colls = whats_new.colls_list (table_new_decoded,cat_index)

#prods_in_tree = list_decode ( prods_in_tree,'utf-8' )

#print special_dest_name
#print spec
print "calculating articuls"
new_arts = whats_new.new_artikuls ( table_new_decoded,arts_old_table,art_index  )
#print new_arts
old_arts = whats_new.old_artikuls ( table_new_decoded,arts_old_table,art_index  )
print "new artikuls: "+str( len(new_arts))
print "old artikuls: "+str( len(old_arts))
#print old_arts
new_collections,old_collections = whats_new.new_collections ( new_colls,collections_old_style )
print "new collection chains:" + str ( len ( new_collections ) )
print "old collection chains:" + str ( len ( old_collections ) )
edit_arts = whats_new.edited_artikuls ( arts_old,table_new_decoded, pa_prod,
 pr_prod,pr_var  )
noimage_arts = whats_new.noimage_artikuls ( prods_tree,table_new_decoded,im )
#noimage_arts=list()
print "noimage arts:"+ str ( len(noimage_arts))
print "edited artikuls: "+str( len(edit_arts)- len(new_arts))
#remove_collections (collections_tree,log,pas,domen)
#remove_collects (collects_tree,log,pas,domen)
print "processing products..."
initial_load ( table,new_arts,edit_arts,old_arts,noimage_arts,prods_tree,art_index,top_level_category_id, 
 pa_prod,parametri_produkta_site,pr_prod,priznaki_produkta_site,
 pr_var,priznaki_varianta_site,im,log,pas,domen)
print "processing collections..."
collections_added =post_collection.post_collections ( new_collections,collections_old_style,parent,collections_tree,log,pas,domen)
print "collections added :" + str(collections_added)
#collections_new,collections_new_style = collections_tree_to_table(collections_tree,cat_index,parent)
print "calculating dictionary..."
dict_new_collects,dnc= whats_new.prods_colls_dict ( table_new_decoded,prods_tree,collections_old_style,cat_index,art_index,arts_old_table)
dict_old_collects= whats_new.old_colls_dict ( collections_old_style, collects_tree )
print "calculating collects..."
(new_collects,old_collects) = whats_new.new_collects ( dict_new_collects,dict_old_collects )
print "new collects: " + str ( len(new_collects) )
print "old collects: " + str ( len(old_collects) )
collects_added = post_collects.post_collects ( new_collects,log,pas,domen )
print "collects added:" + str ( collects_added )
collects_removed = post_collects.remove_collects ( collects_tree,old_collects,log,pas,domen )
print "collects removed:" + str ( collects_removed )
#collects_tree = api_get.get_collects ( log,pas,domen )
collections_removed = post_collection.remove_collections ( old_collections, log,pas,domen )
print "collections removed :" + str(collections_removed)

id=parent
print "_______________"
sys.exit()
#find_dublicates_in_products(prods_tree)
#sys.exit()

for i in range (0,len(table)):
 tmp =categories( table[i], cat_index,top_level_source_name )
 for j in range(0,len(tmp)):
  tm=tmp[j]
  print tm.decode('cp1251').encode('utf-8')
  id_old=id
#  print id_old
  id=post_collection.find_collection_id_by_name ( collections,id ,tm )
  if (id):  
   True
   if j==0:
    first_col=id
   print "finded"+id
  else:
   id= api_set.add_collection_to_site ( id_old,tm.decode('cp1251').encode('utf-8'),log,pas,domen)
   if j==0:
    first_col=id
   print "new  "+str(id)
   if (id):
#    create_collection_in_tree ( collections,tm.decode('cp1251'),id,id_old)
    collections.write(id+".txt")
   else :
    break
 print "_________________"       
# print (unicode(tmp[len(tmp)-1],'cp1251'))+ unicode (len(tmp))
 art = table[i][art_index]
 prod_id = find_product_id_by_artikul ( prods_tree, art )
 print prod_id 
 if (prod_id): 
  if ( if_product_in_collection (collects_tree, prod_id, id) == False ): 
   api_set.post_product_in_collection ( prod_id,id,log,pas,domen )  
   print " not in"
  remove_product_from_products ( prods_tree, prod_id )
 print id
 kroshki (collections_tree,collects_tree,id,prod_id,log,pas,domen)
 id=parent
# print "_________________"
# if i>15:
#  break

prods=prods_tree.getroot().findall("product")
for i in range(0,len(prods)-1):
 prod_id=prods[i].find("id").text 
 colls= find_collects_by_product ( collects_tree,prod_id,spec )

 if colls==None:
#  print " no collects"
  continue 
 for col in colls:
#  print "delete"
#  print prod_id
#  print col 
#  print "___________________"
  if col!=spec :
   api_set.remove_collect (col,log,pas,domen)
  else:
    print spec
# if i> 11:
#  break
#find_dublicates_in_products(prods_tree)

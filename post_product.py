from lxml import etree
import api_set
import ftplib


def modtime(filename):
 print "Retrieve the modtime of a file."
 resp = ftplib.sendcmd('MDTM ' + filename)
 if resp[:3] == '213':
  s = resp[3:].strip()
  return s
 else:
  return None

def add_elements( root,table, site, in_csv):
 size=len(site)
 if size!=len(in_csv):
  print "error in parameters in post_product_in_catalog"
  return None
 for i in range(0,size):
  tl=etree.SubElement( root, site[i])
#  print site[i]
#  if site[i].find("price")>-1:
#   tl.text=str(float(int(table[in_csv[i]].decode('cp1251').replace(',','.'))))
#   print "v "+ site[i]+ "price " + tl.text
#  else:
  tl.text=table[in_csv[i]].decode('cp1251')
#  print tl.text.encode('utf-8')
#  if tl.tag=="quantity":
#   tl.attrib["type"]="integer"
#  if tl.tag=="price":
#   tl.attrib["type"]="decimal"
#  if tl.tag=="price3":
#   tl.attrib["type"]="decimal"

def add_properties( root,table, site, in_csv):
 size=len(site)
 if size!=len(in_csv):
  print "error in parameters in post_product_in_catalog"
  return None
 t=etree.SubElement( root, "properties-attributes",type="array")
 for i in range(0,size):
  t0=etree.SubElement( t, "properties-attribute" )
  t1=etree.SubElement( t0, "title")
  t1.text=site[i].decode('utf-8')
  t2=etree.SubElement( t0, "value")
  t2.text=table[in_csv[i]].decode('cp1251')

def edit_product_in_catalog ( table, id, cat_top, pa_prod,pa_prod_site,
 pr_prod,pr_prod_site, pr_var,pr_var_site,id_im,log,pas,domen):
 xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
 root=etree.Element("product")
 tree =etree.ElementTree(root)
# t0=etree.SubElement( root, "category-id",type="integer")
# t0.text=cat_top
 tid=etree.SubElement( root, "id",type="integer")
 tid.text=id
 add_elements(root,table,pa_prod_site,pa_prod)
 add_properties(root,table,pr_prod_site,pr_prod)
# s1=etree.SubElement( root, "cost-price",type="decimal",nil="true")
# s2=etree.SubElement( root, "old-price",type="decimal",nil="true")
 
 xml=xml_head+etree.tostring(root, encoding="utf-8", method="xml")
# print xml
 var_id=api_set.edit_product_in_catalog ( xml,id,log,pas,domen )
 edit_variant ( table, id, var_id, pr_var, pr_var_site,log,pas,domen )

def post_product_in_catalog ( table,prods_tree, cat_top, pa_prod,pa_prod_site,
 pr_prod,pr_prod_site, pr_var,pr_var_site,id_im,log,pas,domen):
 xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
 root=etree.Element("product")
 tree =etree.ElementTree(root)
 t0=etree.SubElement( root, "category-id",type="integer")
 t0.text=cat_top
 add_elements(root,table,pa_prod_site,pa_prod)
# print "__________"
 add_properties(root,table,pr_prod_site,pr_prod)
 t1=etree.SubElement( root, "variants-attributes",type="array")
 t2=etree.SubElement( t1, "variant")
 add_elements(t2,table,pr_var_site,pr_var)
# print "___________"
# s1=etree.SubElement( root, "cost-price",type="decimal",nil="true")
# s2=etree.SubElement( root, "old-price",type="decimal",nil="true")
 xml=xml_head+etree.tostring(root, encoding="utf-8", method="xml")
# print xml
 id =api_set.add_product_in_products ( xml,log,pas,domen )
 if id:
  t3=etree.SubElement (root,"id",type="integer")
  t3=id
  t4 = etree.SubElement(t2,"product-id",type="integer")
  t4=id
  prods_tree.getroot().append(root)
 return id

def edit_variant ( table, pr_id, var_id, pr_var, pr_var_site,log,pas,domen):
 xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
 roote=etree.Element("variant")
 treee =etree.ElementTree(roote)
 add_elements(roote,table,pr_var_site,pr_var)
 xmle=xml_head+etree.tostring(roote, encoding="utf-8", method="xml")
# print xmle
 api_set.edit_variant ( xmle,pr_id,var_id,log,pas,domen )

def add_image_to_product ( id,id_im,log,pas,domen ):
 xml_head = '<?xml version="1.0" encoding="UTF-8"?>'
 rooti=etree.Element("image")
 treei =etree.ElementTree(rooti)
 it=etree.SubElement(rooti,"title",nil="true" )
 its=etree.SubElement(rooti,"src" )
 its.text=id_im.decode("cp1251")
 xmli=xml_head+etree.tostring(rooti, encoding="utf-8", method="xml")
# print xmli
 api_set.add_image_to_product ( xmli,id,log,pas,domen )

from lxml import etree
import api_get
import api_set
log = "f3e029120b56b2c4a0f554abbb009eb2"
pas = "24e491fca4ac082d63ac20131788d287"
domen = "horosho-ufa.ru"


def generate_seo (log,pas,domen):
 collections =api_get.get_collections(log,pas,domen)
 cols =collections.getroot().findall("collection")

 for col in cols:
  word=col.find("title").text+": "
  id = col.find("id").text
  find = etree.XPath("//collection[parent-id=\'"+id+"\']")
  cl=find(collections)
  for c in cl:
   word=word + c.find("title").text+", "
  api_set.post_seo_in_collection(id,word,log,pas,domen)



generate_seo (log,pas,domen)



def delete(content):
  start = content.find('<')
  end = content.find('>', start)
  result = content[:start] + content[end + 1:]
  return result


def getClearPage(content):
  title = content[content.find("<title>")+7:content.find("</title>")]
  body = content[content.find("<body>")+6:content.find("</body>")]

  while body.find('>') != -1:
    start = body.find('<')
    end = body.find('>')
    body = body[:start] + body[end + 1:]

  return title + body


def getPage(url):
  try:
    import urllib.request
    page = urllib.request.urlopen(url).read()
    page = page.decode("utf-8")
    return page
  except:
    return ""




def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote



def get_all_links(page):
    links = []
    while True:
      url, endpos = get_next_target(page)
      if url:
        links.append(url)
        page = page[endpos:]
      else:
        break
    return links


def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)



def add_to_index(index, keyword, url):
  if keyword in index: #modified bu kısmı değiştirdim, tek tek aramak yerine kontrol ederek ekliyor
    if url not in index[keyword]: #Q1 - D
      index[keyword].append(url)
  else:
    index[keyword] = [url]



def addPageToIndex(index, url, content):
  words = content.split()
  for word in words:
    add_to_index(index, word, url)


def lookup(index, keyword):
  if keyword in index: #modified, keyword var mı diye kontrol ederek sonrasında direkt return value yapıyor.
    return index[keyword]
  else:
    return None


#Q1 - a
def crawlWeb(seed):
  tocrawl = [seed]
  crawled = []
  index = {}
  graph = {}
  while tocrawl:
    page = tocrawl.pop()
    if page not in crawled:
      content = getClearPage(getPage(page))
      addPageToIndex(index, page, content)
      graphLinks = get_all_links(getPage(page)) #html tagindeki linkler kaybolmasın diye böyle
      graph[page] = graphLinks
      union(tocrawl, get_all_links(getPage(page)))
      crawled.append(page)
  return index, graph
#graph represents the outlinks of that page.



def computeRanks(graph):
  d = 0.8
  N = len(graph)
  numloops = 10

  ranks = {}
  #herkese eşit dağılım
  for page in graph:
    ranks[page] = 1 / N
  for i in range(0, numloops):
    newranks = {}
    for page in graph:
      newrank = (1-d) / N

      for node in graph:
        if page in graph[node]: #buna link veriyorsa
          newrank = newrank + d * (ranks[node] / len(graph[node])) #eşit dağılım sağlamak için
      newranks[page] = newrank
    ranks = newranks
  return ranks



def rankedLookup(index, key, graph):
  rawRes = lookup(index, key) #normal arama sonuçları
  rankings = computeRanks(graph) #ranklerin hesaplanması
  list1 = [] #arama sonuçlarının rankleri için, sonrasında ise sıralamak için
  list2 = [] #normal arama sonuçları ve rankleri birleştirmek için
  for i in rawRes:
    list1.append(rankings[i]) #sıralamaları ekliyor
    list2.append([i, rankings[i]]) #sıralamalar ve normal sonuçları eşleştiriyor

  list1 = sorted(list1, reverse=True) #sıralama
  list3 = [] #en son sonuç olarak sıralanmış biçimde normal sonuçları vermek için
  for i in list1:
    for y in list2:
      if i == y[1]:
        list3.append(y[0]) #list 1 ve 2 eşleştirmesi yapıyor uyanları list 3 e ekliyor sonrasında ise return list 3 ile output olarak veriyor.
  return list3



def getSite(address,debug=False,cookie=None,MovedCount=0):
    try:
        import httplib
        from urlparse import urlparse
    except:
        import http.client as httplib
        from urllib.parse import urlparse
    

    MaxRedirectURL = 5
    
    site = urlparse(address)
    if debug:
        print("Protocol:",site.scheme)
        print("Host:",site.hostname)
        print("Path:",site.path)
        print("Query:",site.query)

    if site.scheme == "https":
        conn = httplib.HTTPSConnection(site.hostname)
    elif site.scheme == "http":
        conn = httplib.HTTPConnection(site.hostname)

    #conn.set_debuglevel(1)
        
    conn.request("GET", site.path+"?"+site.query)
    r1 = conn.getresponse()
    if debug:
        print(r1.status, r1.reason)
        if r1.getheader("location"): print("\tlocation:", r1.getheader("location"))
        
    data = r1.read()
    r1.close()
    #redirect, only MaxRedirectURL
    if (r1.status == 301 or r1.status == 302) and MovedCount < MaxRedirectURL:
        return getSite(r1.getheader("location"),debug=debug,cookie=cookie,MovedCount=MovedCount+1)
    elif r1.status != 200:
        open("error.html","w").write(address+data)
        return ""
    if debug:
        open("tmp.html","w").write(data)
    return data


def find_true_url(dane):
    #didn't finish
    for ep, site in dane:
        print(ep)
        html = getSite(site)

        public = re.findall('"(http[^"]+).*?class="btn"',html)
        print(public)

        html = getSite(public[0])

        movie = re.findall('var url = "([^"]+)',html)
        print(movie)

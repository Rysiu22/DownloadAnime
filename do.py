import re, sys
from tools import getSite
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
    raw_input = input


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        urls = open(filename).readlines()
        for url in urls:
            if url.strip() and url.strip()[0] != '#':
                create_file(url.strip())
    else:
        create_file()
    

def create_file(site=None):
    """Create script for Windows"""
    if not site:
        site = raw_input("Put site url:")
    html = getSite(site)

    patern = """(Episode \d+|Movie \d+) : .+?(http[^"]+).+?Direct Download""".replace(" ","\s*")
    #print patern

    dane = re.findall(patern,html)
    print("Find:",len(dane))
    #print dane

    if not len(dane):
        return
    
    urls = []
    for ep, address in dane:
        urls.append(address.replace("//","//public.animeout.xyz/"))


    #valid filename
    s = "".join(x for x in urlparse(site).path if x.isalnum() or x in "._- ")
    s = s.replace("-"," ")

    #create script
    header = ['set use_wget=/wget/wget',
              # curl -g -C - -O "http://"
              'if not exist "'+s+'" mkdir "'+s+'"',
              'cd "'+s+'"'
              ]
    body = ['%use_wget% "'+url+'" -c' for url in urls]
    end = ['cd ..']
    out = '\n'.join( header + body + end )
    
    filename = s+".bat"
    open(filename,"w").write(out)
    print("Created:",filename)

    print("Done")


if __name__ == "__main__":
    main()

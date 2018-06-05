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

def find_true_url(site):
    """Stupid steps to check once real url, can easly crash"""
    debug = False
    # step 1
    if debug:
        print "find_true_url",[site],"\n"
    html = getSite(site)

    if debug:
        open("step1.html","w").write(html)
    
    patern = """(http[^"]+).*class="btn""".replace(" ","\s*")
    dane = re.findall(patern,html)

    if debug:
        print "step 1", len(dane),"\n"

    # step 2
    site = dane[0]
    html = getSite(site)

    if debug:
        open("step2.html","w").write(html)
    
    patern = """var url = "(http[^"]+)""".replace(" ","\s*")
    dane = re.findall(patern,html)

    if debug:
        print "step 2", len(dane),"\n"

    # end
    return dane[0]

def compare_url_schema(site1,site2):
    """Simple check urls is the same"""
    if site1.replace(" ","").replace("?","") == site2.replace(" ","").replace("?",""):
        return True
    else:
        return False

def create_file(site=None):
    """Create script for Windows"""
    if not site:
        site = raw_input("Put site url:")

    # get first site
    html = getSite(site)

    # extract movie links
    patern = """(Episode \d+|Movie \d+) : .+?(http[^"]+).+?Direct Download""".replace(" ","\s*")

    dane = re.findall(patern,html)
    print("Find:",len(dane))
    print dane[:1]

    # if empty then finish
    if not len(dane):
        return

    first_move_url = dane[0][1]

    # go to steps checking real url,
    # (add check first and last. add auto generate diff)
    real_url = find_true_url(first_move_url)
    if not real_url:
        return

    # create urls
    urls = []
    for ep, address in dane:
        # hard
        if not compare_url_schema(first_move_url.replace("//","//public.animeout.xyz/"), real_url):
            address_out = find_true_url(address)
        # easy
        else:
            address_out = address.replace("//","//public.animeout.xyz/")
        urls.append(address_out)
        print address_out


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

import urllib 
import sys

def get_links(url):
    """" Open the URL and extract all the links, storing them in the
         order visited in a *list*.
    """
    try:
        f = urllib.urlopen(url)
    except urllib.URLError, e:
        print "URL %s FAILED!" %url
        return []
    contents = f.read()  # read in the entire html file into a single string
    f.close()

    links = []     # we store the links in a set

    start_loc = 0
    while True:
        #  Get the next start/end tuple, a negative start means we are done.
        (start_loc,end_loc) = next_url(contents, start_loc)
        if start_loc < 0:
            return links

        #  Extract the new URL
        link = contents[start_loc:end_loc]

        #  Should we skip it?
        if skip_link(link):
            start_loc = end_loc
            continue

        #  When the link does not start with http: it is a relative
        #  link so we should prepend the current URL.
        if not link.startswith("http:"):
            if url[-1] == '/':
                link = url + link
            else:
                link = url + '/' + link
        end_loc = start_loc

        #  Add the link
        links.append(link)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "URL must be provided on the command line"
        sys.exit(0)
    
    links = get_links(sys.argv[1])

    print "Links from", sys.argv[1]
    for lnk in links:
        print '    ' + lnk


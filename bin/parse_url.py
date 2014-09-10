import urllib 
import sys

def next_url( fstring, start_loc ):
    """ Get the next url from the fstring starting at the start_loc
        index.  Return a tuple giving the index of the first character
        in the URL in fstring, followed by one-past the last character.
    """
    end_pair = (-1,0)   # What to return if no valid URL is found.

    # Find the <a
    a_loc = fstring.find('<a', start_loc)
    if a_loc == -1:  return end_pair

    # Find the href
    href_loc = fstring.find( 'href', start_loc+1 )
    if href_loc == -1:  return end_pair

    # We have an href, so let's find the "
    url_loc = fstring.find( '"', href_loc+1 )
    if url_loc == -1: return end_pair

    # Find the matching end "
    end_url_loc = fstring.find( '"', url_loc+1)
    if end_url_loc == -1: return end_pair

    # Now we've got it!
    return (url_loc+1, end_url_loc )

# ------------------------------------------------------------------------

def skip_link(link):
    """ A quick test to determine which links to eliminate based on
        being a relative link or using the wrong protocol.
    """
    return \
        '#' in link or '..' in link or '.pdf' in link or '.ps' in link or \
        '.png' in link or '.gif' in link or 'java' in link or \
        link.startswith("ftp:") or link.startswith("file:") or \
        link.startswith("gopher:") or link.startswith("https:") or \
        link.startswith("ws:") or link.startswith("wss:") or \
        'mailto' in link

# ------------------------------------------------------------------------


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


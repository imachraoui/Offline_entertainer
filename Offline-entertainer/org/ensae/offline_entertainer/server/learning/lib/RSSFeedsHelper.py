from bs4 import BeautifulSoup as parser
import urllib3
import feedparser

def detect_feeds_in_HTML(input_stream):
    """ examines an open text stream with HTML for referenced feeds.

    This is achieved by detecting all ``link`` tags that reference a feed in HTML.

    :param input_stream: an arbitrary opened input stream that has a :func:`read` method.
    :type input_stream: an input stream (e.g. open file or URL)
    :return: a list of tuples ``(url, feed_type)``
    :rtype: ``list(tuple(str, str))``
    """
    # check if really an input stream
    if not hasattr(input_stream, "read"):
        raise TypeError("An opened input *stream* should be given, was %s instead!" % type(input_stream))
    result = []
    # get the textual data (the HTML) from the input stream
    html = parser(input_stream.read(),"lxml")
    # find all links that have an "alternate" attribute
    feed_urls = html.findAll("link", rel="alternate")
    # extract URL and type
    for feed_link in feed_urls:
        url = feed_link.get("href", None)
        typeApplication = feed_link.get("type", None)
        # if a valid URL is there
        if url:
            if (typeApplication == 'application/rss+xml'):
                result.append(url)
    return result

def get_rss_feeds(domain,weight):
    http= urllib3.PoolManager()
    f = http.urlopen('GET',domain, preload_content=False)
    rsslinks=detect_feeds_in_HTML(f)
    rsslink = rsslinks[0]
    feed = feedparser.parse(rsslink)
    results = []
    for i in range(0,weight+1):
        entry={}
        post = feed.entries[i]
        entry["title"]= post.title
        entry["summary"]= post.summary
        results.append(entry)
    return(results)

print(get_rss_feeds('http://techcrunch.com',2))
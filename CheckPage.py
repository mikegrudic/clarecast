import urllib, urllib2, re
from numpy import prod
import string
from time import sleep

def CheckPage(last_post=None):
    req = urllib2.Request("https://www.facebook.com/centralcasting")
    response = urllib2.urlopen(req)
    page = response.read()
    
    posts = re.split('<p>|</p>', page.replace('<br />',''))[1::2]
    posts = re.split('Central Casting Los Angeles', page.replace('<br />',''))
    pposts = []
    for p in posts[9:]:
        pposts.append(string.join(re.split('<p>|</p>',p)[1::2]))

    for p in pposts:
        if p == last_post:
            return None
        pl = p.lower()
        nonunion = "non union" in pl
        sex = "female" in pl or "women" in pl
        ethnicity = "ethnicity" in pl or "caucasian" in pl

        if nonunion and sex and ethnicity:
            return p

    return None

def main():
    post = None
    while True:
        print "Checking page...\n"
        newpost = CheckPage(post)
        if newpost != post and newpost != None:
            print newpost + "\n"
            post= newpost
        else:
            print "No new posts.\n"
        sleep(1)
        

if __name__ == "__main__":
    main()
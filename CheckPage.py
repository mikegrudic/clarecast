import urllib, urllib2, re
import string
from time import sleep
import easygui

def GetPostsAndTimes():
    req = urllib2.Request("https://www.facebook.com/centralcasting")
    response = urllib2.urlopen(req)
    page = response.read()
    
    posts = re.split('Central Casting Los Angeles', page.replace('<br />',''))

    pposts = []
    times = []
    for p in posts[9:]:
        if 'data-utime="' in p:
            times.append(int(p.split('data-utime="')[1].split('"')[0]))
            pposts.append(string.join(re.split('<p>|</p>',p)[1::2]))

    pposts = [x for (y,x) in sorted(zip(times,pposts))]
    return pposts[::-1], sorted(times)[::-1]

def ShowOldPosts():
    posts, times = GetPostsAndTimes()
    for p in posts:
        pl = p.lower()
        nonunion = "non union" in pl
        sex = "female" in pl or "women" in pl
        ethnicity = "ethnicity" in pl or "caucasian" in pl
        if nonunion and sex and ethnicity:
            easygui.msgbox(p, title="Casting call!")
        
    
def CheckPage(last_post=None):
    pposts, times = GetPostsAndTimes()
    
    most_recent = pposts[0]

    if most_recent == last_post:
        return None
    else:
        pl = most_recent.lower()
        nonunion = "non union" in pl
        sex = "female" in pl or "women" in pl
        ethnicity = "ethnicity" in pl or "caucasian" in pl
        if True:#        if nonunion and sex and ethnicity:
            return most_recent

    return None
    
def main():
    ShowOldPosts()
    post = None
    while True:
        newpost = CheckPage(post)
        if newpost != post and newpost != None:
            easygui.msgbox(newpost, title="Casting call!")
            with open("calls.txt", "a") as f:
                f.write(newpost)
                f.write("\n")
            post = newpost
        sleep(1)
        

if __name__ == "__main__":
    main()
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

def IsRelevant(post):
    if unionness:
        union_check = True
    else:
        union_check = "non union" in post.replace("-", " ")
    sex_check = sum([w in post for w in sex_words])
    eth_check = sum([w in post for w in eth_words])
    return union_check and sex_check and eth_check
    
def ShowOldPosts():
    posts, times = GetPostsAndTimes()
    for p in posts:
        pl = p.lower()
        if IsRelevant(pl):
            easygui.msgbox(p, title="Casting call!")
        
    
def CheckPage(last_post=None):
    pposts, times = GetPostsAndTimes()
    
    most_recent = pposts[0]

    if most_recent == last_post:
        return None
    else:
        pl = most_recent.lower()
        if IsRelevant(pl):
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
    sex = easygui.buttonbox("Sex:", "Sex",["M","F","Yes"])
    if sex == "Yes":
        easygui.msgbox("ayy lmao")
        sex = easygui.buttonbox("Sex:",None,["M","F"])
    if sex == "M":
        sex_words = 'male',' men'
    else:
        sex_words = 'female', 'women'
        
    unionness = easygui.buttonbox("Union or non-union?","Unionness",["Union","Non-union"]) == "union"
    
    eth_words = easygui.multenterbox("Please enter any terms applying to your ethnicity which you want to check for","Ethnicity",["","","","",""])
    eth_words = [e.lower() for e in eth_words if len(e)>0]
    eth_words.append("ethnicity")

    main()
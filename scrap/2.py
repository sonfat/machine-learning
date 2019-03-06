import requests, re
# url = "http://thzvv.net/forum-181-1.html"
part1 = "http://thzvv.net/forum-181-"
part2 = ".html"
path = "http://thzvv.net/"

re_name = r'class="s xst">(.*?)</a>'
re_link = r'</em> <a href="(.*?)" style='
# onclick="atarget(this)" class="s xst">(.*?)</a>



for page in range(1,3):
    url = part1 + str(page) + part2
    res =requests.get(url)
    # print res.text
    infos = re.findall(re_name, res.text)
    links = re.findall(re_link, res.text)

print links




# print res.text
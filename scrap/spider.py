#!/usr/bin/env python3

import requests,re
domain = 'http://thzvv.net/imc_attachad-ad.html?aid='
def get_tor_url(web_url):
    re_tor_url = r'imc_attachad-ad.html\?aid=(.*?)" onmouseover='
    re_tor_names = r'hidden">.*\](.*?)</DIV></TD></TR>' 
    re_tor_title_names = r'<span id="thread_subject">\d{4}-\d{1,2}-\d{1,2} (.*?)</span>' 
    reurl = r'<a href="thread-1(.*?)" class="xi2">'
    try:
        web_html = requests.get(web_url).text
        for web in re.findall(reurl,web_html):
            web = 'http://thzvv.net/thread-1'+ web
            html_doc = requests.get(web).text
            for urls in re.findall(re_tor_url,html_doc):
                tor_url = domain+urls
                down_tor_url = 'http://thzvv.net/forum.php?mod=attachment&aid='+ urls
                if len(re.findall(re_tor_names,requests.get(tor_url).text)) > 0:
                    print(tor_url)
                    re_tor_name = re.findall(re_tor_names,requests.get(tor_url).text)[0] 
                    re_tor_title_name = re.findall(re_tor_title_names,requests.get(web).text)[0]+'.torrent'
                    print(re_tor_name)
                    if '1080' not in re_tor_name and 'hd' not in re_tor_name :
                        print('Downloading'+ re_tor_name)
                        with open('F:/vedio/'+re_tor_title_name,'wb') as f1:
                            f1.write(requests.get(down_tor_url).content)
    except Exception as err:
        pass
def main():
    for i in range(1,370):
        web_url = 'http://thzvv.net/forum-69-' + str(i) + '.html'
        get_tor_url(web_url)

if __name__ == '__main__':
    main()
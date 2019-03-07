# -*- coding:utf-8 -*-
# author: sonfat
# date: 2019/03/07

import requests, re
import os

# 可以修改的参数：
begin = 1 #首页
over = 3 #尾页
local_path = "F:/video/xi/" #下载路径


part1 = "http://thzvv.net/forum-69-"
part2 = ".html"
path = "http://thzvv.net/"

re_name = r'class="s xst">(.*?)</a>'
re_torrent = r'href="imc_attachad-ad.html\?aid=(.*?)" onmouseover="showMenu'
re_link2 = r'</a>]</em> <a href="(.*?)"'

# 创建文件夹
def create_catalog(local_path):
    path = local_path.rstrip("/")
    try:
        isExists = os.path.exists(path)
        if not isExists:
            print "目录不存在，创建目录......"
            os.makedirs(path)
            print "创建成功，目录位置: " + path + '/'
        else:
            print "目录已存在。"
            print "目录位置: " + path + '/'
    except Exception,e:
        pass

# 一轮处理一页
def grap_infos_and_tor_url(page_no):
    try:
        links = []
        url = part1 + str(page_no) + part2
        res = requests.get(url)
        # print res.text
        infos = re.findall(re_name, res.text)
        pages = re.findall(re_link2, res.text)
        for page in pages:
            links.append(path + page)
        if page_no == 1:
            infos = infos[1:]
        return links, infos
    except Exception,e:
        pass

def download(links, infos):
    for i in range(0, len(links)):
        try:
            res = requests.get(links[i])
            torrent_params = re.findall(re_torrent, res.text)
            tmp = "http://thzvv.net/forum.php?mod=attachment&aid="
            download_link = tmp + torrent_params[0]

            with open(local_path + infos[i].replace(' ', '_') + ".torrent", "wb") as f:
                f.write(requests.get(download_link).content)
                print "[+]- " + links[i] + torrent_params[0] + "  ====>  Download Success"
        except Exception ,e:
            pass


if __name__ == "__main__":

    links, infos = grap_infos_and_tor_url(5)
    print links[2]
    print infso[2]
    # create_catalog(local_path)
    # print "......开始下载......"
    # for page_no in range(begin, over):
    #     links, infos = grap_infos_and_tor_url(page_no=page_no)
    #     download(links, infos)
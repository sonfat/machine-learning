import requests
url  = "http://thzvv.net/forum.php?mod=attachment&aid=MzIyNTkwfGFjNDhjNTlhfDE1NTE5MjcxNjF8MHw3NDMxNTM="
res = requests.get(url).content
with open("F:/test.torrent","wb") as f:
    f.write(res)
print res


# <a href="imc_attachad-ad.html?aid=NDMyNDc3fGM5YjZiYjg2fDE1NTE4NTQ4MDh8MHwxOTQ2MzM2" onmouseover="showMenu({'ctrlid':this.id,'pos':'12'})" id="aid432477" target="_blank" onclick="showWindow('imc_attachad', this.href)" initialized="true">[ThZu.Cc]021419_01-10mu-1080p.torrent</a>
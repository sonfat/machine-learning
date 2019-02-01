import os

path  = 'E:\\application\cmder'
aa = os.walk(path)
for a,b,c in aa:
    print a,b,c
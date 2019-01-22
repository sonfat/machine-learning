# import os
#
# def load_one_flle(filename):
#     # x=[]
#     with open(filename) as f:
#         line=f.readline()
#         line=line.strip('\n')
#     return line
#
# def load_adfa_training_files(rootdir):
#     x=[]
#     y=[]
#     list = os.listdir(rootdir)
#     for i in range(0, len(list)):
#         path = os.path.join(rootdir, list[i])
#         if os.path.isfile(path):
#             x.append(load_one_flle(path))
#             y.append(0)
#     return x,y
#
# def dirlist(path, allfile):
#     filelist = os.listdir(path)
#
#     for filename in filelist:
#         filepath = os.path.join(path, filename)
#         if os.path.isdir(filepath):
#             dirlist(filepath, allfile)
#         else:
#             allfile.append(filepath)
#     return allfile
#
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(min_df=1)
x1 = ['grumman','grumman','lk','grumman','lk','grumman']
x2 = [0, 0, 1, 0, 1, 0]
# x2 = ['0', '0', '1', '0', '1', '0']
x = x1+x2
x = cv.fit_transform(x)
x = x.toarray()
for item in x:
    print item
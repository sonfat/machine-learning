from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(ngram_range=(1,2))

with open("chapter.txt", 'r') as f:
    raw = f.readlines()
    length = len(f.readlines())

y1 = ["0"] * (length/2)
y2 = ["1"] * (length - length/2)
y = np.concatenate((y1,y2))
y_pre = cv.fit_transform(raw).toarray()
print y_pre
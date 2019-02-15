import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def show_k_means():
    print(__doc__)

    plt.figure(figsize=(12,12))

    n_samples = 15000
    seed = 170
    x, y = make_blobs(n_samples=n_samples, random_state=seed)
    y_predicted = KMeans(n_clusters=3, random_state=seed).fit_predict(x)
    print y_predicted

    plt.subplot(221)
    plt.scatter(x[:, 0], x[:, 1], c=y_predicted)
    plt.title("hello word!")

    plt.show()
    # plt.show()


if __name__ == "__main__":
    show_k_means()
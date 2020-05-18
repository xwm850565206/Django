import matplotlib.pyplot as plt
import time

import numpy as np

from api.local.datahelper.Dataloader import DataLoader
from api.local.datahelper.Utils import get_target_segment_data
from api.local.fuzzy.FCMPoint import FCMPoint
from api.local.fuzzy.Math import sub
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置


class FCM:

    def __init__(self):
        self.c_clusters = 3
        self.m = 2
        self.eps = 10
        self.epoch = 50

    def strip(self, result):

        points = [[] for _ in range(self.c_clusters)]
        for i, res in enumerate(result):
            points[res].append([i, i])

        return points

    def run(self, X, segments):

        loss = []
        # Centroids = np.random.random(self.c_clusters)

        membership_mat = np.random.random((len(X), self.c_clusters))
        membership_mat = np.divide(membership_mat, np.sum(membership_mat, axis=1)[:, np.newaxis])
        epoch = 0
        while True:

            working_membership_mat = membership_mat ** self.m
            Centroids = np.divide(np.dot(working_membership_mat.T, X),
                                  np.sum(working_membership_mat.T, axis=1)[:, np.newaxis])

            n_c_distance_mat = np.zeros((len(X), self.c_clusters))
            for i, x in enumerate(X):
                for j, c in enumerate(Centroids):
                    n_c_distance_mat[i][j] = np.linalg.norm(sub(x, c, segments), 2)

            new_membership_mat = np.zeros((len(X), self.c_clusters))

            for i, x in enumerate(X):
                for j, c in enumerate(Centroids):
                    new_membership_mat[i][j] = 1. / np.sum(
                        (n_c_distance_mat[i][j] / n_c_distance_mat[i]) ** (2 / (self.m - 1)))

            tmp = np.sum(abs(sub(new_membership_mat, membership_mat, segments)))
            loss.append(tmp)
            print(tmp)

            if tmp < self.eps:
                break

            epoch += 1
            if epoch >= self.epoch:
                break


            membership_mat = new_membership_mat

        plt.plot(loss)
        plt.xlabel("训练轮次")
        plt.ylabel("损失")
        plt.title("clusters: " + str(self.c_clusters) + " m: " + str(self.m))
        plt.show()

        return Centroids, np.argmax(membership_mat, axis=1), loss[len(loss) - 1]

    def save(self, filename, Centroids, loss, segment, time):

        fcm_point = FCMPoint(self.c_clusters, Centroids, segment)

        with open(filename, 'w') as file:
            file.write(fcm_point.toFileFormat() + '\n')
            file.write("loss:" + str(loss) + '\n')
            file.write("time:" + str(time) + '\n')


if __name__ == '__main__':

    trainset = 'target_comsize'
    # trainset = 'target_credit'
    # trainset = 'target_technique'
    # trainset = 'target_construction'
    # trainset = 'target_strength'
    # trainset = 'target_stable'
    dataloader = DataLoader(is_init_dic=True, prefix='../datahelper/')
    data, segment = get_target_segment_data(dataloader, trainset)

    for key in dataloader.data_filter.mu:
        print(key)
    for key in dataloader.data_filter.sigma:
        print(key)

    fcm = FCM()
    begin_time = time.time()
    center_points, fcm_points, loss = fcm.run(data, segment)
    end_time = time.time()

    print("用时:" + str(end_time-begin_time))

    fcm.save(filename=trainset + '-cluster=' + str(fcm.c_clusters) + '-m=' + str(fcm.m) + '.txt',
             Centroids=dataloader.data_filter.recover_datas(center_points, segment), loss=loss, segment=segment, time=end_time-begin_time)

    # print(fcm_points)

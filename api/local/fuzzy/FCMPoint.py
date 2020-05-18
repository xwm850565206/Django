import json


class FCMPoint:

    def __init__(self, cluster, vectors, segments, vector_to_label=None):

        if vector_to_label is None:
            vector_to_label = dict()

        self.cluster = cluster  # int值
        self.segments = segments  # 形状为(1, n) 的list
        self.vectors = vectors  # 形状为(cluster, len(segments))的list，每一列对应segment对应序号的值

        self.vector_to_label = vector_to_label  # 形状为{key:value}, 其中key是vectors的下标，value是对应代表的标签，不一定有，这个要在文件里写，属于手动定义的范畴

    def toFileFormat(self):
        data_dic = {'cluster': self.cluster, 'vectors': self.vectors.tolist(), 'segments': self.segments}
        # print(data_dic)
        return json.dumps(data_dic, indent=4, ensure_ascii=False)

    def toString(self):
        return str(self.cluster) + '\n' + str(self.segments) + '\n' + str(self.vectors) + '\n' + str(self.vector_to_label) + '\n'

    @staticmethod
    def toFCMPoint(file_string):
        """
        从文件中读取他的信息
        :param self:
        :param file_string: 文件内容
        :return:
        """
        data_dic = json.loads(file_string, encoding='utf-8')
        return FCMPoint(data_dic['cluster'], data_dic['vectors'], data_dic['segments'], data_dic['vector_to_label'])

    @staticmethod
    def distance(self, veca, vecb):
        """
        binary 类型的字段还没考虑
        :param self:
        :param veca:
        :param vecb:
        :return:
        """
        assert len(veca) == len(vecb)

        dis = 0
        for i in range(len(veca)):
            dis += (veca[i] - vecb[i]) ** 2
        return dis

    def getLabel(self, data):
        """
        得到对应的标签
        :param data:形状是[{key, data}, {key, dadta}, ...]
        :return: 标签
        """

        label_index = -1
        min_dis = 0x3f3f3f3f
        for key in data:
            index = self.segments.index(key)
            dis = self.distance(data[key], self.vectors[index])
            if dis < min_dis:
                min_dis = dis
                label_index = index

        assert label_index != -1

        return self.vector_to_label[label_index]

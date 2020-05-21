from api.local.datahelper import Utils
import numpy as np


class DataFilter:

    def __init__(self, is_init_dic, prefix=''):
        self.weight_dic = self._generate_weight()
        self.prefix = prefix

        self.max = dict()
        self.min = dict()
        self.mu = dict()
        self.sigma = dict()

        if is_init_dic:
            self.init_dic = self.load_init_dic()
        else:
            self.init_dic = None

    def normalization(self, data, segment, minn=None, maxn=None):
        _minn = minn
        _maxn = maxn

        if _minn is None:
            _minn = np.min(data)
        if _maxn is None:
            _maxn = np.max(data)

        _range = _maxn - _minn

        self.max[segment] = _maxn
        self.min[segment] = _minn

        if _range == 0:
            return np.ones(data.shape)
        else:
            return (data - _minn) / _range

    def standardization(self, data, segment, mu=None, sigma=None):
        _mu = mu
        _sigma = sigma

        if _mu is None:
            _mu = np.mean(data, axis=0)
        if _sigma is None:
            _sigma = np.std(data, axis=0)

        self.mu[segment] = _mu
        self.sigma[segment] = _sigma

        if _sigma == 0:
            return np.ones(data.shape)
        else:
            return (data - _mu) / _sigma

    def get_weight(self, segment):

        if segment in self.weight_dic:
            return self.weight_dic[segment]
        if str(segment).startswith('inv'):
            return self.weight_dic['inv']
        if str(segment).startswith('xzbz'):
            return self.weight_dic['xzbz']

        return 1.0

    def filter(self, data, segment_list, use_func='standard'):
        """
        在个性化装载完后调用，负责数据的包装
        :param data: 形状为(n, m)的数组
        :param segment_list: 每一列对应的字段名
        :param use_func:两个选项 standard或者minmaxscale，分别是对数据进行归一化或者标准化。
        :return: 过滤，加权以及归一化后的数据
        """
        setattr(self, 'use_func', use_func)
        tmp = []
        for i, segment in enumerate(segment_list):
            raw_data = data[:, i]
            raw_data = np.array(raw_data)
            if use_func == 'standard':
                raw_data = self.standardization(raw_data, segment)
            elif use_func == 'minmaxscale':
                raw_data = self.normalization(raw_data, segment)
            else:
                raise ValueError("UnSupport function: " + use_func)

            raw_data = raw_data * self.get_weight(segment)
            tmp.append(raw_data)

        tmp = np.array(tmp)
        tmp = tmp.T
        return tmp

    def filter_simple_data(self, data, segment_list, use_func='standard'):
        tmp = []
        for i, segment in enumerate(segment_list):
            raw_data = data[:, i]
            raw_data = np.array(raw_data)
            if use_func == 'standard':
                raw_data = self.standardization(raw_data, segment, self.mu[segment], self.sigma[segment])
            elif use_func == 'minmaxscale':
                raw_data = self.normalization(raw_data, segment, self.min[segment], self.max[segment])
            else:
                raise ValueError("UnSupport function: " + use_func)

            raw_data = raw_data * self.get_weight(segment)
            tmp.append(raw_data)

        tmp = np.array(tmp)
        tmp = tmp.T
        return tmp

    def recover_data(self, data, segment):

        if self.use_func == 'standard':
            data = data * self.sigma[segment] + self.mu[segment]
        elif self.use_func == 'minmaxscale':
            _range = self.max[segment] - self.min[segment]
            data = (data * _range) + self.min[segment]

        data = data / self.get_weight(segment)
        return data

    def recover_datas(self, data, segments):
        for i, segment in enumerate(segments):
            data[:, i] = self.recover_data(data[:, i], segment)
        return data

    def load_init_dic(self):
        init_dic = {}
        filename = self.prefix + 'init_dic.txt'
        with open(filename, 'r', encoding='UTF-8') as file:
            cur_key = ''
            while True:
                line = file.readline()
                line = line.replace('\n', '')
                if line is None or line == '':
                    break
                if Utils.is_Chinese(line):
                    tmp = line.split(' ')
                    tmp = set([x for x in tmp if x != ''])
                    sorted(tmp)  # 为了让顺序统一，提前排序
                    init_dic[cur_key] = tmp
                else:
                    cur_key = line

        return init_dic

    @staticmethod
    def _generate_weight():
        weight_dic = {}
        weight_dic.update(Utils.target_credit_weight)
        weight_dic.update(Utils.target_technique_weight)
        weight_dic.update(Utils.target_construction_weight)
        weight_dic.update(Utils.target_comsize_weight)
        weight_dic.update(Utils.target_strength_weight)
        weight_dic.update(Utils.target_stable_weight)
        return weight_dic

    datafilter = None

    @staticmethod
    def createInstance(is_init_dic, prefix):
        DataFilter.datafilter = DataFilter(is_init_dic=is_init_dic, prefix=prefix)
        return DataFilter.datafilter

    @staticmethod
    def getInstance():
        return DataFilter.datafilter


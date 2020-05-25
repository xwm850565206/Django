from api.local.datahelper import Utils
from api.local.datahelper.Dataloader import DataLoader
import api.network.utils.StaticTable as st
import json
import numpy as np


class DataMapHelper:
    data_map_helper = None

    def __init__(self):
        self.belongs = st.belong_list
        self.belong_dic = st.belong_dic

        try:
            self.data_loader = DataLoader.getInstance()
        except ValueError:
            self.data_loader = DataLoader.createInstance(is_init_dic=True, prefix=st.raw_data_path,
                                                         filter_func='minmaxscale')

        self.not_origin_segment_info = self.__generate_not_origin_segment_info()

    @staticmethod
    def getInstance():
        if DataMapHelper.data_map_helper is None:
            DataMapHelper.data_map_helper = DataMapHelper()
        return DataMapHelper.data_map_helper

    def getBelongFromIndex(self, index):
        return self.belongs[index]

    def getBelongIndex(self, segment_name):

        for i, key in enumerate(self.belong_dic):
            try:
                _ = self.belong_dic[key].index(segment_name)
                return i
            except ValueError:
                continue
        raise ValueError("cannot find " + segment_name + " belong")

    def getAllSegmentName(self):
        res = []
        for key in self.belong_dic:
            res.extend(list(self.belong_dic[key]))
        return res

    def getSegmentExplain(self, segment):

        for non_origin_segment in st.not_origin_segments:
            if non_origin_segment.endswith('*'):
                prefix = non_origin_segment.replace('*', '')
                if segment.startswith(prefix):
                    return self.not_origin_segment_info[prefix][int(segment.replace(prefix, ''))]
            elif segment == non_origin_segment:
                return self.not_origin_segment_info[segment]

        if segment in self.data_loader.data_info.data_info:
            return self.data_loader.data_info.data_info[segment]
        return "没有找到对应描述"

    def get_segment_input_content(self, segment_name):
        if segment_name in self.data_loader.data_filter.init_dic:
            return self.data_loader.data_filter.init_dic[segment_name]

    def rescaled_data(self, data_dic, usefunc):

        # if usefunc == 'standard':
        #     for key in data_dic:
        #         sigma = self.data_loader.data_filter.sigma[key]
        #         mu = self.data_loader.data_filter.mu[key]
        #         # data_dic[key] = np.squeeze((np.array(data_dic[key] - mu)) / sigma) if sigma != 0 else np.squeeze(np.ones(len(data_dic[key])))
        #         data_dic[key] = (data_dic[key] - mu) / sigma if sigma != 0 else np.squeeze(
        #             np.ones(len(data_dic[key])))
        #     return data_dic
        # else:
        #     raise ValueError(usefunc + 'is not support now')
        for key in data_dic:
            if data_dic[key] is None:
                data_dic[key] = self.solve_unaccept_value(key, data_dic[key])
            data_dic[key] = np.squeeze(self
                                       .data_loader
                                       .data_filter
                                       .filter_simple_data(np.array([data_dic[key]])
                                                           .reshape((1, -1)), [key], usefunc)).tolist()
        return data_dic

    def alreadyInDataBase(self, company_name):
        try:
            self.data_loader.company_list.index(company_name)
        except ValueError:
            return False
        return True

    def loadItData(self, company_name):
        return self.data_loader.get_company_data(company_name)

    def __generate_not_origin_segment_info(self):
        """
        不是原生字段的解释
        :return:
        """
        not_origin_segment_info = {
            'inv': [x + '占比' for x in self.data_loader.data_filter.init_dic['invtype']],
            'xzbz': ['是否参保:' + x for x in self.data_loader.data_filter.init_dic['xzbzmc']],
            'defendant_num': '成为被告次数',
        }

        return not_origin_segment_info

    def solve_unaccept_value(self, segment, value):
        for tableloader in self.data_loader.loader:
            if tableloader.can_solve_the_unaccept_value(segment, value):
                return tableloader.solve_unaccept_value(segment, value)
        return None


if __name__ == '__main__':
    """
    测试
    """
    instance = DataMapHelper.getInstance()
    print(instance.get_segment_input_content('enttype'))
    # print(instance.alreadyInDataBase('f41f792303bd7185258ff937ca369bd8'))
    # print(instance.alreadyInDataBase("1234"))
    # print(instance.getAllSegmentName())
    # print(instance.data_loader.data_info.data_info)

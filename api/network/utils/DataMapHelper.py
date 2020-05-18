from api.local.datahelper import Utils
from api.local.datahelper.Dataloader import DataLoader
import api.network.utils.StaticTable as st
import json


class DataMapHelper:

    def __init__(self):
        self.belongs = st.belong_list
        self.belong_dic = st.belong_dic
        self.data_loader = DataLoader(is_init_dic=True, prefix=st.raw_data_path)
        self.not_origin_segment_info = self.__generate_not_origin_segment_info()

    @staticmethod
    def getInstance():
        return data_map_helper

    def getBelongFromIndex(self, index):
        return self.belongs[index]

    def getBelongIndex(self, segment_name):

        for i, key in enumerate(self.belong_dic):
            try:
                index = self.belong_dic[key].index(segment_name)
                return index
            except ValueError:
                continue
        return -1

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
            'inv': [x+'占比' for x in self.data_loader.data_filter.init_dic['invtype']],
            'xzbz': ['是否参保:'+x for x in self.data_loader.data_filter.init_dic['xzbzmc']],
            'defendant_num': '成为被告次数',
        }

        return not_origin_segment_info


data_map_helper = DataMapHelper()

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

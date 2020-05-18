from api.network.utils.DataMapHelper import DataMapHelper
import api.network.utils.StaticTable as st
from api.local.fuzzy.FCMPoint import FCMPoint


class FCMComputer:

    def __init__(self):
        self.data_map_helper = DataMapHelper.getInstance()
        self.fcm_points = {}
        for belong in self.data_map_helper.belongs:
            self.fcm_points[belong] = self.__load_fcm_point(belong)

    @staticmethod
    def __load_fcm_point(belong):

        with open(st.fcm_point_dir + belong + '.txt', encoding='UTF-8') as file:
            file_string = ""
            for line in file:
                file_string += line
            return FCMPoint.toFCMPoint(file_string)

    def alreadyInDataBase(self, company_name):
        return self.data_map_helper.alreadyInDataBase(company_name)

    def compute(self, data_dic, company_name):

        # 已经在数据库中的公司，从数据库中直接读入就好, 然后把用户输入的数据和数据库中已有的数据合并一下
        if company_name is not None and self.alreadyInDataBase(company_name):
            exist_data_dic = self.data_map_helper.loadItData(company_name)
            exist_data_dic.update(data_dic)
            data_dic = exist_data_dic

        belong_dic = {}
        for key in data_dic:
            index = self.data_map_helper.getBelongIndex(key)
            belong = self.data_map_helper.getBelongFromIndex(index)

            if belong not in belong_dic:
                belong_dic[belong] = []
            belong_dic[belong].append({key, data_dic[key]})

        # 现在的形状是 {belong1: [{key, data}, {key, dadta}], belong2: [{key, data}, {key, data}], ... }

        labels = []
        for belong in belong_dic:
            labels.append(self.fcm_points[belong].getLabel(belong_dic[belong]))
        return labels


if __name__ == '__main__':
    computer = FCMComputer()
    print(computer.fcm_points['target_strength'].toString())

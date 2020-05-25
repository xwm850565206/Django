from api.network.utils.DataMapHelper import DataMapHelper
import api.network.utils.StaticTable as st
from api.local.fuzzy.FCMPoint import FCMPoint
import json


class FCMComputer:

    def __init__(self):
        self.data_map_helper = DataMapHelper.getInstance()
        self.fcm_points = {}

        for belong in self.data_map_helper.belongs:
            self.fcm_points[belong] = self.__load_fcm_point(belong)

        # print(self.fcm_points['target_strength'].toString())
        # print(json.dumps(self.fcm_points['target_strength'], ensure_ascii=False, indent=4))
        self.__fcm_point_rescaled()
        # print(self.fcm_points['target_strength'].toString())
        # print(json.dumps(self.fcm_points['target_strength'], default=lambda o: o.__dict__, ensure_ascii=False, indent=4))

    @staticmethod
    def __load_fcm_point(belong):

        with open(st.fcm_point_dir + belong + '.txt', encoding='UTF-8') as file:
            file_string = ""
            for line in file:
                file_string += line
            return FCMPoint.toFCMPoint(file_string)

    def alreadyInDataBase(self, company_name):
        return self.data_map_helper.alreadyInDataBase(company_name)

    def __rescaled_data(self, data_dic):
        return self.data_map_helper.rescaled_data(data_dic, 'minmaxscale')

    def __fcm_point_rescaled(self):

        for belong in self.fcm_points:
            for cluster in range(self.fcm_points[belong].cluster):
                data_dic = {}
                for i, segment in enumerate(self.fcm_points[belong].segments):
                    data_dic[segment] = self.fcm_points[belong].vectors[cluster][i]
                # print("pre:\n" + json.dumps(data_dic, ensure_ascii=False, indent=4))
                data_dic = self.__rescaled_data(data_dic)
                # print("after:\n" + json.dumps(data_dic, ensure_ascii=False, indent=4))
                for segment in data_dic:
                    for i, _segment in enumerate(self.fcm_points[belong].segments):
                        if segment == _segment:
                            self.fcm_points[belong].vectors[cluster][i] = data_dic[segment]
                            break

    def compute(self, data_dic, company_name):

        # 已经在数据库中的公司，从数据库中直接读入就好, 然后把用户输入的数据和数据库中已有的数据合并一下
        if company_name is not None and self.alreadyInDataBase(company_name):
            exist_data_dic = self.data_map_helper.loadItData(company_name)
            exist_data_dic.update(data_dic)
            data_dic = exist_data_dic

        data_dic = self.__rescaled_data(data_dic)

        belong_dic = {}
        for key in data_dic:
            try:
                index = self.data_map_helper.getBelongIndex(key)
                belong = self.data_map_helper.getBelongFromIndex(index)
                if belong not in belong_dic:
                    belong_dic[belong] = []
                belong_dic[belong].append([key, data_dic[key]])
            except ValueError:
                continue
        # 现在的形状是 {belong1: [[key, data], [key, data]], belong2: [[key, data], [key, data]], ... }

        labels = {}
        for belong in belong_dic:
            labels[belong] = (self.fcm_points[belong].getLabel(belong_dic[belong]))
        return labels


if __name__ == '__main__':
    computer = FCMComputer()
    res = computer.compute({'xzbz1': None}, computer.data_map_helper.data_loader.company_list[0])
    print(json.dumps(res, ensure_ascii=False, indent=4))
import numpy as np
from api.local.datahelper import Datainfo
from api.local.datahelper import Datafilter
from api.local.datahelper import Utils


import csv

from api.local.datahelper.tableloader.changeinfoloader import ChangeInfoLoader
from api.local.datahelper.tableloader.companyinfoloader import CompanyInfoLoader
from api.local.datahelper.tableloader.entcontributeloader import EntContributeLoader
from api.local.datahelper.tableloader.entinsuranceloader import EntInsuranceLoader
from api.local.datahelper.tableloader.jncreditinfoloader import JnCreditInfoLoader
from api.local.datahelper.tableloader.jntechcenterloader import JnTechCenterLoader
from api.local.datahelper.tableloader.justicedeclareloader import JusticeDeclareLoader
from api.local.datahelper.tableloader.qualitycheckloader import QualityCheckLoader
from api.local.datahelper.tableloader.tableloader import TableLoader


class DataLoader:

    data_loader = None  # instance

    def __init__(self, is_init_dic, prefix='', load_set=None, filter_func='standard'):
        self.is_init_dic = is_init_dic

        self.data_info = Datainfo.DataInfo(prefix)
        self.data_filter = Datafilter.DataFilter.createInstance(is_init_dic, prefix=prefix)
        self.loader = [
            TableLoader(),  # 默认的装载器
            CompanyInfoLoader(), ChangeInfoLoader(), EntContributeLoader(),
            EntInsuranceLoader(), JnCreditInfoLoader(), JnTechCenterLoader(),
            JusticeDeclareLoader(), QualityCheckLoader()
        ]

        self.filedir = prefix + self.data_info.filedir + '/Data_FCDS_hashed'
        self.filter_func = filter_func
        self.data = self.load(load_set)  # 形状为 [{'key':tablename, 'company1':name1, 'company2':name2, ...}, ...]

        if not is_init_dic:  # 没有生成字典的话先生成字典，要生成字典得把_load中的个性化装载注释
            self.generate_init_dic()

        self.company_list = self.get_company_list()
        self.segment_list = []
        self.company_data = self.generate_company_data()  # 生成聚类需要的形状
        self.segment_length = len(self.segment_list)
        self.shape = (len(self.company_list), self.segment_length)
        print("总数据形状为:", self.shape)

    def load(self, file_set=None):

        if file_set is None:
            file_set = self.data_info.file_set

        data = []
        for key in file_set:
            data.append(self._load(Utils.file_set_filter(key)))

        return data

    def _load(self, key):
        wb = csv.reader(open(self.filedir + '/' + key + '.csv', 'r', encoding='UTF-8'))
        ws = [x for x in wb]
        result_dic = {}

        print('load: ' + key)

        for index in range(len(ws[0])):
            _data = [x[index] for x in ws]  # 这里导入数据很冗余了，后面还是改改
            _key = _data[0]
            _data = _data[1:]

            result_dic[_key] = _data
            index += 1

        table_loader = self.get_loader_bu_name(key)

        result_dic['key'] = key  # 处理过程可能需要

        result_dic = table_loader.load(result_dic)  # 个性化装载
        result_dic = table_loader.describe(result_dic)  # 展开，修饰

        result_dic['key'] = key  # 防止处理后丢失

        return result_dic

    def generate_company_data(self):
        """
        生成(n, m)形状的数据，其中n是n个公司，m是m种字段，相当于对数据进行最后一次处理，这之后就可以用于计算了
        :return: company_data
        """
        print("begin to reshape and join all data")

        is_init_segment_list = False  # 生成数据的同时把每一列对应的字段也要初始化完毕
        company_data = [[] for i in range(len(self.company_list))]  # 生成(n, ?)形状的list，根据字段总数确定?
        for i, name in enumerate(self.company_list):
            company = []
            for table in self.data:
                table_loader = self.get_loader_bu_name(table['key'])
                segment_name = table_loader.segment_name[table['key']]
                if not is_init_segment_list:
                    self.segment_list.extend(segment_name)
                if name in table:
                    cur_data = table[name]
                    company.extend(cur_data)
                else:
                    tmp = []
                    for segment in segment_name:
                        tmp.append(table_loader.solve_unaccept_value(None, segment))
                    company.extend(tmp)
            company_data[i] = company
            is_init_segment_list = True

        company_data = np.array(company_data)
        company_data = self.data_filter.filter(company_data, self.segment_list, self.filter_func)

        print("finish join data")
        return company_data

    def generate_init_dic(self):
        """
        生成中文信息字典，用于参考和对照
        :return:
        """
        with open('init_dic.txt', 'w', encoding='utf-8') as file:

            for table in self.data:
                for key in table:

                    if Utils.dic_ignore(key):
                        continue

                    flag = False

                    data = table[key]
                    tmp_set = set()
                    for i in data:
                        if not flag and Utils.is_Chinese(i):
                            flag = True
                        tmp_set.add(i)

                    if not flag:
                        continue

                    file.write(key)
                    file.write('\n')
                    for i in tmp_set:
                        file.write(str(i))
                        file.write(' ')
                    file.write('\n')

    def get_table_by_name(self, key):
        """
        按照表名获取表
        :param key:
        :return:
        """
        for table in self.data:
            if table['key'] == key:
                return table
        return None

    def get_loader_bu_name(self, load_name):
        """
        按照装载器名获取装载器
        :param load_name:
        :return:
        """
        for loader in self.loader:
            if loader.load_name == load_name:
                return loader
        return self.loader[0]  # 返回默认装载器

    def get_company_list(self):
        """
        统计出所有的公司
        :return: 所有在表格中出现过的公司名字
        """
        print("begin to generate company list")

        company_set = set()

        for table in self.data:
            for name in table:
                if name == 'key':
                    continue
                company_set.add(name)

        print("finish generate company list")

        return list(company_set)

    def get_company_data(self, company_name):
        """
        得到某个公司对应的所有数据
        :param company_name:
        :return: 一个字典，key是字段名，value是字段数据
        """
        data_dic = {}
        for table in self.data:
            table_loader = self.get_loader_bu_name(table['key'])
            segment_name = table_loader.segment_name[table['key']]
            if company_name in table:
                cur_data = table[company_name]
                for i, data in enumerate(cur_data):
                    data_dic[segment_name[i]] = data
            else:
                tmp = []
                for segment in segment_name:
                    tmp.append(table_loader.solve_unaccept_value(None, segment))
                for i, data in enumerate(tmp):
                    data_dic[segment_name[i]] = data
        return data_dic

    @staticmethod
    def createInstance(is_init_dic, prefix, filter_func):
        DataLoader.data_loader = DataLoader(is_init_dic=is_init_dic, prefix=prefix, filter_func=filter_func)
        return DataLoader.data_loader

    @staticmethod
    def getInstance():
        if DataLoader.data_loader is None:
            raise ValueError("instance not create yet")
        return DataLoader.data_loader


if __name__ == '__main__':

    dataloader = DataLoader(is_init_dic=True)
    # data, sub_segment_name = utils.get_target_segment_data(venv, 'target_credit')
    #
    # print(sub_segment_name)
    # print(data)

    print(dataloader.segment_list)

    # print(venv.data)


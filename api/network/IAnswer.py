class IAnswer:

    def __init__(self):
        pass

    def getAllSegmentName(self):
        """
        得到所有需要的字段
        :return: list 字段集合
        """
        raise NotImplementedError

    def getSegmentExplain(self, name):
        """
        得到这个字段的描述
        :param name:字段名
        :return:字段名对应描述
        """
        raise NotImplementedError

    def getCompanyLabel(self, data_dic, company_name):
        """
        根据传入的数据为公司打上标签
        :param data_dic: 字典，key为字段名，value为字段名对应的数据，value可能是一个list
        :param company_name: 公司名称，用于检索是否是已在数据库的公司，没有输入就为null
        :return: 一个dict，{key, value}, key是层次名, value是标签信息
        """
        raise NotImplementedError

    def getSegmentBelong(self, name):
        """
        得到字段名所属的层次
        :param name: 字段名
        :return: 层次序号，是一个int
        """
        raise NotImplementedError

    def getBelongMap(self, index):
        """
        根据序号得到层次名称
        :param index:
        :return: 层次名称
        """
        raise NotImplementedError

    def get_segment_input_content(self, segment_name):
        """
        得到这个字段所有的输入
        :param segment_name: 字段名称
        :return: 一个set，这个字段的所有输入
        """
        raise NotImplementedError

    def getCompanyLabelFromExecel(self, execel):
        """
        批量操作，传入符合要求的execel，然后回传一个result.txt
        :return:
        """
        raise NotImplementedError

    def solve_unaccept_value(self, segment, value):
        """
        处理异常字段
        :param segment:
        :param value:
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def getInstance():
        """
        使用这个方法来创建此类
        :return: 类的实例
        """
        raise NotImplementedError

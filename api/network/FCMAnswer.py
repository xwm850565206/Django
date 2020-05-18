from api.network.utils.DataMapHelper import DataMapHelper
from api.network.utils.FCMComputer import FCMComputer
from api.network.IAnswer import IAnswer


class FCMAnswer(IAnswer):

    def __init__(self):
        super().__init__()
        self.data_map_helper = DataMapHelper.getInstance()
        self.fcm_computer = FCMComputer()

    def getAllSegmentName(self):
        return self.data_map_helper.getAllSegmentName()

    def getSegmentExplain(self, name):
        return self.data_map_helper.getSegmentExplain(name)

    def getCompanyLabel(self, data_dic, company_name):
        return self.fcm_computer.compute(data_dic, company_name)

    def getSegmentBelong(self, name):
        return self.data_map_helper.getBelongIndex(name)

    def getBelongMap(self, index):
        return self.data_map_helper.getBelongFromIndex(index)

    def get_segment_input_content(self, segment_name):
        return self.data_map_helper.get_segment_input_content(segment_name)


if __name__ == "__main__":
    """
    测试
    """
    pass

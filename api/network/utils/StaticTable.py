from api.local.datahelper import Utils

# fcm路径
fcm_point_dir = 'F:/CodeFiles/Pycharm Projects/Django/api/network/utils/fcm_points/'

# 数据路径
raw_data_path = 'F:/CodeFiles/Pycharm Projects/Django/api/local/datahelper/'

# 层次枚举
belong_list = ["target_credit", "target_technique", "target_construction", "target_comsize", "target_strength",
               "target_stable"]

# 层次以及层次包含的字段名的字典
belong_dic = {
    'target_credit': Utils.target_credit,
    'target_techique': Utils.target_technique,
    'target_construction': Utils.target_construction,
    'target_comsize': Utils.target_comsize,
    'target_strength': Utils.target_strength,
    'target_stable': Utils.target_stable
}

# 不是原生字段的字典，key:不是原生的字段，value:需要输入的字段，也就是需要调用tableloader方法进行load的字段
not_origin_segments = {
    'inv*', 'xzbz*', 'defendant_num',
}



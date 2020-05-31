import json

from api.network.FCMAnswer import FCMAnswer
from api.network.IAnswer import IAnswer


# 在这里拿到名称检索的name
def fullNameSearch(name):
    f = FCMAnswer.getInstance()
    if not f.alreadyInDataBase(name):
        return None

    conditons = {}
    print("======================", f.getCompanyLabel(conditons, name), "==============")
    return f.getCompanyLabel(conditons, name)


def solve_regcapcur(conditions):
    regcapcur_type = conditions.pop('regcapcur_type')
    if regcapcur_type == 'money_dollar':
        conditions['regcapcur'] = int(conditions['regcapcur'] * 7.0215)
    elif regcapcur_type == 'money_euro':
        conditions['regcapcur'] = int(conditions['regcapcur'] * 7.6324)
    else:
        pass

    regcap_type = conditions.pop('regcap_type')
    if regcap_type == 'money_dollar':
        conditions['regcap'] = int(conditions['regcap'] * 7.0215)
    elif regcap_type == 'money_euro':
        conditions['regcap'] = int(conditions['regcap'] * 7.6324)
    else:
        pass

    money_type_taxes = conditions.pop('money_type_taxes')
    if money_type_taxes == 'money_dollar':
        conditions['taxunpaidnum'] = int(conditions['taxunpaidnum'] * 7.0215)
    elif money_type_taxes == 'money_euro':
        conditions['taxunpaidnum'] = int(conditions['taxunpaidnum'] * 7.6324)
    else:
        pass


def solve_investnum(conditions):
    investnum_type = conditions.pop('investnum_type')
    if investnum_type == 'money_dollar':
        conditions['investnum'] = int(conditions['investnum'] * 7.0215)
    elif investnum_type == 'money_euro':
        conditions['investnum'] = int(conditions['investnum'] * 7.6324)
    else:
        pass

    # 投资比例处理
    invest_total = 0
    for i in range(16):
        invest_total += int(conditions['inv' + str(i)])

    if invest_total != 0:
        for i in range(16):
            conditions['inv' + str(i)] = int(conditions['inv' + str(i)]) / invest_total


def solve_isjnsn(conditions):
    # 省级市级处理
    if conditions['is_jnsn'] == 'level_province':
        conditions['is_jnsn'] = 2
    elif conditions['is_jnsn'] == 'level_city':
        conditions['is_jnsn'] = 1
    else:
        pass


def solve_passpercent(conditions):
    conditions['passpercent'] = conditions['passpercent'] / 100


def solve_creditgrade(conditions):
    # grade_list = ['C', 'B-', 'A-', 'A', 'N', 'N+']
    # grade = conditions['credit_grade']
    # score = grade_list.index(grade)
    # conditions['credit_grade'] = score
    pass


# 在这里拿到条件检索的 key:value
def conditionSearch(conditions):
    f = FCMAnswer.getInstance()
    if 'company_name' in conditions:
        company_name = conditions.pop('company_name')
    else:
        company_name = ""

    if 'csrfmiddlewaretoken' in conditions:
        conditions.pop('csrfmiddlewaretoken')

    # 空字段用处理
    for (key, value) in conditions.items():
        if len(value) == 0:
            conditions[key] = f.solve_unaccept_value(key, value)

    # bool类型字段转换
    for key in conditions:
        value = conditions[key]
        if isinstance(value, bool):
            conditions[key] = 1 if value else 0
        if isinstance(value, str):
            conditions[key] = 1 if value == 'True' else 0

    # 币种金额处理 汇率euro：7.6324  dollar：7.0215

    solve_regcapcur(conditions)
    solve_investnum(conditions)
    solve_isjnsn(conditions)
    solve_passpercent(conditions)
    solve_creditgrade(conditions)

    # conditions在这里拿到
    print("=========conditions============", conditions)
    print("========", f.getCompanyLabel(conditions, company_name), "==========")
    return f.getCompanyLabel(conditions, company_name)


def mutiSearch(filename):
    instance = FCMAnswer.getInstance()
    label_dic = instance.getCompanyLabelFromExecel(filename)
    destination = 'mutilabel.txt'
    with open(destination, 'w', encoding='utf-8') as f:
        f.write(json.dumps(label_dic, ensure_ascii=False, indent=4))
    return destination
# 外包大赛——Django项目

Django为项目主文件夹

templates文件夹中存放页面的源码

static文件夹中存放页面的样式CSS和逻辑处理文件Javascript



#### 前端接口：

Django文件夹中的views.py文件调用后端接口进行进一步的处理

Django文件夹中的IOProcess.py文件中有两个函数：

​	**fullNameSearch**对应**名称检索**，参数为name（str类型）

​	**conditionSearch**对应**条件检索**，参数为conditions（dict类型）,conditions字段中也会有company_name

​	两个函数的参数均为从前端表单中获取的输入值。

​	conditions中字段值的详细解释：

​	passpercent：**float**  eg：0.79

​	is_kcont:  **bool** eg: 'True'

​	credit_grade: **str** eg: 'N+'

​	is_justice_credit : **bool** eg: 'True'

​	is_justice_creditaic: **bool** eg: 'True'

​	ibrand_num: **int** eg:20

​	icopy_num : **int** eg:20

​	ipat_num: **int** eg:20

​	idom_num: **int** eg:20

​	is_jnsn: **int** eg: 0/1

​	inv0~inv15: **float**  eg: 0.21

​	xzbz1~xzbz9: **bool** eg: 'True'

​	regcapcur: **int** eg: 20000(元)

​	investnum: **int** eg:10000

​	regcap: **int** eg: 10000

​	empnum: **int** eg: 200

​	estdate: **str** eg:'2017/03/21'

​	branchnum: **int** eg: 20

​	shopnum: **int** eg: 20

​	qcwynum: **int** eg: 21

​	bidnum: **int** eg:10

​	qcwynum: **int** eg:10

​	is_infoa: **bool** eg: 'True'

​	is_infob: **bool** eg: 'True'

​	alttime: **int** eg: 5

​	defendant_num: **int** eg: 3

​	is_bra: **bool** eg: 'True'

​	is_brap: **int** eg: 5

​	pledgenum: **int** eg: 3

​	taxunpaidnum: **int** eg: 20000

​	is_except: **int** eg: 20

​	unpaidsocialins_s0110~s510: **int** eg:50000


### 后端提供的接口:

api/network/IAnswer.py， 具体实现在FCMAnswer.py中
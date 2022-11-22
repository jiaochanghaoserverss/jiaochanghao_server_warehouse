class DefaultRole:
    ALL = 'ALL'
    ADMIN = 'ADMIN'
    PM = 'PM'
    MINISTER = 'MINISTER'
    TESTER = 'TESTER'
    MASTER = 'MASTER'
    COMPANY = 'COMPANY'
    AUDITOR = 'AUDITOR'
    CHOICES = (
        (ADMIN, '管理员'),
        (PM, '项目经理'),
        (MINISTER, '部长'),
        (TESTER, '测试人员'),
        (MASTER, '领导'),
        (COMPANY, '企业人员'),
        (AUDITOR, '内审员'),
    )


class Gender:
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2

    CHOICES = (
        (UNKNOWN, '未知'),
        (MALE, '男'),
        (FEMALE, '女'),
    )


class SysDictType:
    HARD = 1
    SOFT = 2
    DEPARTMENT = 3
    CHOICES = (
        (HARD, '硬件'),
        (SOFT, '软件'),
        (DEPARTMENT, '组织架构'),
    )


class EnableStatus:
    DEFAULT = 0
    ENABLED = 1
    DISABLED = 2

    CHOICES = (
        (DEFAULT, '未发布'),
        (ENABLED, '启用'),
        (DISABLED, '禁用'),
    )


class DeclareType:
    HARD = 1
    SOFT = 2

    CHOICES = (
        (HARD, '硬件'),
        (SOFT, '软件'),
    )


class AuditStatus:
    WAITING = 0
    PASS = 1
    REJECT = 2

    CHOICES = (
        (WAITING, '待审核'),
        (PASS, '审核通过'),
        (REJECT, '审核不通过'),
    )


class TaskStatus:
    DEFAULT = 0
    SAMPLE = 1
    EVN = 2
    TESTING = 3
    REGRESSION = 4
    REPORTING = 5
    ARCHIVED = 6
    GIVE_UP = 7
    CHOICES = (
        (DEFAULT, '待分配'),
        (SAMPLE, '样品准备'),
        (EVN, '环境部署'),
        (TESTING, '首轮测试'),
        (REGRESSION, '回归测试'),
        (REPORTING, '出具报告'),
        (ARCHIVED, '已归档'),
        (GIVE_UP, '企业放弃'),
    )


class TaskState:
    DEFAULT = 0
    # 样品准备
    SAMPLE = 1
    SAMPLE_INFO_AUDIT = 3
    SIMPLE_FILE = 5
    SIMPLE_FILE_AUDIT = 7

    # 环境准备
    EVN = 9
    ENV_INFO_AUDIT = 10
    ENV_FILE = 13
    ENV_FILE_AUDIT = 15

    # 首轮测试
    TESTING = 17
    TESTING_AUDIT = 19

    # 回归测试
    REGRESSION = 410
    REGRESSION_AUDIT = 23

    # 出具报告
    REPORT_PM = 25
    REPORT_AUDITOR = 27
    REPORT_MINISTER = 29
    REPORT_UPLOAD = 31

    CHOICES = (
        (DEFAULT, '未开始'),
        (SAMPLE, '样品准备'),
        (SAMPLE_INFO_AUDIT, '样品信息审核'),
        (SIMPLE_FILE, '样品确认单'),
        (SIMPLE_FILE_AUDIT, '样品确认单审核'),
        (EVN, '环境准备'),
        (ENV_INFO_AUDIT, '环境信息审核'),
        (ENV_FILE, '环境确认单'),
        (ENV_FILE_AUDIT, '环境确认单审核'),
        (TESTING, '执行测试'),
        (TESTING_AUDIT, '测试结果审核'),
        (REGRESSION, '回归测试'),
        (REGRESSION_AUDIT, '回归结果审核'),
        (REPORT_PM, '项目经理审核'),
        (REPORT_AUDITOR, '内审员审核'),
        (REPORT_MINISTER, '部长审核'),
        (REPORT_UPLOAD, '报告盖章')
    )

    class ROLES:
        DEFAULT = DefaultRole.TESTER
        SAMPLE = DefaultRole.TESTER
        SAMPLE_INFO_AUDIT = DefaultRole.PM
        SIMPLE_FILE = DefaultRole.TESTER
        SIMPLE_FILE_AUDIT = DefaultRole.PM
        EVN = DefaultRole.TESTER
        ENV_INFO_AUDIT = DefaultRole.PM
        ENV_FILE = DefaultRole.TESTER
        ENV_FILE_AUDIT = DefaultRole.PM
        TESTING = DefaultRole.TESTER
        TESTING_AUDIT = DefaultRole.PM
        REGRESSION = DefaultRole.TESTER
        REGRESSION_AUDIT = DefaultRole.PM
        REPORT_PM = DefaultRole.PM
        REPORT_AUDITOR = DefaultRole.AUDITOR
        REPORT_MINISTER = DefaultRole.MINISTER
        REPORT_UPLOAD = DefaultRole.TESTER


class TaskNodeStatus:
    DEFAULT = 0
    BEING = 1
    FINISH = 2
    RESUBMITTED = 3
    FAIL = 4
    BACK = 5
    FAIL_RE_HANDLE = 6
    FINISH_FAIL = 7

    CHOICES = (
        (DEFAULT, '未开始'),
        (BEING, '进行中'),
        (FINISH, '已完成'),
        (RESUBMITTED, '待重新提交'),
        (FAIL, '失败'),
        (BACK, '打回'),
        (FAIL_RE_HANDLE, '失败重新处理'),
        (FINISH_FAIL, '已完成未通过'),
    )


class TestCategory:
    OTHER = 0
    SIMPLE_CONFIRM = 1
    PRODUCT_CONFIRM = 2
    SENIOR_CONFIRM = 3
    ACCEPTANCE_TEST = 4
    ADAPTER_TEST = 5
    CODE_SCAN = 6

    CHOICES = (
        (OTHER, '其他类型测试'),
        (SIMPLE_CONFIRM, '简单确认测试'),
        (PRODUCT_CONFIRM, '产品确认测试'),
        (SENIOR_CONFIRM, '高级确认测试'),
        (ACCEPTANCE_TEST, '验收测试'),
        (ADAPTER_TEST, '适配测试'),
        (CODE_SCAN, '代码扫描测试'),
    )
    NUMBERS = dict((
        (OTHER, '61'),
        (SIMPLE_CONFIRM, '62'),
        (PRODUCT_CONFIRM, '63'),
        (SENIOR_CONFIRM, '64'),
        (ACCEPTANCE_TEST, '65'),
        (ADAPTER_TEST, '66'),
        (CODE_SCAN, '6F'),
    ))


class TestCaseCategory:
    OTHER = 0
    FEATURE = 1
    RELIABILITY = 2
    USABILITY = 3
    PERFORMANCE = 4
    MAINTENANCE = 5
    COMPATIBILITY = 6
    PORTABILITY = 7
    SCALABILITY = 8
    SECURITY = 9
    STANDARDS_COMPLIANCE = 10
    SOURCE_CHECK = 11
    CHOICES = (
        (FEATURE, '功能测试'),
        (RELIABILITY, '可靠性测试'),
        (USABILITY, '易用性测试'),
        (PERFORMANCE, '性能效率测试'),
        (MAINTENANCE, '维护性测试'),
        (COMPATIBILITY, '兼容性测试'),
        (PORTABILITY, '可移植性测试'),
        (SCALABILITY, '可扩展性测试'),
        (SECURITY, '安全性测试'),
        (STANDARDS_COMPLIANCE, '标准符合性测试'),
        (SOURCE_CHECK, '源码检查测试'),
        (OTHER, '其他'),
    )


class ProductCategoryType:
    HARD = 1
    SOFT = 2
    CHOICES = (
        (HARD, '硬件'),
        (SOFT, '软件'),
    )


class StatType:
    NONE = 0
    AVG = 1
    MAX = 2
    MIN = 3
    CHOICES = (

        (NONE, '无需'),
        (AVG, '平均'),
        (MAX, '最大'),
        (MIN, '最小'),
    )


class TableStyle:
    H = 0
    V = 1
    CHOICES = (
        (H, '水平展示'),
        (V, '垂直展示'),
    )


class ClassifiedLevel:
    OTHER = 0
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4

    CHOICES = (
        (OTHER, '其他'),
        (L1, '无秘级'),
        (L2, '秘密'),
        (L3, '机密'),
        (L4, '绝密'),
    )


class PackagingStatus:
    DEFAULT = 0
    WELL = 1
    BROKEN = 2

    CHOICES = (
        (DEFAULT, '默认'),
        (WELL, '完好'),
        (BROKEN, '有撞击痕迹'),
    )


class EnvDeviceType:
    TEST = 1
    ACCOMPANY = 2
    PERIPHERALS = 3

    CHOICES = (
        (TEST, '测试客户端'),
        (ACCOMPANY, '陪测客户端'),
        (PERIPHERALS, '外设'),
    )


class QuestionType:
    OTHER = 0
    PROGRAM = 1
    DOCUMENT = 2
    DESIGN = 3
    CHOICES = (
        (OTHER, '其他问题'),
        (PROGRAM, '程序问题'),
        (DOCUMENT, '文档问题'),
        (DESIGN, '设计问题'),

    )


class QuestionLevel:
    DEFAULT = 0
    LOW = 1
    MINOR = 2
    MAJOR = 3
    CRITICAL = 4
    NOT_QUESTION = 5
    TURN_DOWN = 6
    CHOICES = (
        (DEFAULT, '未定级'),
        (LOW, '建议性'),
        (MINOR, '一般性问题'),
        (MAJOR, '严重性问题'),
        (CRITICAL, '致命问题'),
        (NOT_QUESTION, '不是问题'),
        (TURN_DOWN, '驳回'),
    )


class UploadFilePath:
    SLICE = 'slice_files'
    COMPLETE = 'complete_files'


class CategoryConfigFieldType:
    TEXT = 1
    NUMBER = 2
    SINGLE_CHOICE = 3
    MULTIPLE_CHOICE = 4
    CHOICES = (
        (TEXT, '文本'),
        (NUMBER, '数字'),
        (SINGLE_CHOICE, '单选'),
        (MULTIPLE_CHOICE, '多选'),
    )


class TaskTransitionType:
    DEFAULT = 0
    SUBMIT = 1
    PASSED = 2
    FAILED = 3

    CHOICES = (
        (DEFAULT, '默认值'),
        (SUBMIT, '提交审核'),
        (PASSED, '审核通过'),
        (FAILED, '审核不通过')
    )


class ResultType:
    DEFAULT = 0
    SUCCESS = 1
    FAIL = 2

    CHOICES = (
        (DEFAULT, '默认值'),
        (SUCCESS, '通过'),
        (FAIL, '失败'),
    )


class FileType:
    DEFAULT = 0
    SYSTEM = 1
    UPLOAD = 2
    CHOICES = (
        (DEFAULT, '默认'),
        (SYSTEM, '系统'),
        (UPLOAD, '用户上传'),
    )


class TemplateFile:
    PROJECT = 'project'
    PLANSHEET = 'plansheet'
    SAMPLE = 'sample'
    ENV = 'env'
    QUESTION = 'question'
    EXAMINE = 'examine'
    FILE = 'file'
    FRONT_COVER = 'front_cover'
    FILENAME_DICT = dict((
        (PROJECT, '测试项目模版.xlsx'),
        (SAMPLE, '样品接收归还表.docx'),
        (ENV, '测试环境确认表.docx'),
        (QUESTION, '问题确认单模版.docx'),
        (EXAMINE, '测试报告检查单模版.docx'),
        (FILE, '归档检查单模版.docx'),
        (PLANSHEET, '测试任务计划单.docx'),
        (FRONT_COVER, '问题报告单封面.docx'),
    ))


class Test_envs:
    OTHER = 0
    DEFAULT = 1
    SUBMIT = 2
    PASSED = 3
    FAILED = 4
    CHOICES = (
        (OTHER, '默认0'),
        (DEFAULT, '开发环境'),
        (SUBMIT, '测试环境'),
        (PASSED, '用户实际环境'),
        (FAILED, '本实验室部署')
    )
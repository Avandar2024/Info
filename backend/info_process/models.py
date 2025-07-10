from __future__ import annotations

from datetime import date, datetime

from sqlmodel import Field, SQLModel


class InfoBase(SQLModel):
	id: int | None = Field(default=None, primary_key=True)
	类型: str
	标题: str
	原文信息: str | None = Field(default=None)
	发布日期: date | None = Field(default=None)
	关键词: str | None = Field(default=None)
	原文链接: str | None = Field(default=None, index=True)


class 比赛通知(InfoBase, table=True):
	比赛开始时间: datetime | None = Field(default=None)
	比赛结束时间: datetime | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	主办方: str | None = Field(default=None)
	比赛地点: str | None = Field(default=None)
	比赛名称: str
	比赛级别_形式: str | None = Field(default=None, alias='比赛级别、形式')
	比赛主题: str | None = Field(default=None)
	参赛资格: str | None = Field(default=None)
	技能需求: str | None = Field(default=None)
	比赛奖励: str | None = Field(default=None)
	报名费用: str | None = Field(default=None)


class 学习资源(InfoBase, table=True):
	资源类型: str | None = Field(default=None)
	提供单位: str | None = Field(default=None)
	适用场景: str | None = Field(default=None)
	访问方式: str | None = Field(default=None)
	使用权限_身份: str | None = Field(default=None)
	使用权限_学院: str | None = Field(default=None)
	使用权限_设备: str | None = Field(default=None)
	功能描述: str | None = Field(default=None)
	是否需费用: bool | None = Field(default=None)
	有效期至: datetime | None = Field(default=None)
	技术支持: str | None = Field(default=None)
	关联服务: str | None = Field(default=None)


class 校园通知(InfoBase, table=True):
	通知性质: str | None = Field(default=None)
	核心对象: str | None = Field(default=None)
	相关服务_区域: str | None = Field(default=None, alias='相关服务、区域')
	生效时间: datetime | None = Field(default=None)
	截止时间: str | None = Field(default=None)
	责任部门: str | None = Field(default=None)
	核心摘要: str | None = Field(default=None)


class 学业申请(InfoBase, table=True):
	政策名称: str
	生效时间: datetime | None = Field(default=None)
	过期时间: datetime | None = Field(default=None)
	适用对象: str | None = Field(default=None)
	政策类别: str | None = Field(default=None)
	发布部门: str | None = Field(default=None)
	政策级别: str | None = Field(default=None)
	GPA要求: str | None = Field(default=None)
	学分要求: str | None = Field(default=None)
	其他要求: str | None = Field(default=None)
	特定课程门槛: str | None = Field(default=None)
	申请步骤: str | None = Field(default=None)
	申请起始日期: datetime | None = Field(default=None)
	申请截止时间: datetime | None = Field(default=None)
	相关材料: str | None = Field(default=None)
	相关政策: str | None = Field(default=None)


class 学业相关政策(InfoBase, table=True):
	政策名称: str
	生效时间: datetime | None = Field(default=None)
	过期时间: datetime | None = Field(default=None)
	发布部门: str | None = Field(default=None)
	适用对象: str | None = Field(default=None)
	政策类别: str | None = Field(default=None)
	核心条款: str | None = Field(default=None)
	关联系统: str | None = Field(default=None)
	系统操作指南链接: str | None = Field(default=None)


class 奖励_资助政策(InfoBase, table=True):
	政策名称: str
	政策类别: str | None = Field(default=None)
	适用年度: str | None = Field(default=None)
	奖励内容: str | None = Field(default=None)
	适用对象: str | None = Field(default=None)
	评定维度_学业成绩: str | None = Field(default=None)
	评定维度_科研创新: str | None = Field(default=None)
	评定维度_社会实践: str | None = Field(default=None)
	其他评定方法: str | None = Field(default=None)
	硬性否决条件_学业: str | None = Field(default=None)
	硬性否决条件_纪律: str | None = Field(default=None)
	是否需要答辩: bool | None = Field(default=None)
	材料清单: str | None = Field(default=None)


class 惩罚制度(InfoBase, table=True):
	政策名称: str
	政策类别: str | None = Field(default=None)
	适用对象: str | None = Field(default=None)
	处罚等级体系: str | None = Field(default=None)
	影响范围_评奖评优: str | None = Field(default=None)
	影响范围_保研资格: str | None = Field(default=None)
	关联政策: str | None = Field(default=None)


class 校园安全(InfoBase, table=True):
	政策名称: str
	政策类别: str | None = Field(default=None)
	管理对象类型: str | None = Field(default=None)
	责任主体: str | None = Field(default=None)
	适用对象: str | None = Field(default=None)


class 讲座或分享会信息(InfoBase, table=True):
	讲座起始时间: datetime | None = Field(default=None)
	讲座结束时间: datetime | None = Field(default=None)
	地点: str | None = Field(default=None)
	线上参会链接或腾讯会议号: str | None = Field(default=None)
	讲座类型: str | None = Field(default=None)
	讲座领域: str | None = Field(default=None)
	是否需要报名: bool | None = Field(default=None)
	五育认定类型: str | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	主讲人信息: str | None = Field(default=None)
	适用年级: str | None = Field(default=None)


class 志愿活动(InfoBase, table=True):
	主办单位: str | None = Field(default=None)
	服务起始时间: datetime | None = Field(default=None)
	服务结束时间: datetime | None = Field(default=None)
	服务地点类型: str | None = Field(default=None)
	详细地址: str | None = Field(default=None)
	线上服务方式: str | None = Field(default=None)
	志愿类型: str | None = Field(default=None)
	志愿时长_小时: str | None = Field(default=None)
	招募人数: int | None = Field(default=None)
	单次或长期: str | None = Field(default=None)
	技能要求: str | None = Field(default=None)
	是否培训: bool | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	面向群体: str | None = Field(default=None)
	是否提供证书: bool | None = Field(default=None)
	特殊福利: str | None = Field(default=None)


class 社会实践(InfoBase, table=True):
	活动开始时间: datetime | None = Field(default=None)
	活动结束时间: datetime | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	主办单位: str | None = Field(default=None)
	活动地点: str | None = Field(default=None)
	活动主题: str | None = Field(default=None)
	实践形式: str | None = Field(default=None)
	组队要求: str | None = Field(default=None)
	参与对象: str | None = Field(default=None)
	学分认定: str | None = Field(default=None)
	经费支持: str | None = Field(default=None)
	报名方式: str | None = Field(default=None)
	技能需求: str | None = Field(default=None)
	考核标准: str | None = Field(default=None)
	关联课程: str | None = Field(default=None)
	咨询方式: str | None = Field(default=None)


class 国际交流项目(InfoBase, table=True):
	项目名称: str
	项目类别: str | None = Field(default=None)
	合作国家地区: str | None = Field(default=None)
	合作院校机构: str | None = Field(default=None)
	项目申请截止时间: datetime | None = Field(default=None)
	项目开始日期: datetime | None = Field(default=None)
	项目结束日期: datetime | None = Field(default=None)
	项目时长描述: str | None = Field(default=None)
	学科领域: str | None = Field(default=None)
	申请资格_学历: str | None = Field(default=None)
	申请资格_GPA: str | None = Field(default=None)
	申请资格_其他: str | None = Field(default=None)
	语言要求_英语: str | None = Field(default=None)
	语言要求_小语种: str | None = Field(default=None)
	选拔标准: str | None = Field(default=None)
	申请材料清单: str | None = Field(default=None)
	资助信息_奖学金: str | None = Field(default=None)
	资助信息_生活补贴: str | None = Field(default=None)
	住宿安排类型: str | None = Field(default=None)
	文化适应资源: str | None = Field(default=None)
	项目亮点标签: str | None = Field(default=None)
	官方咨询渠道: str | None = Field(default=None)


class 社团消息(InfoBase, table=True):
	消息子类: str | None = Field(default=None)
	社团名称: str
	社团类别: str | None = Field(default=None)
	活动类型: str | None = Field(default=None)
	活动时间: str | None = Field(default=None)
	活动地点: str | None = Field(default=None)
	参与要求: str | None = Field(default=None)
	特色标签: str | None = Field(default=None)
	联系方式: str | None = Field(default=None)


class 文体活动(InfoBase, table=True):
	活动开始时间: datetime | None = Field(default=None)
	活动结束时间: datetime | None = Field(default=None)
	活动地点: str | None = Field(default=None)
	活动类型: str | None = Field(default=None)
	主办单位: str | None = Field(default=None)
	参与资格_年级: str | None = Field(default=None)
	参与资格_学院: str | None = Field(default=None)
	报名方式: str | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	费用金额: str | None = Field(default=None)
	活动亮点: str | None = Field(default=None)
	五育认定类型: str | None = Field(default=None)
	线上参与链接: str | None = Field(default=None)
	组队人数: str | None = Field(default=None)


class 实践培训活动(InfoBase, table=True):
	活动开始时间: datetime | None = Field(default=None)
	活动结束时间: datetime | None = Field(default=None)
	活动地点: str | None = Field(default=None)
	主办单位: str | None = Field(default=None)
	活动形式: str | None = Field(default=None)
	活动类型: str | None = Field(default=None)
	实践内容: str | None = Field(default=None)
	指导老师_讲师: str | None = Field(default=None, alias='指导老师、讲师')
	参与对象_年级: str | None = Field(default=None)
	参与对象_专业: str | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	费用金额: str | None = Field(default=None)
	是否提供证书: bool | None = Field(default=None)
	证书类型: str | None = Field(default=None)
	五育认定类型: str | None = Field(default=None)
	技能要求: str | None = Field(default=None)
	课程亮点: str | None = Field(default=None)
	报名方式: str | None = Field(default=None)


class 作品征集(InfoBase, table=True):
	主办单位: str | None = Field(default=None)
	征集开始时间: datetime | None = Field(default=None)
	提交截止时间: datetime | None = Field(default=None)
	作品主题: str | None = Field(default=None)
	作品形式: str | None = Field(default=None)
	内容要求: str | None = Field(default=None)
	格式要求: str | None = Field(default=None)
	参与资格_身份: str | None = Field(default=None)
	参与资格_人数: str | None = Field(default=None)
	提交渠道: str | None = Field(default=None)
	奖励设置: str | None = Field(default=None)
	成果应用: str | None = Field(default=None)


class 其他活动(InfoBase, table=True):
	活动名称: str
	主办单位: str | None = Field(default=None)
	活动起始时间: datetime | None = Field(default=None)
	活动结束时间: datetime | None = Field(default=None)
	地点: str | None = Field(default=None)
	线上参会链接或腾讯会议号: str | None = Field(default=None)
	活动类别: str | None = Field(default=None)
	涉及领域: str | None = Field(default=None)
	面向群体: str | None = Field(default=None)
	核心内容: str | None = Field(default=None)
	技能要求: str | None = Field(default=None)
	报名截止时间: datetime | None = Field(default=None)
	报名方式: str | None = Field(default=None)
	是否面试: bool | None = Field(default=None)
	五育认定类型: str | None = Field(default=None)
	携带材料: str | None = Field(default=None)


class 实习就业(InfoBase, table=True):
	公司名称: str | None = Field(default=None)
	工作地点: str | None = Field(default=None)
	实习开始时间: datetime | None = Field(default=None)
	实习持续时间: str | None = Field(default=None)
	申请截止日期: datetime | None = Field(default=None)
	招聘对象_年级: str | None = Field(default=None)
	招聘对象_专业: str | None = Field(default=None)
	学历要求: str | None = Field(default=None)
	技能要求: str | None = Field(default=None)
	工作内容: str | None = Field(default=None)
	薪资待遇: str | None = Field(default=None)
	公司福利: str | None = Field(default=None)
	申请方式: str | None = Field(default=None)
	是否提供转正机会: bool | None = Field(default=None)
	笔试要求: str | None = Field(default=None)
	面试要求: str | None = Field(default=None)


class 其他类型(InfoBase, table=True):
	内容分类: str | None = Field(default=None)
	核心内容摘要: str | None = Field(default=None)
	涉及对象: str | None = Field(default=None)
	生效时间: datetime | None = Field(default=None)
	失效时间: str | None = Field(default=None)
	行动截止时间: str | None = Field(default=None)
	来源部门: str | None = Field(default=None)
	来源层级: str | None = Field(default=None)


# A dictionary to map '类型' to the corresponding model class
model_map = {
	'比赛通知': 比赛通知,
	'学习资源': 学习资源,
	'校园通知': 校园通知,
	'学业申请': 学业申请,
	'学业相关政策': 学业相关政策,
	'奖励、资助政策': 奖励_资助政策,
	'惩罚制度': 惩罚制度,
	'校园安全': 校园安全,
	'讲座或分享会信息': 讲座或分享会信息,
	'志愿活动': 志愿活动,
	'社会实践': 社会实践,
	'国际交流项目': 国际交流项目,
	'社团消息': 社团消息,
	'文体活动': 文体活动,
	'实践培训活动': 实践培训活动,
	'作品征集': 作品征集,
	'其他活动': 其他活动,
	'实习就业': 实习就业,
	'其他类型': 其他类型,
}

# 旅游景点分析与AI旅游路线推荐系统

基于Django开发的旅游景点分析与AI智能旅游路线推荐平台。

## 项目简介

本系统是一个综合性的旅游景点分析平台，集成了景点数据管理、用户评论分析、AI智能客服和旅游路线推荐功能，为用户提供全方位的旅游信息服务。

## 技术栈

- **后端框架**: Django
- **数据库**: MySQL / SQLite
- **AI服务**: DeepSeek API 
- **数据处理**: Pandas, NumPy

## 功能模块

### 1. 首页展示

- 景点数量统计（收费景区、省份、城市）
- 热门景点排行榜
- 销量排行展示
- 中国地图数据可视化

### 2. 景点浏览与搜索

- 按省份、城市筛选景点
- 景点详情展示（评分、评论数、价格、标签）
- 景点图片展示

### 3. AI智能客服

- 基于DeepSeek的智能问答
- 旅游景点信息查询
- 旅游路线推荐

### 4. 用户系统

- 用户注册与登录
- 个人资料管理
- 评论与评分功能

### 5. 数据分析

- 景点热度分析
- 销量数据分析
- 用户评论分析

## 项目结构

```
travel/
├── AI/                      # AI相关功能
│   ├── Get_Chat.py         # AI聊天服务
│   └── Get_Message.py      # 消息处理
├── data/                    # 数据处理模块
│   ├── spider.py          # 数据爬虫
│   ├── data_analyse.py    # 数据分析
│   ├── csv_to_sql.py      # 数据导入
│   └── data_control.py    # 数据控制
├── home/                    # Django应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── urls.py            # URL路由
│   └── admin.py           # 管理后台
├── templates/               # HTML模板
├── media/                   # 媒体文件
├── travel/                  # Django项目配置
├── utils/                   # 工具函数
├── config.py               # 配置文件
├── manage.py              # Django管理脚本
└── requirements.txt       # 依赖列表
```

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ (可选，默认使用SQLite)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库配置

编辑 `config.py` 文件配置数据库连接：

```python
class Config:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'your_password'
    DATABASE = 'travel'
    PORT = 3306
```

### 运行项目

```bash
# 初始化数据库
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

访问 `http://127.0.0.1:8000/` 查看项目。

## 主要功能演示

### AI智能客服

系统基于DeepSeek API和LangChain构建智能客服，能够：

- 回答用户关于景点的问题
- 推荐合适的旅游景点
- 提供旅游路线建议

### 数据分析

系统包含完整的数据分析流程：

1. `spider.py` - 爬取景点数据
2. `data_control.py` - 数据清洗与处理
3. `csv_to_sql.py` - 导入数据库
4. `data_analyse.py` - 数据分析与可视化

## 依赖说明

| 依赖包       | 版本      | 用途      |
| --------- | ------- | ------- |
| Django    | -       | Web框架   | 
## 注意事项

1. AI功能需要配置有效的API Key
2. 首次运行需要执行数据库迁移
3. 确保MySQL服务正在运行（如使用MySQL）

## License

MIT License

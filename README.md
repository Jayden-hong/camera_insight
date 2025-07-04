# 📸 Camera Insight - 摄像头AI分析系统

一款基于web的摄像头点位周边区域类型分析工具，支持手动添加或Excel批量导入摄像头数据，提供多种多模态大模型做场景分析。

## ✨ 主要功能

### 📊 Excel/CSV批量导入
- 🗂️ 支持上传Excel文件（.xlsx, .xls格式）和CSV文件
- 🔄 自动解析详细的摄像头信息（摄像头编码、位置、类型等）
- 🗺️ 批量在地图和左侧面板显示摄像头点位

### 🎯 摄像头管理
- ➕ 动态添加、编辑、删除摄像头
- 🔗 地图标记与左侧列表同步显示

### 🤖 AI场景分析
- 📷 上传摄像头实时画面
- 🗺️ 自动生成30米区域平面图
- 🎚️ 可调节视野角度（30°-120°）和视野距离（20-100米）
- ✏️ 自定义分析提示词
- 🧠 基于AI模型进行场景识别和分析

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Flask
- 网络连接（用于地图加载和AI分析）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
创建 `.env` 文件并配置以下API密钥：
```bash
SILICONFLOW_API_KEY=你的SiliconFlow_API密钥
STEPFUN_API_KEY=你的阶跃星辰API密钥
```

### 启动服务
```bash
python app.py
```
服务将在本地: http://localhost:5001 启动

## 📋 数据格式要求

### CSV文件格式说明
系统支持包含以下字段的CSV文件（推荐使用UTF-8编码）：

| 字段名 | 说明 | 是否必需 | 示例 |
|--------|------|----------|------|
| 编码 | 识别码 | 可选 | 4403078300000000000 |
| 平台镜头名称 | 摄像头显示名称 | **必需** | XX大道XX场D口停车场出入口 |
| 区域 | 所属区域 | 可选 | XXXX区域 |
| 片区 | 所属片区 | 可选 | XXXX片区 |
| 建筑物 | 所在建筑物 | 可选 | 图书馆 |
| 楼层 | 所在楼层 | 可选 | 一层 |
| 场所类型 | 场所分类 | 可选 | 地上停车场 |
| 相对场所位置信息 | 相对位置 | 可选 | D口 |
| 具体场所位置信息 | 具体位置 | 可选 | 出入口 |
| 细节备注 | 补充说明 | 可选 | xxx大学对面 |
| 现场实际镜头名称 | 实际名称 | 可选 | - |
| 枪球类型 | 摄像头类型 | 可选 | 枪/球 |
| 经度 | 地理坐标经度 | **必需** | 119.221253 |
| 纬度 | 地理坐标纬度 | **必需** | 21.695207 |

### 📄 CSV格式示例见文档

> 💡 **重要提示：** 
> - 系统会自动识别CSV文件的列结构
> - 必须包含经度和纬度字段
> - 摄像头名称字段可以是"平台镜头名称"或"摄像头名称"
> - 建议使用UTF-8编码保存CSV文件避免中文乱码


## 📁 项目结构

```
camera_insight_demo/
├── 📄 app.py                    # Flask后端服务
├── 📁 static/
│   └── 🌐 index.html           # 主界面
├── 📋 requirements.txt         # Python依赖
├── 📊 camera_template.csv      # CSV模板文件
├── 🔒 .env                     # 环境变量配置
├── 🛡️ .gitignore              # Git忽略文件
└── 📖 README.md               # 说明文档
```


## ⚠️ 注意事项

1. ✅ 确保CSV文件格式正确，使用UTF-8编码
2. 📍 经度和纬度字段必须是有效的数值
3. 🔑 需要有效的API密钥才能使用AI分析功能
4. 🌐 地图加载需要网络连接
5. 🔒 请妥善保管API密钥，不要提交到版本控制系统

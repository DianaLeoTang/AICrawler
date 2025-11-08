# AICrawler
一个爬取顶刊定向方向的python工具
# 顶刊医学机器学习文章爬取工具

## 功能介绍

这个Python脚本可以帮助你爬取2025年在Nature、Science、Cell及其子刊发表的医学领域机器学习/深度学习相关文章。

## 覆盖的期刊

### Nature系列
- Nature
- Nature Medicine
- Nature Biotechnology
- Nature Methods
- Nature Machine Intelligence
- Nature Biomedical Engineering

### Science系列
- Science
- Science Translational Medicine
- Science Advances

### Cell系列
- Cell
- Cell Systems
- Cell Reports Medicine
- Cell Reports

## 使用方法

### 1. 安装依赖
```bash
pip install requests
```

### 2. 运行脚本
```bash
python journal_scraper.py
```

### 3. 输出文件
脚本会生成两个文件：
- `medical_ml_articles_2025.csv` - CSV格式的结果
- `medical_ml_articles_2025.json` - JSON格式的结果

## 数据来源

脚本使用以下合法的公开API：
1. **PubMed API** - 美国国立医学图书馆的免费数据库
2. **Crossref API** - 开放的学术引文数据库

## 搜索关键词

脚本会搜索包含以下关键词的文章：
- machine learning (机器学习)
- deep learning (深度学习)
- artificial intelligence (人工智能)
- neural network (神经网络)
- medical/clinical (医学/临床)
- diagnosis (诊断)
- prediction (预测)

## 输出字段说明

- **title**: 文章标题
- **authors**: 作者列表
- **journal**: 期刊名称
- **pub_date**: 发表日期
- **doi**: 数字对象唯一标识符
- **pmid**: PubMed ID (如果有)
- **url**: 文章链接
- **abstract**: 摘要 (如果有)

## 注意事项

1. **API使用限制**：脚本已内置延迟以遵守API使用规范
2. **网络要求**：需要能够访问PubMed和Crossref的API
3. **数据完整性**：由于API限制，单次运行可能无法获取所有文章
4. **合法性**：所有数据来源均为公开合法的学术数据库

## 进阶使用

### 修改搜索时间范围
编辑脚本中的 `year` 参数：
```python
scraper.scrape_all(year=2024)  # 改为2024年
```

### 添加更多期刊
在 `journals` 字典中添加：
```python
journals = {
    'Nature': ['Nature', 'Nature Medicine', '你的期刊名称'],
    # ...
}
```

### 修改关键词
在 `keywords` 列表中修改：
```python
keywords = ['machine learning', 'deep learning', '你的关键词']
```

## 故障排除

### 问题1: 网络连接错误
- 检查网络连接
- 确认可以访问 eutils.ncbi.nlm.nih.gov 和 api.crossref.org

### 问题2: 没有找到结果
- 尝试放宽搜索条件
- 检查年份是否正确
- 某些最新文章可能还未收录到数据库

### 问题3: API限制
- 脚本已设置延迟，如仍遇到限制，可增加sleep时间

## 示例输出

```
============================================================
开始爬取2025年顶刊医学机器学习相关文章
============================================================

--- 方法1: 通过PubMed搜索 ---
正在搜索: Nature Medicine...
找到 45 篇文章

--- 方法2: 通过Crossref搜索 ---
正在搜索 Nature Medicine 中的相关文章...
找到 52 篇文章

总共找到 87 篇独特文章

前5条结果预览:
============================================================

1. Deep learning predicts cardiovascular disease risk from retinal images
   期刊: Nature Medicine
   作者: Smith J, Johnson A, Williams B...
   发表日期: 2025-03-15
   DOI: 10.1038/s41591-025-xxxxx
```

## 许可证

本脚本仅供学术研究使用，请遵守各数据源的使用条款。

## 联系方式

如有问题或建议，欢迎反馈。

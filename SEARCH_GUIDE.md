# 🎯 Google Scholar + PubMed 联合检索指南

## 📋 检索策略概览


## 方法一：PubMed检索（推荐先做这个）⭐⭐⭐⭐⭐

### 🔗 访问地址
https://pubmed.ncbi.nlm.nih.gov

### 🔍 检索式（复制粘贴即可）

```
("Nature"[Journal] OR "Nature Medicine"[Journal] OR "Nature Biotechnology"[Journal] OR "Nature Methods"[Journal] OR "Nature Machine Intelligence"[Journal] OR "Science"[Journal] OR "Science Translational Medicine"[Journal] OR "Science Advances"[Journal] OR "Cell"[Journal] OR "Cell Systems"[Journal] OR "Cell Reports"[Journal] OR "Cell Reports Medicine"[Journal])
AND
("machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract] OR "artificial intelligence"[Title/Abstract] OR "neural network"[Title/Abstract] OR "AI"[Title/Abstract])
AND
(medical[Title/Abstract] OR clinical[Title/Abstract] OR diagnosis[Title/Abstract] OR patient[Title/Abstract] OR disease[Title/Abstract] OR treatment[Title/Abstract] OR healthcare[Title/Abstract])
AND
2025[PDAT]
```

### 📥 导出步骤
1. 搜索后，勾选所有结果（或点击"Send to" → "File"）
2. 选择格式：CSV 或 XML
3. 包含字段：
   - PMID
   - Title
   - Authors
   - Journal
   - Publication Date
   - DOI
   - Abstract
4. 点击"Create File"下载

### 💡 PubMed高级技巧
- 使用"Save Search"保存检索式，设置邮件提醒
- 使用"Similar articles"找相关文章
- 导出格式选择"PubMed"可以直接导入EndNote/Zotero

---

## 方法二：Google Scholar检索（推荐第二做）⭐⭐⭐⭐⭐

### 🔗 访问地址
https://scholar.google.com

### ⚙️ 第一步：设置图书馆链接（只需设置一次）

1. 点击左上角菜单 → "设置" → "图书馆链接"
2. 搜索并勾选：
   - ✅ Tsinghua University Library
   - ✅ Harvard University Library
3. 点击"保存"

**效果：** 之后搜索结果旁边会显示 `[清华图书馆]` 或 `[哈佛]` 链接，直接点击就能看PDF！

### 🔍 分期刊检索（逐个复制到Google Scholar）

#### 1. Nature
```
source:"Nature" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 2. Nature Medicine
```
source:"Nature Medicine" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 3. Nature Biotechnology
```
source:"Nature Biotechnology" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 4. Nature Methods
```
source:"Nature Methods" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 5. Science
```
source:"Science" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 6. Science Translational Medicine
```
source:"Science Translational Medicine" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 7. Cell
```
source:"Cell" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 8. Cell Systems
```
source:"Cell Systems" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

#### 9. Cell Reports Medicine
```
source:"Cell Reports Medicine" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) 2025
```

---

## 📥 从Google Scholar批量导出（3种方法）

### 方法A：使用Zotero浏览器插件（最推荐）⭐⭐⭐⭐⭐

1. 安装Zotero：https://www.zotero.org
2. 安装Zotero Connector浏览器插件
3. 在Google Scholar搜索结果页面
4. 点击浏览器右上角的Zotero图标
5. ✅ 自动批量导入所有文章！
6. 在Zotero中导出为CSV/Excel

**优点：**
- 一键导入整页结果
- 自动抓取PDF（在校园网内）
- 可以导出任意格式

### 方法B：手动复制BibTeX

1. 在Google Scholar搜索结果中
2. 点击文章下方的 **"引用"**
3. 点击 **"BibTeX"**
4. 复制粘贴到文本文件
5. 使用我提供的Python脚本解析BibTeX

### 方法C：使用Google Scholar的"我的图书馆"

1. 在搜索结果中点击⭐保存到"我的图书馆"
2. 访问"我的图书馆"：https://scholar.google.com/scholar?scilib=1
3. 勾选多篇文章
4. 点击"导出" → 选择格式

---

## 🔄 合并PubMed和Google Scholar结果

### 使用Excel合并

1. 将PubMed的CSV和Google Scholar的结果都导入Excel
2. 使用"删除重复项"功能（根据标题去重）
3. 或使用我提供的Python脚本自动合并

### 使用Python脚本合并

```bash
python merge_results.py pubmed_results.csv scholar_results.csv
```

---

## 📊 预期结果数量

根据以往经验：
- **PubMed**: 约100-300篇（2025年至今）
- **Google Scholar**: 约200-500篇（可能包含预印本）
- **合并去重后**: 约250-600篇

---

## 💡 Pro Tips

### 1. 在校园网内的优势
- Google Scholar会直接显示PDF链接
- 点击文章标题后右侧会有"清华图书馆"或"哈佛"链接
- 大部分文章都能直接下载全文

### 2. 提高检索精度
如果结果太多，可以在检索式中添加更具体的术语：
```
AND ("prediction model" OR "diagnostic model" OR "risk prediction")
```

### 3. 扩展检索范围
如果结果太少，可以：
- 去掉部分限制词（如不限定医学领域）
- 包含预印本（如bioRxiv）
- 扩展到2024年

### 4. 追踪最新文章
- PubMed: 保存检索式 + 设置邮件提醒
- Google Scholar: 创建Alert（点击搜索结果左下角的"创建提醒"）

---

## 🚀 推荐工作流程

### 第一天（30分钟）
1. ✅ PubMed检索并导出（10分钟）
2. ✅ 设置Google Scholar图书馆链接（2分钟）
3. ✅ 安装Zotero + 插件（5分钟）
4. ✅ 用Zotero批量抓取Google Scholar结果（10分钟）

### 第二天（20分钟）
1. ✅ 在Excel中合并两个数据源（5分钟）
2. ✅ 删除重复项（5分钟）
3. ✅ 按期刊、日期排序（5分钟）
4. ✅ 开始阅读！

---

## 📧 需要帮助？

如果遇到问题：
1. **清华图书馆咨询台**: https://lib.tsinghua.edu.cn
2. **哈佛图书馆咨询**: https://library.harvard.edu/ask
3. 或者告诉我具体问题，我继续帮你优化！

---

## 附录：Python合并脚本在这里

运行 `python combined_scraper.py` 会：
1. 自动从PubMed获取数据（需要网络）
2. 提供Google Scholar检索式
3. 合并两个来源的结果
4. 自动去重
5. 导出CSV和JSON

如果PubMed网络有问题，可以手动在PubMed网站导出CSV，然后用我的脚本合并。
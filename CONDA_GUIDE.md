# Conda环境创建和运行指南

## 🚀 快速开始（复制粘贴即可）

### 方法1：使用conda命令直接创建（推荐）

```bash
# 创建名为scholar_pubmed的Python环境
conda create -n scholar_pubmed python=3.10 -y

# 激活环境
conda activate scholar_pubmed

# 安装依赖包
pip install requests feedparser

# 运行脚本
python combined_scraper.py
```

### 方法2：使用environment.yml文件创建

```bash
# 使用配置文件创建环境
conda env create -f environment.yml

# 激活环境
conda activate scholar_pubmed

# 运行脚本
python combined_scraper.py
```

---

## 📋 详细步骤说明

### 第一步：创建conda环境

```bash
conda create -n scholar_pubmed python=3.10 -y
```

**说明：**
- `-n scholar_pubmed`: 环境名称（可以改成你喜欢的名字）
- `python=3.10`: Python版本
- `-y`: 自动确认，不用手动输入yes

### 第二步：激活环境

```bash
conda activate scholar_pubmed
```

**验证激活成功：**
命令行提示符前面应该显示 `(scholar_pubmed)`

### 第三步：安装依赖包

```bash
pip install requests feedparser
```

**或者一次性安装：**
```bash
pip install requests feedparser pandas
```

### 第四步：运行脚本

```bash
# 运行联合检索脚本
python combined_scraper.py

# 或者合并已有的CSV文件
python merge_results.py pubmed_results.csv scholar_results.csv
```

---

## 🔧 完整的一键运行脚本

### Linux/Mac用户：

创建一个 `run.sh` 文件：

```bash
#!/bin/bash

# 检查conda是否安装
if ! command -v conda &> /dev/null
then
    echo "❌ Conda未安装，请先安装Anaconda或Miniconda"
    exit
fi

echo "📦 创建conda环境..."
conda create -n scholar_pubmed python=3.10 -y

echo "🔄 激活环境..."
source activate scholar_pubmed

echo "📥 安装依赖..."
pip install requests feedparser

echo "🚀 运行脚本..."
python combined_scraper.py

echo "✅ 完成！"
```

运行：
```bash
chmod +x run.sh
./run.sh
```

### Windows用户：

创建一个 `run.bat` 文件：

```batch
@echo off

echo 📦 创建conda环境...
conda create -n scholar_pubmed python=3.10 -y

echo 🔄 激活环境...
call conda activate scholar_pubmed

echo 📥 安装依赖...
pip install requests feedparser

echo 🚀 运行脚本...
python combined_scraper.py

echo ✅ 完成！
pause
```

运行：双击 `run.bat` 文件

---

## 🛠️ 常见问题解决

### Q1: 提示conda命令不存在
**解决方案：**
```bash
# 检查conda是否安装
conda --version

# 如果没有安装，下载安装Miniconda（更轻量）
# Linux/Mac:
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 或者安装完整的Anaconda
# 访问：https://www.anaconda.com/download
```

### Q2: conda activate命令不工作
**解决方案：**
```bash
# 初始化conda
conda init bash  # 如果用bash
conda init zsh   # 如果用zsh

# 重启终端或运行
source ~/.bashrc  # 或 source ~/.zshrc
```

### Q3: pip安装速度太慢
**解决方案：使用清华镜像源**
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests feedparser
```

### Q4: 网络访问受限（PubMed/Google Scholar连接失败）
**解决方案：**
- 确保你在清华或哈佛的校园网内
- 或连接学校的VPN
- PubMed和Google Scholar不需要特殊网络权限

---

## 📦 完整的environment.yml配置文件

```yaml
name: scholar_pubmed
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.10
  - pip
  - pip:
    - requests>=2.31.0
    - feedparser>=6.0.0
```

使用方法：
```bash
conda env create -f environment.yml
conda activate scholar_pubmed
python combined_scraper.py
```

---

## 🎯 推荐工作流程

### 选项A：在本地运行（如果有网络）

```bash
# 1. 创建并激活环境
conda create -n scholar_pubmed python=3.10 -y
conda activate scholar_pubmed

# 2. 安装依赖
pip install requests feedparser

# 3. 运行脚本
python combined_scraper.py

# 4. 查看结果
ls -lh combined_results_2025.csv
```

### 选项B：手动检索 + 脚本合并（推荐）

```bash
# 1. 创建环境（同上）
conda create -n scholar_pubmed python=3.10 -y
conda activate scholar_pubmed
pip install requests feedparser pandas

# 2. 手动在PubMed和Google Scholar检索，导出CSV

# 3. 合并结果
python merge_results.py pubmed_export.csv scholar_export.csv merged_output.csv

# 4. 查看结果
cat merged_output.csv
```

---

## 🧹 环境管理命令

```bash
# 查看所有conda环境
conda env list

# 删除环境（如果不需要了）
conda env remove -n scholar_pubmed

# 导出环境（便于分享）
conda env export > environment.yml

# 更新包
pip install --upgrade requests feedparser
```

---

## 💻 完整示例（从零开始）

```bash
# === 第一次使用 ===

# 1. 创建环境
conda create -n scholar_pubmed python=3.10 -y

# 2. 激活环境
conda activate scholar_pubmed

# 3. 安装依赖
pip install requests feedparser

# 4. 下载脚本（如果还没有）
# 将combined_scraper.py放在当前目录

# 5. 运行
python combined_scraper.py

# === 以后使用 ===

# 直接激活环境并运行
conda activate scholar_pubmed
python combined_scraper.py
```

---

## 📝 检查清单

运行前确保：
- ✅ 已安装conda（`conda --version`）
- ✅ 环境已创建（`conda env list`）
- ✅ 依赖已安装（`pip list | grep requests`）
- ✅ 脚本文件在当前目录（`ls *.py`）
- ✅ 有网络连接（如果自动检索）

---

需要其他帮助随时告诉我！
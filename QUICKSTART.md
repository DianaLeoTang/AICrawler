# 🚀 快速开始 - 3分钟搞定

## 方式1：一键安装运行（最简单）⭐⭐⭐⭐⭐

### Linux/Mac用户：
```bash
# 下载所有文件后，在终端运行：
bash setup.sh
```

### Windows用户：
```batch
# 双击运行 setup.bat 文件
```

**就这么简单！脚本会自动：**
- ✅ 检查conda是否安装
- ✅ 创建Python环境
- ✅ 安装所需依赖
- ✅ 询问是否立即运行

---

## 方式2：手动命令（3条命令）

```bash
# 1. 创建环境
conda create -n scholar_pubmed python=3.10 -y

# 2. 激活环境并安装依赖
conda activate scholar_pubmed
pip install requests feedparser

# 3. 运行脚本
python combined_scraper.py
```

---

## 方式3：使用配置文件

```bash
# 一行命令创建环境
conda env create -f environment.yml

# 激活并运行
conda activate scholar_pubmed
python combined_scraper.py
```

---

## 📋 文件说明

| 文件 | 用途 | 必需 |
|------|------|------|
| `setup.sh` | Linux/Mac一键安装脚本 | ⭐推荐 |
| `setup.bat` | Windows一键安装脚本 | ⭐推荐 |
| `environment.yml` | Conda环境配置文件 | 可选 |
| `combined_scraper.py` | 主检索脚本 | ✅必需 |
| `merge_results.py` | 结果合并脚本 | ✅必需 |
| `CONDA_GUIDE.md` | 详细指南 | 参考 |
| `SEARCH_GUIDE.md` | 检索指南 | 参考 |

---

## ⚡ 超快速命令（复制粘贴）

```bash
# 一次性创建环境并安装依赖
conda create -n scholar_pubmed python=3.10 -y && \
conda activate scholar_pubmed && \
pip install requests feedparser && \
python combined_scraper.py
```

---

## 🎯 运行后你会得到：

1. **PubMed检索结果** - 自动从PubMed API获取
2. **Google Scholar检索式** - 9个现成的检索式
3. **合并后的CSV文件** - 去重后的完整结果
4. **JSON格式数据** - 便于程序处理

---

## 💡 Tips

- **首次运行慢？** 正常，conda在下载Python和依赖包
- **网络限制？** 使用清华镜像：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests feedparser`
- **PubMed连接失败？** 使用手动检索方法（见SEARCH_GUIDE.md）

---

## 🆘 遇到问题？

### conda命令不存在
```bash
# 安装Miniconda（轻量级）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### conda activate不工作
```bash
conda init bash  # 或 zsh
source ~/.bashrc  # 重新加载
```

### 网络太慢
```bash
# 使用国内镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
```

---

## 📞 需要更多帮助？

查看详细文档：
- `CONDA_GUIDE.md` - 完整的conda使用指南
- `SEARCH_GUIDE.md` - 手动检索的详细步骤

---

就是这么简单！🎉
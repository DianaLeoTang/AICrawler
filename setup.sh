#!/bin/bash

# 简单运行脚本 - 假设环境已创建

echo "================================================"
echo "   运行 Google Scholar + PubMed 检索工具"
echo "================================================"
echo ""

# 初始化conda
eval "$(conda shell.bash hook)" 2>/dev/null || eval "$(conda shell.zsh hook)" 2>/dev/null

# 激活环境
echo "🔄 激活conda环境 scholar_pubmed..."
conda activate scholar_pubmed

# 检查激活是否成功
if [ $? -ne 0 ]; then
    echo "❌ 环境激活失败"
    echo ""
    echo "请先运行: bash setup.sh 创建环境"
    exit 1
fi

echo "✓ 环境已激活"
echo ""

# 检查Python
if ! command -v python &> /dev/null; then
    echo "❌ Python未找到"
    echo "请检查conda环境是否正确安装"
    exit 1
fi

echo "✓ Python版本: $(python --version)"
echo ""

# 运行脚本
echo "🚀 开始检索..."
echo ""
python combined_scraper.py

echo ""
echo "================================================"
echo "✅ 检索完成！"
echo "================================================"
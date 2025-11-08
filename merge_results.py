#!/usr/bin/env python3
"""
PubMed + Google Scholar 结果合并工具
用于合并从两个数据库手动导出的CSV文件
"""

import csv
import json
import sys
from typing import List, Dict, Set

def normalize_title(title: str) -> str:
    """标准化标题用于比对"""
    return title.lower().strip().replace('.', '').replace(',', '')

def read_csv_file(filepath: str) -> List[Dict]:
    """读取CSV文件"""
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        print(f"✓ 读取 {filepath}: {len(results)} 条记录")
        return results
    except Exception as e:
        print(f"✗ 读取文件失败 {filepath}: {e}")
        return []

def merge_and_deduplicate(pubmed_data: List[Dict], scholar_data: List[Dict]) -> List[Dict]:
    """合并并去重"""
    merged = []
    seen_titles = set()
    
    # 首先添加PubMed结果（通常更可靠）
    for item in pubmed_data:
        title = item.get('Title', item.get('title', ''))
        normalized = normalize_title(title)
        
        if normalized and normalized not in seen_titles:
            seen_titles.add(normalized)
            item['data_source'] = 'PubMed'
            merged.append(item)
    
    # 添加Google Scholar结果（跳过重复）
    duplicates = 0
    for item in scholar_data:
        title = item.get('Title', item.get('title', ''))
        normalized = normalize_title(title)
        
        if normalized and normalized not in seen_titles:
            seen_titles.add(normalized)
            item['data_source'] = 'Google Scholar'
            merged.append(item)
        else:
            duplicates += 1
    
    print(f"\n合并统计:")
    print(f"  PubMed记录: {len(pubmed_data)}")
    print(f"  Google Scholar记录: {len(scholar_data)}")
    print(f"  重复记录: {duplicates}")
    print(f"  合并后: {len(merged)}")
    
    return merged

def save_results(data: List[Dict], output_file: str):
    """保存结果"""
    if not data:
        print("✗ 没有数据可保存")
        return
    
    # 获取所有可能的字段
    all_fields = set()
    for item in data:
        all_fields.update(item.keys())
    
    # 保存CSV
    csv_file = output_file if output_file.endswith('.csv') else f'{output_file}.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=sorted(all_fields))
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n✓ CSV结果已保存: {csv_file}")
    
    # 保存JSON
    json_file = csv_file.replace('.csv', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON结果已保存: {json_file}")
    
    # 生成简单统计
    print("\n" + "="*60)
    print("前10条记录预览:")
    print("="*60)
    
    for i, item in enumerate(data[:10], 1):
        title = item.get('Title', item.get('title', 'N/A'))
        journal = item.get('Journal', item.get('journal', 'N/A'))
        source = item.get('data_source', 'N/A')
        print(f"\n{i}. {title[:80]}...")
        print(f"   期刊: {journal} | 来源: {source}")

def main():
    print("="*60)
    print("PubMed + Google Scholar 结果合并工具")
    print("="*60)
    
    if len(sys.argv) < 3:
        print("\n使用方法:")
        print("  python merge_results.py <pubmed.csv> <scholar.csv> [output.csv]")
        print("\n示例:")
        print("  python merge_results.py pubmed_export.csv scholar_export.csv merged_results.csv")
        print("\n说明:")
        print("  - pubmed.csv: 从PubMed导出的CSV文件")
        print("  - scholar.csv: 从Google Scholar导出的CSV文件")
        print("  - output.csv: 输出文件名（可选，默认为merged_results.csv）")
        return
    
    pubmed_file = sys.argv[1]
    scholar_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else '/mnt/user-data/outputs/merged_results.csv'
    
    print(f"\n输入文件:")
    print(f"  PubMed: {pubmed_file}")
    print(f"  Google Scholar: {scholar_file}")
    print(f"输出文件: {output_file}\n")
    
    # 读取文件
    pubmed_data = read_csv_file(pubmed_file)
    scholar_data = read_csv_file(scholar_file)
    
    if not pubmed_data and not scholar_data:
        print("\n✗ 没有读取到任何数据，请检查文件路径和格式")
        return
    
    # 合并去重
    merged_data = merge_and_deduplicate(pubmed_data, scholar_data)
    
    # 保存结果
    save_results(merged_data, output_file)
    
    print("\n✅ 合并完成！")

if __name__ == "__main__":
    main()
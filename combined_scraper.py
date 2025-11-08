#!/usr/bin/env python3
"""
Google Scholar + PubMed 联合检索工具
检索2025年Nature/Science/Cell系列医学机器学习文章
取两个数据库结果的并集
"""

import requests
import time
import csv
import json
from typing import List, Dict, Set
from datetime import datetime
import re

class ScholarPubMedScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.pubmed_results = []
        self.scholar_results = []
        self.merged_results = []
        
    def search_pubmed(self, year: int = 2025) -> List[Dict]:
        """
        使用PubMed API进行检索
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # 定义期刊列表
        journals = [
            'Nature', 'Nature Medicine', 'Nature Biotechnology', 'Nature Methods',
            'Nature Machine Intelligence', 'Nature Biomedical Engineering',
            'Science', 'Science Translational Medicine', 'Science Advances',
            'Cell', 'Cell Systems', 'Cell Reports', 'Cell Reports Medicine'
        ]
        
        # 构建查询
        journal_query = ' OR '.join([f'"{j}"[Journal]' for j in journals])
        
        query = f'''
        ({journal_query}) 
        AND (machine learning[Title/Abstract] OR deep learning[Title/Abstract] 
             OR artificial intelligence[Title/Abstract] OR neural network[Title/Abstract]
             OR AI[Title/Abstract] OR ML[Title/Abstract])
        AND (medical[Title/Abstract] OR clinical[Title/Abstract] 
             OR diagnosis[Title/Abstract] OR patient[Title/Abstract]
             OR disease[Title/Abstract] OR treatment[Title/Abstract]
             OR healthcare[Title/Abstract])
        AND {year}[PDAT]
        '''
        
        print("=" * 70)
        print("📚 PubMed 检索中...")
        print("=" * 70)
        
        try:
            # 第一步：搜索获取ID
            search_url = f"{base_url}esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': 500,  # 增加到500篇
                'retmode': 'json',
                'sort': 'pub_date',
                'mindate': f'{year}/01/01',
                'maxdate': f'{year}/12/31'
            }
            
            response = requests.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            search_data = response.json()
            
            id_list = search_data.get('esearchresult', {}).get('idlist', [])
            total_count = search_data.get('esearchresult', {}).get('count', 0)
            print(f"✓ PubMed找到 {total_count} 篇文章，正在获取前 {len(id_list)} 篇详情...")
            
            if not id_list:
                return []
            
            # 第二步：批量获取详情（每次100篇）
            articles = []
            batch_size = 100
            
            for i in range(0, len(id_list), batch_size):
                batch_ids = id_list[i:i+batch_size]
                print(f"  正在获取第 {i+1}-{min(i+batch_size, len(id_list))} 篇...")
                
                time.sleep(0.5)  # API限制
                
                summary_url = f"{base_url}esummary.fcgi"
                summary_params = {
                    'db': 'pubmed',
                    'id': ','.join(batch_ids),
                    'retmode': 'json'
                }
                
                response = requests.get(summary_url, params=summary_params, timeout=30)
                response.raise_for_status()
                summary_data = response.json()
                
                for pmid, article_data in summary_data.get('result', {}).items():
                    if pmid == 'uids':
                        continue
                    
                    authors = article_data.get('authors', [])
                    author_list = '; '.join([a.get('name', '') for a in authors[:10]])
                    
                    # 提取DOI
                    doi = ''
                    article_ids = article_data.get('articleids', [])
                    for aid in article_ids:
                        if aid.get('idtype') == 'doi':
                            doi = aid.get('value', '')
                            break
                    
                    article = {
                        'pmid': pmid,
                        'title': article_data.get('title', ''),
                        'authors': author_list,
                        'journal': article_data.get('fulljournalname', ''),
                        'pub_date': article_data.get('pubdate', ''),
                        'doi': doi or article_data.get('elocationid', ''),
                        'source': article_data.get('source', ''),
                        'link': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        'data_source': 'PubMed'
                    }
                    articles.append(article)
            
            print(f"✓ PubMed检索完成，共获取 {len(articles)} 篇文章\n")
            return articles
            
        except Exception as e:
            print(f"✗ PubMed检索错误: {e}\n")
            return []
    
    def search_google_scholar_serpapi(self, year: int = 2025, api_key: str = None) -> List[Dict]:
        """
        使用SerpAPI检索Google Scholar（需要API key）
        """
        if not api_key:
            print("=" * 70)
            print("📚 Google Scholar 检索（需要API key）")
            print("=" * 70)
            print("⚠️  Google Scholar检索需要API key")
            print("   可以在 https://serpapi.com 注册获取免费额度")
            print("   或使用下面的备用方法\n")
            return []
        
        print("=" * 70)
        print("📚 Google Scholar 检索中...")
        print("=" * 70)
        
        # 定义期刊
        journals = [
            'Nature', 'Nature Medicine', 'Nature Biotechnology',
            'Science', 'Science Translational Medicine',
            'Cell', 'Cell Systems', 'Cell Reports Medicine'
        ]
        
        all_articles = []
        
        for journal in journals:
            query = f'source:"{journal}" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) {year}'
            
            print(f"  正在搜索 {journal}...")
            
            try:
                params = {
                    'engine': 'google_scholar',
                    'q': query,
                    'api_key': api_key,
                    'num': 20,  # 每个期刊获取20篇
                    'as_ylo': year,
                    'as_yhi': year
                }
                
                response = requests.get('https://serpapi.com/search', params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                results = data.get('organic_results', [])
                
                for result in results:
                    article = {
                        'title': result.get('title', ''),
                        'authors': result.get('publication_info', {}).get('authors', []),
                        'journal': journal,
                        'pub_date': result.get('publication_info', {}).get('summary', ''),
                        'link': result.get('link', ''),
                        'snippet': result.get('snippet', ''),
                        'data_source': 'Google Scholar'
                    }
                    all_articles.append(article)
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                print(f"    ✗ 错误: {e}")
                continue
        
        print(f"✓ Google Scholar检索完成，共获取 {len(all_articles)} 篇文章\n")
        return all_articles
    
    def search_google_scholar_manual(self, year: int = 2025) -> List[Dict]:
        """
        Google Scholar手动检索指南（无需API）
        """
        print("=" * 70)
        print("📚 Google Scholar 手动检索指南")
        print("=" * 70)
        
        journals = [
            'Nature', 'Nature Medicine', 'Nature Biotechnology', 'Nature Methods',
            'Science', 'Science Translational Medicine',
            'Cell', 'Cell Systems', 'Cell Reports Medicine'
        ]
        
        print("\n🔍 请在Google Scholar中使用以下检索式：")
        print("\n" + "=" * 70)
        
        for i, journal in enumerate(journals, 1):
            query = f'source:"{journal}" ("machine learning" OR "deep learning" OR "artificial intelligence") (medical OR clinical OR diagnosis) {year}'
            print(f"\n{i}. {journal}:")
            print(f"   {query}")
        
        print("\n" + "=" * 70)
        print("\n📋 操作步骤：")
        print("1. 访问 https://scholar.google.com")
        print("2. 复制上面的检索式到搜索框")
        print("3. 点击搜索结果右下角的 '引用' → 'BibTeX'")
        print("4. 或直接复制标题、作者、期刊等信息")
        print("5. 在清华/哈佛校园网内可直接看到PDF链接")
        
        print("\n💡 提示：")
        print("- Google Scholar结果可以用引用管理软件（Zotero/EndNote）批量导出")
        print("- 在校园网内会自动显示图书馆的全文链接")
        print("- 可以设置Google Scholar的'图书馆链接'为清华或哈佛")
        
        print("\n⚙️  设置图书馆链接：")
        print("1. Google Scholar → 设置 → 图书馆链接")
        print("2. 搜索 'Tsinghua' 或 'Harvard'")
        print("3. 勾选图书馆，保存")
        print("4. 之后搜索结果会显示图书馆全文链接\n")
        
        return []
    
    def merge_results(self, pubmed_results: List[Dict], scholar_results: List[Dict]) -> List[Dict]:
        """
        合并PubMed和Google Scholar结果，去重
        """
        print("=" * 70)
        print("🔄 合并结果并去重...")
        print("=" * 70)
        
        # 用于去重的集合
        seen_titles = set()
        seen_dois = set()
        merged = []
        
        # 先添加PubMed结果
        for article in pubmed_results:
            title = article.get('title', '').lower().strip()
            doi = article.get('doi', '').lower().strip()
            
            # 标题去重
            if title and title not in seen_titles:
                seen_titles.add(title)
                if doi:
                    seen_dois.add(doi)
                merged.append(article)
        
        # 再添加Google Scholar结果（跳过重复）
        for article in scholar_results:
            title = article.get('title', '').lower().strip()
            
            if title and title not in seen_titles:
                seen_titles.add(title)
                merged.append(article)
        
        print(f"✓ PubMed结果: {len(pubmed_results)} 篇")
        print(f"✓ Google Scholar结果: {len(scholar_results)} 篇")
        print(f"✓ 合并后（去重）: {len(merged)} 篇\n")
        
        return merged
    
    def save_results(self, results: List[Dict], filename: str = 'combined_results_2025.csv'):
        """
        保存结果到CSV和JSON
        """
        if not results:
            print("⚠️  没有结果可保存\n")
            return None
        
        output_path = f'/mnt/user-data/outputs/{filename}'
        
        # 保存CSV
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['title', 'authors', 'journal', 'pub_date', 'doi', 'pmid', 'link', 'data_source', 'snippet']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for article in results:
                writer.writerow(article)
        
        print(f"✓ CSV结果已保存: {output_path}")
        
        # 保存JSON
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ JSON结果已保存: {json_path}\n")
        
        return output_path
    
    def generate_report(self, results: List[Dict]):
        """
        生成统计报告
        """
        if not results:
            return
        
        print("=" * 70)
        print("📊 统计报告")
        print("=" * 70)
        
        # 按期刊统计
        journal_count = {}
        source_count = {}
        
        for article in results:
            journal = article.get('journal', 'Unknown')
            source = article.get('data_source', 'Unknown')
            
            journal_count[journal] = journal_count.get(journal, 0) + 1
            source_count[source] = source_count.get(source, 0) + 1
        
        print("\n📚 各期刊文章数量:")
        for journal, count in sorted(journal_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {journal}: {count} 篇")
        
        print("\n🔍 数据来源统计:")
        for source, count in sorted(source_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {source}: {count} 篇")
        
        print("\n" + "=" * 70)
        print("📄 最新10篇文章预览:")
        print("=" * 70)
        
        for i, article in enumerate(results[:10], 1):
            print(f"\n{i}. {article.get('title', 'N/A')}")
            print(f"   📚 期刊: {article.get('journal', 'N/A')}")
            print(f"   ✍️  作者: {article.get('authors', 'N/A')[:80]}...")
            print(f"   📅 日期: {article.get('pub_date', 'N/A')}")
            print(f"   🔗 链接: {article.get('link', 'N/A')}")
            print(f"   📊 来源: {article.get('data_source', 'N/A')}")
    
    def run(self, year: int = 2025, serpapi_key: str = None):
        """
        主执行函数
        """
        print("\n" + "=" * 70)
        print("🚀 Google Scholar + PubMed 联合检索")
        print("=" * 70)
        print(f"检索年份: {year}")
        print(f"目标期刊: Nature/Science/Cell 系列")
        print(f"关键词: 机器学习 + 医学/临床")
        print("=" * 70 + "\n")
        
        # 1. PubMed检索
        self.pubmed_results = self.search_pubmed(year)
        
        # 2. Google Scholar检索
        if serpapi_key:
            self.scholar_results = self.search_google_scholar_serpapi(year, serpapi_key)
        else:
            # 提供手动检索指南
            self.search_google_scholar_manual(year)
            self.scholar_results = []
        
        # 3. 合并结果
        self.merged_results = self.merge_results(self.pubmed_results, self.scholar_results)
        
        # 4. 保存结果
        if self.merged_results:
            self.save_results(self.merged_results)
            self.generate_report(self.merged_results)
        
        print("=" * 70)
        print("✅ 检索完成！")
        print("=" * 70)

def main():
    scraper = ScholarPubMedScraper()
    
    # 运行检索
    # 如果有SerpAPI key，可以传入：scraper.run(2025, serpapi_key='your_key')
    scraper.run(2025)
    
    print("\n💡 提示：")
    print("- PubMed数据已自动获取")
    print("- Google Scholar需要手动检索或使用API")
    print("- 建议使用Google Scholar的'引用'功能批量导出")
    print("- 可以用Zotero等工具从Google Scholar批量导入\n")

if __name__ == "__main__":
    main()
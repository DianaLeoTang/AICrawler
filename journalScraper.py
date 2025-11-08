#!/usr/bin/env python3
"""
顶刊医学机器学习文章爬取工具
爬取Nature、Science、Cell及其子刊在2025年发表的医学AI/ML相关文章
"""

import requests
import json
import time
from datetime import datetime
import csv
import os
from typing import List, Dict

class JournalScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.results = []
        
    def search_pubmed(self, query: str, year: int = 2025) -> List[Dict]:
        """
        使用PubMed API搜索文章
        PubMed是合法的公开数据库
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # 第一步：搜索获取ID列表
        search_url = f"{base_url}esearch.fcgi"
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': 100,
            'retmode': 'json',
            'sort': 'pub_date',
            'mindate': f'{year}/01/01',
            'maxdate': f'{year}/12/31'
        }
        
        print(f"正在搜索: {query}")
        time.sleep(0.5)  # 遵守API使用规范
        
        try:
            response = requests.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            search_data = response.json()
            
            id_list = search_data.get('esearchresult', {}).get('idlist', [])
            print(f"找到 {len(id_list)} 篇文章")
            
            if not id_list:
                return []
            
            # 第二步：获取详细信息
            fetch_url = f"{base_url}efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(id_list[:50]),  # 限制每次50篇
                'retmode': 'xml',
                'rettype': 'abstract'
            }
            
            time.sleep(0.5)
            response = requests.get(fetch_url, params=fetch_params, timeout=30)
            
            # 第三步：获取JSON格式的摘要数据
            summary_url = f"{base_url}esummary.fcgi"
            summary_params = {
                'db': 'pubmed',
                'id': ','.join(id_list[:50]),
                'retmode': 'json'
            }
            
            time.sleep(0.5)
            response = requests.get(summary_url, params=summary_params, timeout=30)
            response.raise_for_status()
            summary_data = response.json()
            
            articles = []
            for pmid, article_data in summary_data.get('result', {}).items():
                if pmid == 'uids':
                    continue
                    
                article = {
                    'pmid': pmid,
                    'title': article_data.get('title', ''),
                    'authors': ', '.join([author.get('name', '') for author in article_data.get('authors', [])[:5]]),
                    'journal': article_data.get('fulljournalname', ''),
                    'pub_date': article_data.get('pubdate', ''),
                    'doi': article_data.get('elocationid', ''),
                    'source': article_data.get('source', ''),
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"错误: {e}")
            return []
    
    def search_crossref(self, journal: str, keywords: List[str], year: int = 2025) -> List[Dict]:
        """
        使用Crossref API搜索文章
        Crossref是合法的开放引文数据库
        """
        base_url = "https://api.crossref.org/works"
        
        query = ' AND '.join(keywords)
        params = {
            'query.container-title': journal,
            'query': query,
            'filter': f'from-pub-date:{year},until-pub-date:{year}',
            'rows': 50,
            'select': 'DOI,title,author,published-print,container-title,abstract'
        }
        
        print(f"正在搜索 {journal} 中的相关文章...")
        time.sleep(1)  # 遵守API使用规范
        
        try:
            response = requests.get(base_url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('message', {}).get('items', []):
                authors = item.get('author', [])
                author_names = ', '.join([f"{a.get('given', '')} {a.get('family', '')}" for a in authors[:5]])
                
                pub_date = item.get('published-print', item.get('published-online', {}))
                date_parts = pub_date.get('date-parts', [[]])[0]
                pub_date_str = '-'.join(map(str, date_parts)) if date_parts else ''
                
                article = {
                    'doi': item.get('DOI', ''),
                    'title': item.get('title', [''])[0],
                    'authors': author_names,
                    'journal': item.get('container-title', [''])[0],
                    'pub_date': pub_date_str,
                    'abstract': item.get('abstract', ''),
                    'url': f"https://doi.org/{item.get('DOI', '')}"
                }
                articles.append(article)
            
            print(f"找到 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            print(f"错误: {e}")
            return []
    
    def scrape_all(self):
        """
        爬取所有期刊的文章
        """
        print("=" * 60)
        print("开始爬取2025年顶刊医学机器学习相关文章")
        print("=" * 60)
        
        # 定义搜索策略
        journals = {
            'Nature': ['Nature', 'Nature Medicine', 'Nature Biotechnology', 'Nature Methods'],
            'Science': ['Science', 'Science Translational Medicine'],
            'Cell': ['Cell', 'Cell Systems', 'Cell Reports Medicine']
        }
        
        keywords = ['machine learning', 'deep learning', 'artificial intelligence', 
                   'neural network', 'medical', 'clinical', 'diagnosis', 'prediction']
        
        # 方法1: 使用PubMed搜索
        print("\n--- 方法1: 通过PubMed搜索 ---")
        for journal_family, journal_list in journals.items():
            for journal in journal_list:
                query = f'("{journal}"[Journal]) AND (machine learning OR deep learning OR artificial intelligence) AND (medical OR clinical OR diagnosis OR prediction) AND 2025[PDAT]'
                articles = self.search_pubmed(query, 2025)
                self.results.extend(articles)
        
        # 方法2: 使用Crossref搜索
        print("\n--- 方法2: 通过Crossref搜索 ---")
        for journal_family, journal_list in journals.items():
            for journal in journal_list:
                articles = self.search_crossref(journal, keywords[:4], 2025)
                self.results.extend(articles)
        
        # 去重
        unique_results = []
        seen_titles = set()
        for article in self.results:
            title = article.get('title', '').lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(article)
        
        self.results = unique_results
        print(f"\n总共找到 {len(self.results)} 篇独特文章")
        
    def save_results(self, filename: str = 'medical_ml_articles_2025.csv'):
        """
        保存结果到CSV文件
        """
        if not self.results:
            print("没有结果可保存")
            return
        
        output_path = f'/mnt/user-data/outputs/{filename}'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'authors', 'journal', 'pub_date', 'doi', 'pmid', 'url']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for article in self.results:
                writer.writerow(article)
        
        print(f"\n结果已保存到: {output_path}")
        
        # 同时保存JSON格式
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"JSON格式已保存到: {json_path}")
        
        return output_path

def main():
    """
    主函数
    """
    scraper = JournalScraper()
    
    # 执行爬取
    scraper.scrape_all()
    
    # 保存结果
    output_file = scraper.save_results()
    
    # 显示前几条结果
    if scraper.results:
        print("\n" + "=" * 60)
        print("前5条结果预览:")
        print("=" * 60)
        for i, article in enumerate(scraper.results[:5], 1):
            print(f"\n{i}. {article.get('title', 'N/A')}")
            print(f"   期刊: {article.get('journal', 'N/A')}")
            print(f"   作者: {article.get('authors', 'N/A')[:100]}...")
            print(f"   发表日期: {article.get('pub_date', 'N/A')}")
            print(f"   DOI: {article.get('doi', 'N/A')}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
顶刊医学机器学习文章爬取工具 - 订阅版
适用于有期刊订阅权限的机构用户
支持多种数据源：Web of Science, Scopus, PubMed, 期刊官网RSS
"""

import requests
import feedparser
import json
import csv
import time
from datetime import datetime
from typing import List, Dict
import xml.etree.ElementTree as ET

class SubscriptionScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.results = []
        
    def scrape_nature_rss(self, journal_name: str, rss_url: str) -> List[Dict]:
        """
        通过Nature系列期刊的RSS源获取文章
        Nature提供免费的RSS订阅
        """
        print(f"正在从RSS获取 {journal_name} 的文章...")
        try:
            feed = feedparser.parse(rss_url)
            articles = []
            
            keywords = ['machine learning', 'deep learning', 'artificial intelligence', 
                       'neural network', 'AI', 'ML', 'medical', 'clinical', 'diagnosis']
            
            for entry in feed.entries:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                # 检查是否包含相关关键词
                if any(kw in title or kw in summary for kw in keywords):
                    article = {
                        'title': entry.get('title', ''),
                        'authors': entry.get('author', ''),
                        'journal': journal_name,
                        'pub_date': entry.get('published', ''),
                        'link': entry.get('link', ''),
                        'doi': entry.get('prism_doi', ''),
                        'summary': entry.get('summary', '')[:500]
                    }
                    articles.append(article)
            
            print(f"找到 {len(articles)} 篇相关文章")
            return articles
            
        except Exception as e:
            print(f"RSS解析错误: {e}")
            return []
    
    def scrape_science_rss(self, journal_name: str, rss_url: str) -> List[Dict]:
        """
        通过Science系列期刊的RSS源获取文章
        """
        print(f"正在从RSS获取 {journal_name} 的文章...")
        try:
            feed = feedparser.parse(rss_url)
            articles = []
            
            keywords = ['machine learning', 'deep learning', 'artificial intelligence', 
                       'neural network', 'AI', 'medical', 'clinical']
            
            for entry in feed.entries:
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if any(kw in title or kw in summary for kw in keywords):
                    article = {
                        'title': entry.get('title', ''),
                        'authors': entry.get('author', ''),
                        'journal': journal_name,
                        'pub_date': entry.get('published', ''),
                        'link': entry.get('link', ''),
                        'doi': entry.get('dc_identifier', ''),
                        'summary': entry.get('summary', '')[:500]
                    }
                    articles.append(article)
            
            print(f"找到 {len(articles)} 篇相关文章")
            return articles
            
        except Exception as e:
            print(f"RSS解析错误: {e}")
            return []
    
    def search_pubmed_simple(self, journals: List[str], year: int = 2025) -> List[Dict]:
        """
        简化的PubMed搜索 - 一次性搜索多个期刊
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        
        # 构建期刊列表查询
        journal_query = ' OR '.join([f'"{j}"[Journal]' for j in journals])
        
        query = f'({journal_query}) AND (machine learning OR deep learning OR artificial intelligence) AND (medical OR clinical OR diagnosis) AND {year}[PDAT]'
        
        print(f"正在PubMed搜索所有期刊...")
        
        try:
            # 搜索
            search_url = f"{base_url}esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': 200,  # 增加到200篇
                'retmode': 'json',
                'sort': 'pub_date',
                'mindate': f'{year}/01/01',
                'maxdate': f'{year}/12/31'
            }
            
            response = requests.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            search_data = response.json()
            
            id_list = search_data.get('esearchresult', {}).get('idlist', [])
            print(f"找到 {len(id_list)} 篇文章")
            
            if not id_list:
                return []
            
            # 获取详情
            time.sleep(0.5)
            summary_url = f"{base_url}esummary.fcgi"
            summary_params = {
                'db': 'pubmed',
                'id': ','.join(id_list),
                'retmode': 'json'
            }
            
            response = requests.get(summary_url, params=summary_params, timeout=30)
            response.raise_for_status()
            summary_data = response.json()
            
            articles = []
            for pmid, article_data in summary_data.get('result', {}).items():
                if pmid == 'uids':
                    continue
                
                authors = article_data.get('authors', [])
                author_list = ', '.join([a.get('name', '') for a in authors[:5]])
                
                article = {
                    'pmid': pmid,
                    'title': article_data.get('title', ''),
                    'authors': author_list,
                    'journal': article_data.get('fulljournalname', ''),
                    'pub_date': article_data.get('pubdate', ''),
                    'doi': article_data.get('elocationid', ''),
                    'link': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"PubMed搜索错误: {e}")
            return []
    
    def scrape_all_simple(self):
        """
        简化版爬取 - 使用最直接的方法
        """
        print("=" * 70)
        print("开始爬取2025年顶刊医学机器学习相关文章 (简化版)")
        print("=" * 70)
        
        # Nature系列RSS源
        nature_feeds = {
            'Nature': 'http://feeds.nature.com/nature/rss/current',
            'Nature Medicine': 'http://feeds.nature.com/nm/rss/current',
            'Nature Biotechnology': 'http://feeds.nature.com/nbt/rss/current',
            'Nature Methods': 'http://feeds.nature.com/nmeth/rss/current',
            'Nature Machine Intelligence': 'http://feeds.nature.com/natmachintell/rss/current',
        }
        
        # Science系列RSS源
        science_feeds = {
            'Science': 'https://www.science.org/rss/news_current.xml',
            'Science Translational Medicine': 'https://www.science.org/rss/stm_current.xml',
        }
        
        print("\n--- 方法1: RSS订阅源 (最快) ---")
        # 爬取Nature系列
        for journal, rss_url in nature_feeds.items():
            articles = self.scrape_nature_rss(journal, rss_url)
            self.results.extend(articles)
            time.sleep(1)
        
        # 爬取Science系列
        for journal, rss_url in science_feeds.items():
            articles = self.scrape_science_rss(journal, rss_url)
            self.results.extend(articles)
            time.sleep(1)
        
        print("\n--- 方法2: PubMed统一搜索 ---")
        all_journals = [
            'Nature', 'Nature Medicine', 'Nature Biotechnology', 'Nature Methods',
            'Science', 'Science Translational Medicine',
            'Cell', 'Cell Systems', 'Cell Reports Medicine'
        ]
        
        pubmed_articles = self.search_pubmed_simple(all_journals, 2025)
        self.results.extend(pubmed_articles)
        
        # 去重
        unique_results = []
        seen_titles = set()
        for article in self.results:
            title = article.get('title', '').lower()
            if title and title not in seen_titles and len(title) > 10:
                seen_titles.add(title)
                unique_results.append(article)
        
        self.results = unique_results
        print(f"\n✓ 总共找到 {len(self.results)} 篇独特文章")
    
    def save_results(self, filename: str = 'medical_ml_articles_2025.csv'):
        """保存结果"""
        if not self.results:
            print("没有结果可保存")
            return
        
        output_path = f'/mnt/user-data/outputs/{filename}'
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['title', 'authors', 'journal', 'pub_date', 'doi', 'pmid', 'link', 'summary']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for article in self.results:
                writer.writerow(article)
        
        print(f"\n✓ CSV结果已保存到: {output_path}")
        
        # JSON格式
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ JSON结果已保存到: {json_path}")
        
        return output_path
    
    def generate_report(self):
        """生成统计报告"""
        if not self.results:
            return
        
        print("\n" + "=" * 70)
        print("统计报告")
        print("=" * 70)
        
        # 按期刊统计
        journal_count = {}
        for article in self.results:
            journal = article.get('journal', 'Unknown')
            journal_count[journal] = journal_count.get(journal, 0) + 1
        
        print("\n各期刊文章数量:")
        for journal, count in sorted(journal_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {journal}: {count} 篇")
        
        # 显示最新的10篇
        print("\n" + "=" * 70)
        print("最新10篇文章预览:")
        print("=" * 70)
        
        for i, article in enumerate(self.results[:10], 1):
            print(f"\n{i}. {article.get('title', 'N/A')}")
            print(f"   📚 期刊: {article.get('journal', 'N/A')}")
            print(f"   ✍️  作者: {article.get('authors', 'N/A')[:80]}...")
            print(f"   📅 日期: {article.get('pub_date', 'N/A')}")
            print(f"   🔗 链接: {article.get('link', 'N/A')}")

def main():
    scraper = SubscriptionScraper()
    scraper.scrape_all_simple()
    scraper.save_results()
    scraper.generate_report()

if __name__ == "__main__":
    main()
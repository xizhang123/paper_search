import requests
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.parse import quote

# KMP算法实现
def kmp_search(text, pattern):
    if not text or not pattern:
        return -1
    
    # 计算部分匹配表
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    def is_boundary(text, pos):
        return pos < 0 or pos >= len(text) or text[pos].isspace() or text[pos] in ['2','\'','.','!']
    
    lps = compute_lps(pattern)
    i = j = 0
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == len(pattern):
                match_start = i - j
                match_end = i
                if is_boundary(text, match_start - 1) and is_boundary(text, match_end):
                    return match_start
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# 读取CCF.csv文件
def load_ccf_data():
    try:
        df = pd.read_csv('CCF.csv')
        abbr_list = []
        full_list = []
        
        for _, row in df.iterrows():
            abbr = row.get('刊物/会议简称', '')
            full_name = row.get('刊物/会议全称', '')
            rank = row.get('等级', '')
            venue_type = row.get('期刊/会议', '')
            
            if isinstance(abbr, str) and abbr.strip():
                abbr_list.append((abbr.strip(), (rank, venue_type, abbr.strip())))
            if isinstance(full_name, str) and full_name.strip():
                full_list.append((full_name.strip(), (rank, venue_type, full_name.strip())))
        
        abbr_list.sort(key=lambda x: len(x[0]), reverse=True)
        full_list.sort(key=lambda x: len(x[0]), reverse=True)
        
        return dict(abbr_list), dict(full_list)
    except Exception as e:
        print(f"读取CCF.csv时出错: {e}")
        return {}, {}

# 获取文章的发表信息
def get_venue_info(venue_text, abbr_dict, full_dict):
    venue_info = ('未收录', '', '')
    matched_venue = None
    
    if venue_text:
        venue_text_clean = venue_text.replace('\n', ' ')
        venue_text_clean = venue_text_clean.replace('  ', ' ')
        venue_text_clean = venue_text_clean.replace('  ', ' ')
        venue_text_clean = venue_text_clean.replace('  ', ' ')
        
        for abbr, info in abbr_dict.items():
            if kmp_search(venue_text_clean, abbr) != -1:
                venue_info = info
                matched_venue = abbr
                break
        
        if venue_info[0] == '未收录':
            for full_name, info in full_dict.items():
                if kmp_search(venue_text_clean, full_name) != -1:
                    venue_info = info
                    matched_venue = full_name
                    break
    
    return venue_text_clean if venue_text else None, matched_venue, venue_info

def search_papers(queries, max_results=1):
    all_hits = set()
    
    for query in queries:
        base_url = "https://dblp.org/search/publ/api"
        encoded_query = quote(query)
        url = f"{base_url}?q={encoded_query}&format=xml&h={max_results}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            hits = root.findall('.//hit')
            all_hits.update(hits)
        except Exception as e:
            print(f"DBLP API查询出错: {e}")
    
    # 加载CCF数据
    abbr_dict, full_dict = load_ccf_data()
    
    # 准备存储数据的列表
    paper_data = []
    
    # 处理搜索结果
    for hit in all_hits:
        info = hit.find('.//info')
        if info is not None:
            title = info.find('.//title')
            year = info.find('.//year')
            venue = info.find('.//venue')
            url = info.find('.//ee')
            
            venue_text = venue.text if venue is not None and venue.text else ""
            venue_text, matched_venue, venue_info = get_venue_info(venue_text, abbr_dict, full_dict)
            ccf_level, venue_type, original_name = venue_info
            
            paper_info = {
                "时间": f"{year.text if year is not None else '未知'}年",
                "下载链接": url.text if url is not None else "",
                "标题": title.text if title is not None else "",
                "类型": venue_type if venue_type else "",
                "CCF等级": ccf_level,
                "匹配会议/期刊": original_name if matched_venue else "",
                "原始文本": venue_text if venue_text else ""
            }
            paper_data.append(paper_info)
    
    # 保存为CSV
    df = pd.DataFrame(paper_data)
    df.to_csv("dblp_papers.csv", index=False, encoding="utf-8-sig", quoting=1)
    
    return len(paper_data)
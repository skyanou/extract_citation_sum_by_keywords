import re
import os

def search_articles(file_path, keywords, rule='or'):
    """
    Reads the file, parses article structure (extracting Journal separately), 
    and searches based on keywords.
    """
    
    # 1. Input Validation
    if isinstance(keywords, str):
        keywords = [keywords]
    
    rule = rule.lower()
    if rule not in ['and', 'or']:
        print("Error: Rule must be 'and' or 'or'.")
        return

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # 2. Parse the File
    articles = []
    current_block = []
    # Regex: Matches start of line, digits (citations), space, 4 digits (year)
    citation_pattern = re.compile(r'^(\d+)\s+(\d{4})$')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = citation_pattern.match(line)
        if match:
            # Found the citation/year line -> End of current article
            citations = int(match.group(1))
            year = int(match.group(2))
            
            # --- 核心修改逻辑开始 ---
            # 假设 current_block 的最后一行是 Journal，前面的是 Title/Authors
            if current_block:
                journal = current_block[-1]  # 提取最后一行作为期刊
                content_lines = current_block[:-1] # 剩余部分作为内容
            else:
                journal = "Unknown Journal"
                content_lines = []

            full_text = " ".join(content_lines)
            # --- 核心修改逻辑结束 ---
            
            articles.append({
                'text': full_text,
                'journal': journal,  # 存储期刊信息
                'citations': citations,
                'year': year
            })
            current_block = [] # Reset buffer
        else:
            # Still reading title/authors/journal
            current_block.append(line)

    # 3. Search Logic
    print(f"\nSearch Config | Keywords: {keywords} | Rule: '{rule.upper()}'")
    print("="*80)
    
    found_articles = []
    total_citations = 0
    
    for article in articles:
        # 搜索范围：通常搜索 text 即可，也可以选择是否搜索 journal 字段
        # 这里为了保险，我们将 text 和 journal 拼在一起进行关键词匹配
        search_target = (article['text'] + " " + article['journal']).lower()
        
        if rule == 'and':
            is_match = all(k.lower() in search_target for k in keywords)
        else: # rule == 'or'
            is_match = any(k.lower() in search_target for k in keywords)
            
        if is_match:
            found_articles.append(article)
            total_citations += article['citations']

    # 4. Display Results
    if found_articles:
        for idx, item in enumerate(found_articles, 1):
            # 修改展示格式，加入 Journal
            print(f"[{idx}] Citations: {item['citations']} | Year: {item['year']} | Journal: {item['journal']}")
            print(f"    Content: {item['text'][:100]}...") # 这里的切片是为了防止显示太长
            print("-" * 40)
        
        print(f"\n{'='*80}")
        print(f"Summary:")
        print(f"  - Keywords: {keywords}")
        print(f"  - Logic: {rule.upper()}")
        print(f"  - Articles Found: {len(found_articles)}")
        print(f"  - Total Citations: {total_citations}")
        print(f"{'='*80}\n")
    else:
        print(f"No articles found matching criteria.")
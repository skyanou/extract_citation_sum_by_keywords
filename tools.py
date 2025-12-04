import re
import os

def search_articles(file_path, keywords, rule='or'):
    """
    Reads the file, parses article structure, and searches based on keywords and logic rules.
    
    Parameters:
    - file_path (str): Path to the .txt file.
    - keywords (str or list): One keyword or a list of keywords to search for.
    - rule (str): 'and' (all must match) or 'or' (any can match). Default is 'or'.
    """
    
    # 1. Input Validation & Standardization
    # If user passes a single string, convert it to a list for consistent processing
    if isinstance(keywords, str):
        keywords = [keywords]
    
    # Ensure rule is lowercase
    rule = rule.lower()
    if rule not in ['and', 'or']:
        print("Error: Rule must be 'and' or 'or'.")
        return

    # Check if file exists
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
            
            # Join cached lines to form full text
            full_text = " ".join(current_block)
            
            articles.append({
                'text': full_text,
                'citations': citations,
                'year': year
            })
            current_block = [] # Reset buffer
        else:
            # Still reading title/authors
            current_block.append(line)

    # 3. Search Logic
    print(f"\nSearch Config | Keywords: {keywords} | Rule: '{rule.upper()}'")
    print("="*60)
    
    found_articles = []
    total_citations = 0
    
    for article in articles:
        text_lower = article['text'].lower()
        
        # Check matches based on the rule
        if rule == 'and':
            # ALL keywords must be present
            is_match = all(k.lower() in text_lower for k in keywords)
        else: # rule == 'or'
            # ANY keyword must be present
            is_match = any(k.lower() in text_lower for k in keywords)
            
        if is_match:
            found_articles.append(article)
            total_citations += article['citations']

    # 4. Display Results
    if found_articles:
        for idx, item in enumerate(found_articles, 1):
            print(f"[{idx}] Citations: {item['citations']} | Year: {item['year']}")
            print(f"    Content: {item['text'][:150]}...") # Truncate for cleaner view
            print("-" * 30)
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  - Keywords: {keywords}")
        print(f"  - Logic: {rule.upper()}")
        print(f"  - Articles Found: {len(found_articles)}")
        print(f"  - Total Citations: {total_citations}")
        print(f"{'='*60}\n")
    else:
        print(f"No articles found matching criteria.")
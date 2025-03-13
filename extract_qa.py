import requests
from bs4 import BeautifulSoup
import csv
import os

# URLs for different chapters
urls = {
    "3rd Standard Chapter 1 - Term1- My Body": "https://samacheer-kalvi.com/samacheer-kalvi-3rd-standard-science-guide-term-1-chapter-1/",
    "3rd Standard Chapter 2 - Term1- Plants": "https://samacheer-kalvi.com/samacheer-kalvi-3rd-standard-science-guide-term-1-chapter-2/",
    "3rd Standard Chapter 3 - Term1- Birds": "https://samacheer-kalvi.com/samacheer-kalvi-3rd-standard-science-guide-term-1-chapter-3/",
    "3rd Standard Chapter 4 - Term1- Water": "https://samacheer-kalvi.com/samacheer-kalvi-3rd-standard-science-guide-term-1-chapter-4/"
}

def extract_qa(url):
    try:
        # Send request with headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all question and answer elements
        qa_pairs = []
        
        # Look for questions in different heading tags and strong tags
        questions = soup.find_all(['h2', 'h3', 'h4', 'strong'])
        
        for q in questions:
            question_text = q.get_text().strip()
            # Skip if not a question
            if not any(keyword in question_text.lower() for keyword in ['question', 'mcq', 'choose', 'fill', 'match', 'answer']):
                continue
                
            # Get the answer - usually in the next sibling or paragraph
            answer = ""
            next_elem = q.find_next(['p', 'div', 'ul', 'ol'])
            if next_elem:
                answer = next_elem.get_text().strip()
            
            if question_text and answer:
                qa_pairs.append([question_text, answer])
        
        return qa_pairs
        
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return []

def save_to_csv(qa_pairs, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Answer'])
        writer.writerows(qa_pairs)

def main():
    for chapter_name, url in urls.items():
        print(f"Processing {chapter_name}...")
        qa_pairs = extract_qa(url)
        
        if qa_pairs:
            filename = f"{chapter_name}.csv"
            save_to_csv(qa_pairs, filename)
            print(f"Saved {len(qa_pairs)} Q&A pairs to {filename}")
        else:
            print(f"No Q&A pairs found for {chapter_name}")

if __name__ == "__main__":
    main()

# Simplified Search Engine — Based on Section 23.6 of the Textbook

## 1. Project Overview
This project implements a simplified search engine exactly following the guidelines provided in Section 23.6 (Subsection: Search Engine) of the course textbook. It processes a small set of local HTML pages, crawls internal links, extracts text, builds an inverted index, and ranks pages based on TF-IDF + hyperlink influence.

The system supports interactive search queries and returns documents sorted by relevance.

---

## 2. Features Implemented
- Web Crawler (BFS Frontier-Based)
- HTML Parsing with BeautifulSoup
- Stop-Word Removal
- Tokenization + Normalization
- Trie-Based Term Index
- Inverted Index
- TF-IDF Ranking (Advanced)
- Simple Ranking (Optional)
- Hyperlink-Based Boost
- Handles 6+ Large Web Pages (NYTimes, Portland, Stevens pages)
- Boundary Condition Handling

---

## 3. Directory Structure

```
SearchEngineProject/
│
├── search_engine.py
├── README.md
├── output.txt
├── sample_output.txt
├── boundary_tests.txt
│
└── webpages/
      ├── python.html
      ├── java.html
      ├── cpp.html
      ├── programming_basics.html
      ├── data_structures.html
      ├── web_development.html
      ├── The New York Times - Breaking News...
      ├── Visit Portland Maine...
      ├── Stevens Institute of Technology - Master of Science in Cybersecurity.html
      ├── Cybersecurity Bachelor's Degree - Stevens Institute of Technology.html
      ├── New Graduate Students - Stevens Institute of Technology.html
      └── ... (other pages)
```

---

## 4. Mapping to Section 23.6 of Textbook

| Section | Requirement | Implementation |
|--------|-------------|----------------|
| 23.6.1 | Web crawling with frontier | BFS crawler with queue + visited set |
| 23.6.2 | Parsing HTML | BeautifulSoup parser |
| 23.6.3 | Tokenization | Regex extraction, lowercasing |
| 23.6.4 | Stop word removal | Built-in STOP_WORDS set |
| 23.6.5 | Indexing | Trie + inverted index |
| 23.6.6 | Ranking | TF-IDF + hyperlink scoring |
| 23.6.7 | Query processing | Multi-term search + intersection |
| 23.6.8 | Result ranking | Scores sorted descending |

---

## 5. Algorithms & Data Structures Used

### 5.1 Web Crawling Algorithm (BFS)
The crawler:
1. Reads all `.html` files in the `webpages/` directory.
2. Uses a queue as the crawl frontier.
3. Extracts visible text, page titles, and internal `.html` links.
4. Follows only internal links.
5. Uses a visited set to avoid cycles.

---

### 5.2 Tokenization
- Lowercase conversion  
- Regex extraction  
- Removal of stop-words  

---

### 5.3 Inverted Index
A hash-map of hash-maps:
```
{
  "python": { "python.html": 4, "programming_basics.html": 2 }
}
```

---

### 5.4 Trie Structure
Efficient prefix-based storage supporting fast word lookup.

---

### 5.5 Ranking Algorithm — TF-IDF + Hyperlink Bonus
```
TF = frequency of term in document / total words in document
IDF = log((1 + N) / (1 + df)) + 1
Score = TF * IDF + 0.1 * incoming_links
```

---

## 6. Search Process
1. Process query  
2. Tokenize and remove stop-words  
3. Trie lookup  
4. Intersect document sets  
5. Compute ranking score  
6. Sort results  
7. Display  

---

## 7. Sample Output
See `output.txt` for full run.

---

## 8. Boundary Testing
See `boundary_tests.txt`.

---

## 9. How to Run
```
pip install beautifulsoup4
python search_engine.py
```

---

## 10. Conclusion
This project fully implements the simplified search engine described in Section 23.6, including crawling, indexing, TF-IDF ranking, hyperlink boosts, and multi-term search.

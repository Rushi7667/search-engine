import os
import re
import math
from collections import defaultdict, Counter, deque
from bs4 import BeautifulSoup

# STOP WORD LIST (Section 23.6.4 Recommendation)

STOP_WORDS = {
    'a','an','the','and','or','but','in','on','at','to','for','with','by','of',
    'is','was','were','am','are','be','been','being','have','has','had','do',
    'does','did','will','would','shall','should','may','might','must','can',
    'could','i','you','he','she','it','we','they','them','their','his','her',
    'its','our','your','my','mine','yours','ours','this','that','these','those',
    'from','as','if','then','else','when','where','why','how','all','any','both',
    'each','few','more','most','some','such','up','down','over','under','again',
    'further','off','out','into','onto','about','between','during','before',
    'after','above','below','through','while','against','nor','only','own',
    'same','too','very','also'
}

# Trie Data Structure (Section 23.6.5)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.occurrence_index = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, occ_idx):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.occurrence_index = occ_idx

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.occurrence_index


#  BFS Web Crawler (Section 23.6.1)

class WebCrawler:
    def __init__(self, directory):
        self.dir = directory
        self.pages = {}
        self.links = defaultdict(list)

    def extract(self, html, filename):
        soup = BeautifulSoup(html, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Title extraction
        title = soup.title.string.strip() if soup.title else filename

        # Visible text only
        text = soup.get_text(separator=" ").lower()
        words = re.findall(r"[a-zA-Z]+", text)
        words = [w for w in words if w not in STOP_WORDS]

        # Internal links only (local files)
        link_list = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".html"):
                link_list.append(href)

        return title, words, link_list

    def crawl(self):
        queue = deque()
        visited = set()

        all_files = [f for f in os.listdir(self.dir) if f.endswith(".html")]

        for file in all_files:
            queue.append(file)

        while queue:
            file = queue.popleft()
            if file in visited:
                continue
            visited.add(file)

            path = os.path.join(self.dir, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    html = f.read()
            except:
                continue  # ignore unreadable files

            title, words, outgoing = self.extract(html, file)
            self.pages[file] = {
                "title": title,
                "words": words
            }

            for link in outgoing:
                self.links[file].append(link)
                if link not in visited and link in all_files:
                    queue.append(link)

        print(f"Crawled {len(self.pages)} pages.")


#  Search Engine Core

class SearchEngine:
    def __init__(self, directory, ranking_mode="tf-idf"):
        self.dir = directory
        self.ranking_mode = ranking_mode

        self.crawler = WebCrawler(directory)
        self.trie = Trie()

        self.inverted_index = []
        self.word_to_index = {}
        self.document_lengths = {}
        self.incoming_links = defaultdict(int)

    # Index Building (Section 23.6.3 - 23.6.6)
    def build_index(self):
        self.crawler.crawl()

        # Count incoming links
        for src, outs in self.crawler.links.items():
            for dest in outs:
                self.incoming_links[dest] += 1

        # Build inverted index
        for file, data in self.crawler.pages.items():
            word_freq = Counter(data["words"])
            self.document_lengths[file] = sum(word_freq.values())

            for word, freq in word_freq.items():
                if word not in self.word_to_index:
                    self.word_to_index[word] = len(self.inverted_index)
                    self.inverted_index.append(defaultdict(int))

                idx = self.word_to_index[word]
                self.inverted_index[idx][file] = freq

        # Insert into Trie
        for word, idx in self.word_to_index.items():
            self.trie.insert(word, idx)

        print(f"Indexed {len(self.word_to_index)} unique terms.")

    # TF-IDF Calculation
    def compute_score(self, word, doc, freq, N, df):
        if self.ranking_mode == "simple":
            return freq  # simple frequency ranking

        # TF-IDF mode
        tf = freq / self.document_lengths[doc]
        idf = math.log((1 + N) / (1 + df)) + 1
        return tf * idf

    # Search Function (Section 23.6.7)
    def search(self, query):
        terms = re.findall(r"[a-zA-Z]+", query.lower())
        terms = [t for t in terms if t not in STOP_WORDS]

        if not terms:
            return []

        doc_sets = []
        for t in terms:
            idx = self.trie.search(t)
            if idx is None:
                return []
            doc_sets.append(set(self.inverted_index[idx].keys()))

        # Intersection (documents that contain all terms)
        matching_docs = set.intersection(*doc_sets)
        if not matching_docs:
            return []

        # Ranking
        scores = {}
        N = len(self.crawler.pages)

        for doc in matching_docs:
            total_score = 0
            for t in terms:
                idx = self.trie.search(t)
                occurrences = self.inverted_index[idx]
                df = len(occurrences)
                freq = occurrences[doc]
                total_score += self.compute_score(t, doc, freq, N, df)

            # Hyperlink Bonus
            total_score += 0.1 * self.incoming_links[doc]
            scores[doc] = total_score

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# MAIN EXECUTION

if __name__ == "__main__":
    engine = SearchEngine("webpages/", ranking_mode="tf-idf")
    engine.build_index()

    print("\nEnter a search query (type 'q' to quit)\n")

    while True:
        query = input("> ")
        if query.lower() == "q":
            break

        results = engine.search(query)
        if not results:
            print("No results found.\n")
            continue

        print(f"\nFound {len(results)} result(s):")
        for doc, score in results:
            title = engine.crawler.pages[doc]["title"]
            print(f"{title} ({doc}) - Score: {score:.4f}")
        print()
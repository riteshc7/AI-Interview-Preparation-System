import re
from typing import List, Tuple


def extract_keywords(text: str) -> List[str]:
    text_lower = text.lower()
    
    words = re.findall(r'\b[a-z]{3,}\b', text_lower)
    
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
        'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
        'its', 'may', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did',
        'own', 'say', 'she', 'too', 'use', 'your', 'each', 'make', 'like',
        'this', 'that', 'than', 'them', 'then', 'when', 'with', 'have', 'from',
        'they', 'will', 'would', 'there', 'their', 'what', 'about', 'which',
        'when', 'where', 'been', 'very', 'also', 'more', 'into', 'some', 'could'
    }
    
    keywords = [w for w in words if w not in stop_words]
    
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, _ in sorted_keywords[:20]]


def calculate_similarity(text1: str, text2: str) -> float:
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    return len(intersection) / len(union) if union else 0.0


def analyze_sentiment(text: str) -> Tuple[str, float]:
    positive_words = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'love', 'best', 'perfect', 'awesome', 'beautiful', 'outstanding'
    }
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'poor', 'hate',
        'disappointing', 'failure', 'wrong', 'difficult', 'problem'
    }
    
    text_lower = text.lower()
    words = set(re.findall(r'\b[a-z]+\b', text_lower))
    
    pos_count = len(words.intersection(positive_words))
    neg_count = len(words.intersection(negative_words))
    
    if pos_count > neg_count:
        return 'positive', (pos_count - neg_count) / max(len(words), 1) * 100
    elif neg_count > pos_count:
        return 'negative', (neg_count - pos_count) / max(len(words), 1) * 100
    else:
        return 'neutral', 50.0


def extract_entities(text: str) -> List[dict]:
    import re
    
    tech_patterns = [
        (r'\b(Python|Java|JavaScript|TypeScript|C\+\+|Ruby|Go|Rust|Swift|Kotlin)\b', 'Language'),
        (r'\b(React|Angular|Vue|Django|Flask|Spring|Rails|Laravel)\b', 'Framework'),
        (r'\b(PostgreSQL|MySQL|MongoDB|Redis|Elasticsearch)\b', 'Database'),
        (r'\b(AWS|Azure|GCP|Docker|Kubernetes)\b', 'Technology'),
    ]
    
    entities = []
    for pattern, label in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({'text': match, 'label': label})
    
    return entities


def calculate_readability_score(text: str) -> float:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.0
    
    words = text.split()
    avg_sentence_length = len(words) / len(sentences)
    
    syllables = sum(count_syllables(word) for word in words)
    avg_syllables_per_word = syllables / max(len(words), 1)
    
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    return max(0, min(100, score))


def count_syllables(word: str) -> int:
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    
    return count

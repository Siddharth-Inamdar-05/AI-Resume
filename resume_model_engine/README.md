# AI Resume Screening and Skill Matching Engine

A production-ready **core NLP model** for intelligent resume screening and candidate ranking. This is a **model-only** implementation with no frontend or backend API—designed to be imported and integrated into your backend services.

## 🎯 Features

- **Text Cleaning**: Normalize and preprocess resume/JD text
- **Skill Extraction**: Extract 200+ technical and soft skills with synonym support
- **Contact Extraction**: Regex-based extraction of emails, phones, GitHub, LinkedIn
- **NER Extraction**: spaCy-based entity recognition (Person, Organization, Location, Date)
- **Semantic Similarity**: TF-IDF cosine similarity between JD and resumes
- **Weighted Scoring**: Configurable skill match + semantic similarity scoring
- **Candidate Ranking**: Automated ranking with rule-based reasoning

## 📁 Project Structure

```
resume_model_engine/
│
├── data/
│   └── skills.csv              # 200+ skills dataset
│
├── src/
│   ├── __init__.py
│   ├── cleaner.py              # Text preprocessing
│   ├── skill_extractor.py      # Skill matching with synonyms
│   ├── regex_extractor.py      # Contact info extraction
│   ├── ner_extractor.py        # Named Entity Recognition
│   ├── similarity.py           # TF-IDF similarity computation
│   ├── scorer.py               # Scoring logic
│   ├── ranker.py               # Ranking and reason generation
│   └── pipeline.py             # Main orchestration pipeline
│
├── tests/
│   └── test_pipeline.py        # Test suite
│
├── demo_run.py                 # Runnable demo
├── requirements.txt
└── README.md
```

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## 📖 Usage

### Running the Demo

```bash
python demo_run.py
```

This will process 3 sample resumes against a sample job description and display ranked results.

### Importing in Your Backend

```python
from src.pipeline import evaluate_candidates

# Job description text
jd_text = """
Senior ML Engineer
Required: Python, TensorFlow, AWS, Docker
...
"""

# Dictionary of candidates {candidate_id: resume_text}
candidates = {
    "candidate_001": "John Doe... Python, TensorFlow...",
    "candidate_002": "Jane Smith... Java, Spring...",
}

# Run the pipeline
results = evaluate_candidates(jd_text, candidates)

# Results is a list of dicts, sorted by final_match_score (descending)
for candidate in results:
    print(f"{candidate['candidate_id']}: {candidate['final_match_score']}%")
    print(f"Reason: {candidate['short_reason']}")
```

### Custom Scoring Weights

```python
# Use 60% skill matching, 40% semantic similarity
results = evaluate_candidates(
    jd_text, 
    candidates,
    skill_weight=0.60,
    semantic_weight=0.40
)
```

## 📊 Output Format

Each candidate result contains:

```python
{
    "candidate_id": str,
    "emails": List[str],
    "phones": List[str],
    "github": List[str],
    "linkedin": List[str],
    "extracted_skills": List[str],
    "matched_skills": List[str],
    "missing_skills": List[str],
    "skill_match_score": float,           # 0-100
    "semantic_similarity_score": float,   # 0-100
    "final_match_score": float,           # 0-100
    "ner_entities": {
        "PERSON": List[str],
        "ORG": List[str],
        "GPE": List[str],
        "DATE": List[str]
    },
    "short_reason": str                   # 2-3 line assessment
}
```

## 🧪 Running Tests

```bash
python tests/test_pipeline.py
```

## 🔧 Module Descriptions

| Module | Purpose |
|--------|---------|
| `cleaner.py` | Text normalization (lowercase, whitespace removal, preserve contractions) |
| `skill_extractor.py` | Load skills from CSV, match using regex with synonyms (e.g., PyTorch/Torch) |
| `regex_extractor.py` | Extract emails, phone numbers, GitHub, LinkedIn URLs |
| `ner_extractor.py` | spaCy NER for Person, Organization, Location, Date entities |
| `similarity.py` | TF-IDF vectorization + cosine similarity (0-100 scale) |
| `scorer.py` | Skill match percentage and weighted final score calculation |
| `ranker.py` | Sort candidates by score and generate rule-based reasons |
| `pipeline.py` | Main orchestration: processes JD + resumes, returns ranked results |

## 🎓 Skill Synonym Support

The engine supports common skill aliases:

- `pytorch` → `torch`
- `c++` → `cpp`, `cplusplus`
- `machine learning` → `ml`
- `natural language processing` → `nlp`
- `aws` → `amazon web services`
- And many more...

Add custom synonyms in `src/skill_extractor.py` → `SKILL_SYNONYMS` dictionary.

## 🔮 Future Extensions

### SBERT Integration

To add semantic embeddings using Sentence-BERT:

1. Install: `pip install sentence-transformers`
2. Update `src/similarity.py` → `compute_sbert_similarity()`
3. Use in pipeline instead of TF-IDF

### Advanced NER

Replace spaCy with transformer-based NER for better accuracy:
- Install: `pip install transformers`
- Use models like `dslim/bert-base-NER`

### Custom Skill Lists

Replace `data/skills.csv` with domain-specific skills:
- Healthcare: medical procedures, certifications
- Finance: risk modeling, compliance frameworks
- Legal: practice areas, jurisdictions

## 📋 Requirements

- Python 3.8+
- spacy 3.7.2
- scikit-learn 1.4.0
- pandas 2.2.0

## 🤝 Integration Example

### FastAPI Backend

```python
from fastapi import FastAPI
from src.pipeline import evaluate_candidates

app = FastAPI()

@app.post("/screen-resumes")
def screen_resumes(jd: str, resumes: dict):
    results = evaluate_candidates(jd, resumes)
    return {"candidates": results}
```

### Flask Backend

```python
from flask import Flask, request, jsonify
from src.pipeline import evaluate_candidates

app = Flask(__name__)

@app.route('/api/screen', methods=['POST'])
def screen():
    data = request.json
    results = evaluate_candidates(data['jd'], data['resumes'])
    return jsonify(results)
```

## 📝 License

This project is open-source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ for intelligent recruitment automation.

---

**Note**: This is a core model engine only. No UI or API endpoints are included. Import the pipeline into your backend services for production use.

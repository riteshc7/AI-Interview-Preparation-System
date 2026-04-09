import random
from typing import List
from ..models.schemas import QuestionItem, QuestionGenerateRequest


QUESTION_BANKS = {
    "backend developer": {
        "technical": [
            {
                "question": "Explain the difference between SQL and NoSQL databases. When would you choose one over the other?",
                "keywords": ["sql", "nosql", "relational", "schema", "scalability", "transactions", "acid", "eventual consistency"],
                "difficulty": "medium"
            },
            {
                "question": "What is REST API? Describe its principles and constraints.",
                "keywords": ["rest", "api", "http", "stateless", "resources", "verbs", "get", "post", "put", "delete", "crud"],
                "difficulty": "easy"
            },
            {
                "question": "How would you optimize a slow database query? Discuss indexing strategies and query optimization techniques.",
                "keywords": ["index", "explain", "query", "join", "cache", "optimize", "profiling", "partitioning"],
                "difficulty": "medium"
            },
            {
                "question": "Explain the concept of microservices architecture. What are its advantages and disadvantages compared to monolithic architecture?",
                "keywords": ["microservices", "monolith", "api", "deployment", "scaling", "independence", "distributed", "service mesh"],
                "difficulty": "hard"
            },
            {
                "question": "What is the ACID property in database transactions? Why is it important?",
                "keywords": ["atomicity", "consistency", "isolation", "durability", "transaction", "rollback", "commit"],
                "difficulty": "medium"
            },
            {
                "question": "Describe how you would implement authentication and authorization in a web application.",
                "keywords": ["jwt", "oauth", "session", "token", "bcrypt", "hash", "salt", "refresh token", "access control"],
                "difficulty": "medium"
            },
            {
                "question": "What is Docker and how does it help in deployment? Explain containerization benefits.",
                "keywords": ["docker", "container", "image", "dockerfile", "kubernetes", "orchestration", "microservices"],
                "difficulty": "medium"
            },
            {
                "question": "Explain the concept of caching. What caching strategies would you implement for a web application?",
                "keywords": ["cache", "redis", "memcached", "invalidation", "ttl", "lru", "write-through", "read-through"],
                "difficulty": "medium"
            },
            {
                "question": "What are the differences between synchronous and asynchronous programming? When would you use each?",
                "keywords": ["async", "sync", "threading", "multiprocessing", "coroutine", "callback", "event loop", "concurrency"],
                "difficulty": "medium"
            },
            {
                "question": "Explain CI/CD pipeline concepts and their importance in modern software development.",
                "keywords": ["ci", "cd", "pipeline", "automation", "testing", "deployment", "jenkins", "github actions"],
                "difficulty": "easy"
            },
            {
                "question": "What is database indexing and how does it improve query performance?",
                "keywords": ["index", "b-tree", "hash index", "composite index", "query optimization", "performance"],
                "difficulty": "medium"
            },
            {
                "question": "Describe the CAP theorem and its implications for distributed systems.",
                "keywords": ["cap", "consistency", "availability", "partition tolerance", "distributed", "tradeoff"],
                "difficulty": "hard"
            },
        ],
        "behavioral": [
            {
                "question": "Describe a challenging technical problem you faced and how you solved it.",
                "keywords": ["problem solving", "approach", "solution", "learning", "teamwork"],
                "difficulty": "medium"
            },
            {
                "question": "How do you stay updated with the latest technology trends and continue learning?",
                "keywords": ["learning", "growth", "technology", "courses", "community", "documentation"],
                "difficulty": "easy"
            },
            {
                "question": "Tell me about a time when you had to work with a difficult team member. How did you handle it?",
                "keywords": ["teamwork", "communication", "conflict resolution", "empathy", "collaboration"],
                "difficulty": "medium"
            },
            {
                "question": "Describe your experience with code reviews. What do you look for when reviewing others' code?",
                "keywords": ["code review", "best practices", "quality", "feedback", "collaboration"],
                "difficulty": "easy"
            },
        ]
    },
    "frontend developer": {
        "technical": [
            {
                "question": "What is the difference between let, const, and var in JavaScript? Explain hoisting behavior.",
                "keywords": ["var", "let", "const", "scope", "hoisting", "temporal dead zone", "block scope", "function scope"],
                "difficulty": "easy"
            },
            {
                "question": "Explain the React component lifecycle. How have lifecycle methods evolved with React hooks?",
                "keywords": ["mounting", "updating", "unmounting", "useeffect", "componentdidmount", "componentwillunmount", "state", "props"],
                "difficulty": "medium"
            },
            {
                "question": "How does the virtual DOM work in React? Why is it more efficient than direct DOM manipulation?",
                "keywords": ["virtual", "dom", "reconciliation", "diffing", "performance", "batching", "fiber"],
                "difficulty": "medium"
            },
            {
                "question": "What are closures in JavaScript? Provide a practical use case.",
                "keywords": ["closure", "scope", "function", "lexical", "encapsulation", "private variables", "currying"],
                "difficulty": "hard"
            },
            {
                "question": "Describe the difference between CSS Grid and Flexbox. When would you use each?",
                "keywords": ["grid", "flexbox", "layout", "one-dimensional", "two-dimensional", "alignment", "distribution"],
                "difficulty": "medium"
            },
            {
                "question": "What is TypeScript and what advantages does it offer over plain JavaScript?",
                "keywords": ["typescript", "types", "interface", "compile", "safety", "autocomplete", "es6"],
                "difficulty": "easy"
            },
            {
                "question": "Explain the concept of state management in React. What are the options available?",
                "keywords": ["state", "redux", "context", "zustand", "recoil", "prop drilling", "global state"],
                "difficulty": "medium"
            },
            {
                "question": "What are Web Components? How do they differ from React/Vue components?",
                "keywords": ["web components", "custom elements", "shadow dom", "html templates", "encapsulation"],
                "difficulty": "hard"
            },
        ],
        "behavioral": [
            {
                "question": "How do you handle browser compatibility issues in your projects?",
                "keywords": ["browser", "compatibility", "testing", "progressive enhancement", "graceful degradation"],
                "difficulty": "medium"
            },
            {
                "question": "Describe your approach to optimizing web performance.",
                "keywords": ["performance", "optimization", "bundle size", "lazy loading", "caching", "core web vitals"],
                "difficulty": "medium"
            },
        ]
    },
    "data scientist": {
        "technical": [
            {
                "question": "What is the difference between supervised and unsupervised learning? Give examples of algorithms for each.",
                "keywords": ["supervised", "unsupervised", "labeled", "unlabeled", "regression", "classification", "clustering", "降维"],
                "difficulty": "easy"
            },
            {
                "question": "Explain the bias-variance tradeoff. How does it affect model performance?",
                "keywords": ["bias", "variance", "overfitting", "underfitting", "model complexity", "generalization", "regularization"],
                "difficulty": "medium"
            },
            {
                "question": "How would you handle missing data in a dataset? Discuss various imputation techniques.",
                "keywords": ["imputation", "deletion", "interpolation", "mean", "median", "mode", "knn", "regression imputation"],
                "difficulty": "medium"
            },
            {
                "question": "What is cross-validation and why is it important? Describe k-fold cross-validation.",
                "keywords": ["cross-validation", "k-fold", "training", "validation", "test set", "generalization", "overfitting"],
                "difficulty": "medium"
            },
            {
                "question": "Explain the difference between L1 and L2 regularization. When would you use each?",
                "keywords": ["l1", "l2", "regularization", "lasso", "ridge", "penalty", "sparsity", "norm"],
                "difficulty": "hard"
            },
            {
                "question": "What is the purpose of feature engineering? Give examples of common techniques.",
                "keywords": ["feature engineering", "scaling", "encoding", "polynomial", "binning", "feature selection"],
                "difficulty": "medium"
            },
            {
                "question": "Describe the random forest algorithm. How does it achieve better performance than single decision trees?",
                "keywords": ["random forest", "ensemble", "bagging", "decision tree", "feature importance", "overfitting"],
                "difficulty": "medium"
            },
        ],
        "behavioral": [
            {
                "question": "How do you communicate complex technical findings to non-technical stakeholders?",
                "keywords": ["communication", "storytelling", "visualization", "stakeholders", "insights"],
                "difficulty": "medium"
            },
            {
                "question": "Describe a data project where you had to make assumptions. How did you validate them?",
                "keywords": ["assumptions", "validation", "testing", "hypothesis", "experimentation"],
                "difficulty": "medium"
            },
        ]
    }
}


DEFAULT_QUESTIONS = {
    "technical": [
        {
            "question": "Describe your approach to solving complex technical problems.",
            "keywords": ["problem solving", "analysis", "research", "testing", "iteration"],
            "difficulty": "medium"
        },
        {
            "question": "What programming languages and frameworks are you most proficient in?",
            "keywords": ["languages", "frameworks", "proficiency", "experience", "projects"],
            "difficulty": "easy"
        },
        {
            "question": "How do you ensure code quality and maintainability in your projects?",
            "keywords": ["code quality", "testing", "review", "documentation", "best practices"],
            "difficulty": "medium"
        },
    ],
    "behavioral": [
        {
            "question": "Where do you see yourself in five years?",
            "keywords": ["career", "growth", "goals", "development", "learning"],
            "difficulty": "easy"
        },
        {
            "question": "Tell me about a project you're most proud of.",
            "keywords": ["project", "achievement", "challenge", "solution", "outcome"],
            "difficulty": "easy"
        },
    ]
}


class QuestionGenerator:
    def __init__(self):
        self.question_banks = QUESTION_BANKS
        self.default_questions = DEFAULT_QUESTIONS
    
    def generate(self, request: QuestionGenerateRequest) -> List[QuestionItem]:
        role_lower = request.role.lower()
        interview_type = request.interview_type
        
        selected_questions = []
        
        if role_lower in self.question_banks:
            bank = self.question_banks[role_lower]
        else:
            bank = self.question_banks["backend developer"]
        
        if interview_type in ["technical", "mixed"]:
            tech_questions = bank.get("technical", self.default_questions["technical"])
            tech_count = len(tech_questions) if interview_type == "technical" else (request.total_questions * 2) // 3
            selected_questions.extend(self._select_questions(tech_questions, tech_count, "technical"))
        
        if interview_type in ["behavioral", "mixed"]:
            behav_questions = bank.get("behavioral", self.default_questions["behavioral"])
            behav_count = len(behav_questions) if interview_type == "behavioral" else request.total_questions // 3
            selected_questions.extend(self._select_questions(behav_questions, behav_count, "behavioral"))
        
        random.shuffle(selected_questions)
        
        return selected_questions[:request.total_questions]
    
    def _select_questions(self, questions: List[dict], count: int, q_type: str) -> List[QuestionItem]:
        difficulty_map = {"easy": 1, "medium": 2, "hard": 3}
        exp_level = {"junior": 1, "mid": 2, "senior": 3, "lead": 4}
        
        exp_num = exp_level.get("mid", 2)
        
        scored = []
        for q in questions:
            diff_num = difficulty_map.get(q.get("difficulty", "medium"), 2)
            score = 1 / (1 + abs(diff_num - exp_num))
            scored.append((q, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        selected = [q for q, _ in scored[:count]]
        
        return [
            QuestionItem(
                question=q["question"],
                type=q_type,
                difficulty=q.get("difficulty", "medium"),
                keywords=q.get("keywords", []),
                time_limit=300
            )
            for q in selected
        ]


question_generator = QuestionGenerator()

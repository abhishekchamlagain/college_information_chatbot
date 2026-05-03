"""
Padmashree College Chatbot — Flask API Server
Run: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle, json, re, random, os, nltk
from datetime import datetime
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# ── Download NLTK data ────────────────────────────────────
for pkg in ["punkt", "wordnet", "stopwords", "omw-1.4"]:
    nltk.download(pkg, quiet=True)

# ── Flask App ─────────────────────────────────────────────
app = Flask(__name__,
            template_folder="website",   # your website folder
            static_folder="website",     # serves css/js/images
            static_url_path="")          # keeps original paths

CORS(app)  # allows frontend to call API

# ── Load Model ────────────────────────────────────────────
print("Loading model...")
model        = pickle.load(open("model.pkl", "rb"))
le           = pickle.load(open("le.pkl",    "rb"))
intents_data = json.load(open("intents_final.json", "r", encoding="utf-8"))
print(f" Model loaded | Intents: {len(intents_data['intents'])}")

# ══════════════════════════════════════════════════════════
# PREPROCESSING PIPELINE (copied from notebook)
# ══════════════════════════════════════════════════════════

lemmatizer = WordNetLemmatizer()

try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS = set(stopwords.words("english"))

IMPORTANT_WORDS = {"not","no","when","where","how","what","who",
                   "which","why","can","is","are","have","do",
                   "does","will","any","more"}
STOPWORDS -= IMPORTANT_WORDS

ROMAN_NEPALI_MAP = {
    "k xa bro":"what is","k ho bro":"what is","kaha xa bro":"where is",
    "kaha cha":"where is","kaha xa":"where is","kati xa":"how much",
    "kati ho":"how much","kati cha":"how much","kasari garne":"how to do",
    "kasari linu":"how to get","kasari":"how","kun kun":"which all",
    "kun":"which","k xa":"what is","k ho":"what is","k chha":"what is",
    "k cha":"what is","kasto":"what kind","kahile":"when",
    "paincha ki":"available","paincha":"available get",
    "milcha ki":"possible","milcha":"possible available",
    "lagcha":"cost required","huncha":"happens",
    "padhna xa":"want to study","padhna":"study","padhye":"after studying",
    "garne":"do","garnu":"do","linu":"take","dinu":"give",
    "hernu":"check see","apply garne":"apply","join garne":"join",
    "bata":"from","ramro xa":"good","ramro":"good","sasto":"cheap affordable",
    "mahango":"expensive","ekdam":"very","dherai":"very much",
    "thik xa":"okay","namaste":"hello","namaskar":"hello",
    "sanchai":"hello","dhanyabad":"thank you","shukriya":"thank you",
    "kaam lagyo":"helpful","clear bhayo":"clear understood",
    "bujhyo":"understood",
    "bro":"","dai":"","didi":"","yar":"","ni":"","na":"",
    "ta":"","nai":"","hai":"","aba":"","ra":"",
}

ABBR_MAP = {
    r"\bbit\b":"bachelor information technology",
    r"\bbca\b":"bachelor computer application",
    r"\bbba\b":"bachelor business administration",
    r"\bbhm\b":"bachelor hospitality management",
    r"\btu\b":"tribhuvan university",
    r"\bfyp\b":"final year project",
    r"\bgpa\b":"grade point average",
    r"\bit\b":"information technology",
    r"\bcs\b":"computer science",
    r"\bai\b":"artificial intelligence",
    r"\bml\b":"machine learning",
    r"\bapi\b":"application programming interface",
}

CONTRACTIONS = {
    r"what's":"what is", r"don't":"do not", r"doesn't":"does not",
    r"can't":"cannot",   r"won't":"will not", r"isn't":"is not",
    r"aren't":"are not", r"i'm":"i am",       r"you're":"you are",
    r"it's":"it is",     r"we're":"we are",   r"they're":"they are",
    r"i've":"i have",    r"you've":"you have", r"i'll":"i will",
    r"you'll":"you will",r"he's":"he is",     r"she's":"she is",
}

def normalize_fb_nepali(text):
    for k, v in sorted(ROMAN_NEPALI_MAP.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'\b' + re.escape(k) + r'\b', v, text)
    return text

def expand_abbreviations(text):
    for p, r in ABBR_MAP.items():
        text = re.sub(p, r, text, flags=re.IGNORECASE)
    return text

def clean_text(text):
    if not text or not isinstance(text, str): return ""
    text = text.lower().strip()
    for c, e in CONTRACTIONS.items():
        text = re.sub(c, e, text, flags=re.IGNORECASE)
    text = re.sub(r'https?://\S+|www\.\S+|[\w\.-]+@[\w\.-]+\.\w+', '', text)
    text = normalize_fb_nepali(text)
    text = expand_abbreviations(text)
    text = re.sub(r"[^a-zA-Z\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_and_lemmatize(text):
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    tokens = [lemmatizer.lemmatize(t, pos='v') for t in tokens]
    tokens = [lemmatizer.lemmatize(t, pos='n') for t in tokens]
    return " ".join(tokens)

def preprocess(text):
    cleaned = clean_text(text)
    final   = tokenize_and_lemmatize(cleaned)
    return final if final.strip() else cleaned

# ══════════════════════════════════════════════════════════
# RULE-BASED ENGINE (Layer 1)
# ══════════════════════════════════════════════════════════

CONFIDENCE_THRESHOLD = 0.30

RULES = [
    # ── VP/Director — MOST SPECIFIC FIRST ────────────────
    {
        "pattern": r"\b(md\b|managing\s*director|vice\s*principal"
                   r"|vp\b|chairman"
                   r"|director\s*number|md\s*contact"
                   r"|head\s*of\s*college|college\s*director"
                   r"|director\s*padmashree|padmashree\s*md)\b",
        "tag": "VP_director",
        "response": None
    },

    # ── Contact ───────────────────────────────────────────
    {
        "pattern": r"(\+977|4112252|4112403"
                   r"|phone\s*number|contact\s*number"
                   r"|helpline|call\s*college|college\s*number"
                   r"|college\s*phone|reach\s*us)",
        "tag": "contact",
        "response": "Phone: +977-1-4112252 / +977-1-4112403\n www.padmashreecollege.edu.np"
    },

    # ── Location ──────────────────────────────────────────
    {
        "pattern": r"(gpo\s*box|google\s*map"
                   r"|how\s*to\s*reach\s*college"
                   r"|how\s*to\s*go\s*to\s*college"
                   r"|college\s*address|address\s*of\s*padmashree"
                   r"|where\s*is\s*padmashree\s*college"
                   r"|college\s*location|direction\s*to\s*college)",
        "tag": "location",
        "response": " Padmashree College, Tinkune, Kathmandu, Nepal. (GPO Box: 15252)"
    },

    # ── Website ───────────────────────────────────────────
    {
        "pattern": r"(padmashreecollege\.edu\.np"
                   r"|official\s*website|college\s*website"
                   r"|web\s*portal|website\s*link|college\s*site"
                   r"|online\s*portal)",
        "tag": "website",
        "response": " Official website: www.padmashreecollege.edu.np"
    },

    # ── Ragging ───────────────────────────────────────────
    {
        "pattern": r"\b(ragging|anti.?ragging"
                   r"|zero\s*tolerance"
                   r"|fresher\s*safe|is\s*college\s*safe"
                   r"|bullying|harassment\s*college"
                   r"|eve\s*teasing)\b",
        "tag": "ragging",
        "response": " Padmashree has ZERO TOLERANCE against ragging."
    },

    # ── Greeting ──────────────────────────────────────────
    {
        "pattern": r"^(hi|hello|hey|yo|namaste|namaskar|sanchai"
                   r"|good\s*morning|good\s*afternoon|good\s*evening"
                   r"|howdy|greetings|sup)[!\s?]*$",
        "tag": "greeting",
        "response": "Hello! Welcome to Padmashree College  How can I help you today?"
    },

    # ── Goodbye — BEFORE thanks ───────────────────────────
    {
        "pattern": r"\b(bye|goodbye|cya|see\s*you|take\s*care"
                   r"|ok\s*bye|baii|later|good\s*night"
                   r"|farewell|tata)\b",
        "tag": "goodbye",
        "response": "Goodbye! Best of luck! "
    },

    # ── Thanks ────────────────────────────────────────────
    {
        "pattern": r"\b(thank\s*you|thanks|dhanyabad|shukriya"
                   r"|thnx|thx|that\s*helped"
                   r"|appreciate|much\s*appreciated)\b",
        "tag": "thanks",
        "response": "You're welcome! Feel free to ask anything "
    },

    # ── Office Hours ──────────────────────────────────────
    {
        "pattern": r"\b(office\s*timing|office\s*timings|office\s*hours"
                   r"|opening\s*time|closing\s*time|college\s*hours"
                   r"|when\s*open|office\s*open|working\s*hours"
                   r"|what\s*time\s*open|college\s*timing"
                   r"|what\s*are\s*the\s*timings|timings\b)\b",
        "tag": "hours",
        "response": None
    },

    # ── Programs Offered ──────────────────────────────────
    {
        "pattern": r"\b(all\s*courses|courses\s*available|courses\s*offered"
                   r"|all\s*programs|programs\s*available|programs\s*offered"
                   r"|what\s*courses|which\s*courses|list\s*of\s*courses"
                   r"|list\s*of\s*programs|what\s*programs)\b",
        "tag": "programs_offered",
        "response": None
    },

    # ── Fees ──────────────────────────────────────────────
    {
        "pattern": r"\b(fee\s*structure|semester\s*fee|total\s*fee"
                   r"|annual\s*fee|fees\s*kati|how\s*much\s*fee"
                   r"|tuition\s*fee|fees\s*details"
                   r"|fees\s*information|yearly\s*fees)\b",
        "tag": "fees",
        "response": None
    },

    # ── Admission ─────────────────────────────────────────
    {
        "pattern": r"\b(how\s*to\s*apply|admission\s*process"
                   r"|admission\s*open|enrollment\s*process"
                   r"|how\s*to\s*enroll|get\s*admission"
                   r"|admission\s*procedure|intake\s*open"
                   r"|how\s*can\s*i\s*apply|apply\s*to\s*padmashree)\b",
        "tag": "admission",
        "response": None
    },
]

# ══════════════════════════════════════════════════════════
# HYBRID ENGINE FUNCTIONS
# ══════════════════════════════════════════════════════════

def rule_based_match(user_input, intents_data):
    text_lower = user_input.lower().strip()
    for rule in RULES:
        if re.search(rule["pattern"], text_lower, re.IGNORECASE):
            tag = rule["tag"]
            if rule["response"]:
                return tag, rule["response"]
            for intent in intents_data["intents"]:
                if intent["tag"] == tag and intent.get("responses"):
                    return tag, random.choice(intent["responses"])
    return None, None

def log_failed_query(user_input, response, confidence, method,
                     predicted_intent, log_file="fallback_queries.json"):
    try:
        logs = json.load(open(log_file, "r", encoding="utf-8")) if os.path.exists(log_file) else []
        logs.append({
            "timestamp":        datetime.now().isoformat(),
            "user_input":       user_input,
            "predicted_intent": predicted_intent,
            "confidence":       float(confidence),
            "method":           method,
            "bot_response":     response,
        })
        json.dump(logs, open(log_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    except Exception:
        pass

def get_response(user_input, model, le, intents_data, threshold=None):
    if threshold is None:
        threshold = CONFIDENCE_THRESHOLD

    # Layer 1 — Rule Based
    rule_tag, rule_response = rule_based_match(user_input, intents_data)
    if rule_response:
        return {"response": rule_response, "intent": rule_tag,
                "confidence": 1.0, "method": "rule-based"}

    # Layer 2 — Naive Bayes
    processed = preprocess(user_input)
    if not processed.strip():
        return {"response": "Could you rephrase that?",
                "intent": "unknown", "confidence": 0.0, "method": "fallback"}

    proba = model.predict_proba([processed])[0]
    best  = int(np.argmax(proba))
    conf  = float(proba[best])
    tag   = le.inverse_transform([best])[0]

    # Layer 3 — Confidence Gate
    if conf < threshold:
        return {"response": "I'm not sure about that. Could you rephrase, or call us at +977-1-4112252?",
                "intent": tag, "confidence": conf, "method": "fallback"}

    # Fetch from intents.json
    for intent in intents_data["intents"]:
        if intent["tag"] == tag and intent.get("responses"):
            return {"response": random.choice(intent["responses"]),
                    "intent": tag, "confidence": conf, "method": "naive-bayes"}

    return {"response": "Intent found but no response configured.",
            "intent": tag, "confidence": conf, "method": "naive-bayes"}

# ══════════════════════════════════════════════════════════
# FLASK ROUTES
# ══════════════════════════════════════════════════════════

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({
        "status":  "running",
        "intents": len(intents_data["intents"]),
        "model":   "Naive Bayes + Rule-Based Hybrid"
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        msg  = data.get("message", "").strip()

        if not msg:
            return jsonify({"success": False, "response": "Please type something!"})

        # ─── DEBUG: Log incoming message ─────────────────────────────────
        print("\n" + "─"*60)
        print(f"USER MESSAGE: {msg}")
        print("─"*60)

        result = get_response(msg, model, le, intents_data)

        # ─── DEBUG: Log bot response details ─────────────────────────────
        print(f"BOT RESPONSE  : {result['response']}")
        print(f"INTENT        : {result['intent']}")
        print(f"CONFIDENCE    : {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        print(f"METHOD        : {result['method'].upper()}")
        
        if result["method"] == "fallback":
            print(f"FALLBACK LOGGED to fallback_queries.json")
            log_failed_query(msg, result["response"],
                           result["confidence"],
                           result["method"],
                           result["intent"])
        
        print("─"*60 + "\n")

        return jsonify({
            "success":    True,
            "response":   result["response"],
            "intent":     result["intent"],
            "confidence": round(result["confidence"], 3),
            "method":     result["method"]
        })

    except Exception as e:
        print(f" ERROR: {e}")
        return jsonify({
            "success":  False,
            "response": "Sorry, something went wrong. Please try again."
        }), 500

# ══════════════════════════════════════════════════════════
# RUN SERVER
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  PADMASHREE COLLEGE CHATBOT API SERVER")
    print("="*50)
    print(f"  Intents loaded : {len(intents_data['intents'])}")
    print(f"  Rules loaded   : {len(RULES)}")
    print(f"  Threshold      : {CONFIDENCE_THRESHOLD}")
    print("="*50)
    print("  Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

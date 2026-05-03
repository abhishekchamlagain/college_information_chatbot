# Padmashree College Website with AI Chatbot

## Overview
This project integrates an AI-powered chatbot into the Padmashree College website. The chatbot appears as a floating circular button in the bottom-right corner and provides instant assistance to visitors.

## Project Structure

```
final/
├── app.py                      # Flask API server (Main backend)
├── model.pkl                   # Trained Naive Bayes model
├── le.pkl                      # Label encoder for intents
├── intents_final.json          # Intent definitions and responses
├── fallback_queries.json       # Logged fallback/unmatched queries
├── Padmashree_Chatbot_Iterative.ipynb  # Jupyter notebook (model training)
│
└── website/                    # Frontend files
    ├── index.html              # Main college website
    ├── test_chat.html          # Testing page for chatbot
    ├── README.md               # This file
    ├── css/
    │   └── style.css           # Styling for website and chatbot
    ├── js/
    │   └── chatbot.js          # Chatbot widget functionality
    └── images/                 # Website images
```

## Features

### Website Features
-  Modern, responsive design
-  Professional college layout with sections:
  - Hero section with call-to-action
  - About section with statistics
  - Courses/Programs showcase
  - Admissions information
  - Contact details
-  Mobile-friendly navigation
-  Smooth scrolling and animations

### Chatbot Features
-  Floating circular button (bottom-right corner)
-  Smooth expand/collapse animations
-  Real-time AI-powered responses
-  Chat history display
-  Typing indicators
-  Welcome message
-  Error handling
-  Responsive design

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Edge, Brave, Firefox)
- Required Python packages: Flask, Flask-CORS, NLTK, scikit-learn, numpy

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install flask flask-cors nltk scikit-learn numpy pickle
```

### Step 2: Prepare NLTK Data

The app.py automatically downloads required NLTK data on first run. Required packages:
- `punkt` - Tokenizer
- `wordnet` - Lemmatizer
- `stopwords` - English stopwords
- `omw-1.4` - Open Multilingual Wordnet

### Step 3: Start the Backend API Server

Navigate to the project root directory and run:

```bash
# Make sure you're in the main project directory
cd "C:\Users\acer\OneDrive\Pictures\Padmashree college BIT\9th Semester\FYP 2\final"

# Start the Flask API server
python app.py
```

You should see output like:
```
==================================================
  PADMASHREE COLLEGE CHATBOT API SERVER
==================================================
  Intents loaded : XX
  Rules loaded   : XX
  Threshold      : 0.30
==================================================
  Open: http://localhost:5000
==================================================
```

The API server will start on `http://localhost:5000`

### Step 4: Open the Website in Browser

**Option A: Direct File (Recommended for Testing)**
1. Navigate to the website folder
2. Open `index.html` directly in your browser
3. The chatbot will automatically connect to `http://localhost:5000/chat`

**Option B: Using Local Web Server (Better for Development)**
```bash
cd website
python -m http.server 8000
```
Then open: `http://localhost:8000` in your browser

**Note:** When you run `python app.py`, clicking the `http://localhost:5000` link in the terminal will now open directly in your default browser (Chrome, Edge, or Brave).

## Usage

### Using the Chatbot

1. **Open the Website**: Load `index.html` in your browser
2. **Find the Chat Button**: Look for the circular blue button in the bottom-right corner
3. **Start Chatting**: 
   - Click the button to open the chat window
   - Type your message in the input field
   - Press Enter or click the send button
   - Wait for the AI assistant to respond

4. **Close Chat**: Click the × button or the circular button again

### Sample Questions to Try

- "What courses do you offer?"
- "How can I apply for admission?"
- "What are the eligibility criteria?"
- "Tell me about the college"
- "What is the fee structure?"
- "Where is the college located?"

## API Endpoints

### Base URL: `http://localhost:5000`

#### `GET /`
Health check and API information

#### `GET /health`
Check API and chatbot status

#### `POST /chat`
Send a message to the chatbot

**Request:**
```json
{
  "message": "What courses do you offer?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "We offer BBA, MBA, BCA, MCA, B.Tech, M.Tech...",
  "message": "What courses do you offer?"
}
```

## Customization

### Changing Colors & Styling
Edit `website/css/style.css` and modify the CSS variables or specific classes to customize:
- Chatbot button colors
- Chat window appearance
- Font styles and sizes
- Animation effects

### Modifying College Information
Edit `website/index.html` to update:
- College name and branding
- Contact information
- Courses offered
- About section content
- Admissions details
- Navigation links

### Updating Chatbot Responses
The chatbot uses a **Hybrid Engine** with 3 layers:

1. **Rule-Based Matching** (Fastest - Exact patterns):
   - Edit the `RULES` list in `app.py`
   - Add specific patterns for common questions
   - Includes support for Roman Nepali text normalization

2. **Naive Bayes Classification** (ML-based):
   - Edit `intents_final.json` to add/modify intents
   - Add new patterns and responses
   - Retrain the model using the Jupyter notebook

3. **Fallback Responses**:
   - Logged to `fallback_queries.json`
   - Use these to improve the chatbot
   - Add patterns to `RULES` for frequently asked questions

### Files to Edit:
- `intents_final.json` - Intent definitions with patterns and responses
- `app.py` - Rules engine and configuration
- `fallback_queries.json` - Review unmatched queries to improve responses

## Troubleshooting

### Chatbot not responding

1. **Check if API server is running:**
   ```bash
   python app.py
   ```
   You should see:
   ```
   PADMASHREE COLLEGE CHATBOT API SERVER
   Intents loaded : [number]
   Rules loaded   : [number]
   ```

2. **Verify Flask is installed:**
   ```bash
   pip install flask flask-cors
   ```

3. **Check browser console** (Press F12):
   - Open Console tab
   - Look for error messages (e.g., network errors)
   - Verify API URL: `http://localhost:5000/chat`

4. **Test API manually:**
   ```bash
   # Using curl (Windows PowerShell)
   $body = @{message='hello'} | ConvertTo-Json
   Invoke-WebRequest -Uri "http://localhost:5000/chat" -Method POST -Body $body -ContentType "application/json"
   ```

### Chat window not appearing

1. **Check if chatbot.js is loaded:**
   - Press F12 → Network tab
   - Refresh page
   - Look for `chatbot.js` - should have status 200
   - Check console for JavaScript errors

2. **Verify JavaScript path** in `index.html`:
   - Should point to: `js/chatbot.js`

3. **Clear browser cache:**
   - Press `Ctrl + Shift + Delete`
   - Clear all browsing data
   - Restart browser

### Model or Data Loading Errors

1. **Missing model files:**
   - Ensure `model.pkl` and `le.pkl` are in the main directory
   - Run `Padmashree_Chatbot_Iterative.ipynb` to retrain model

2. **JSON parsing errors:**
   - Verify `intents_final.json` is valid JSON
   - Check for syntax errors (missing commas, quotes)
   - Use online JSON validator

3. **NLTK data errors:**
   - App automatically downloads on first run
   - If fails, manually download:
     ```python
     import nltk
     nltk.download('punkt')
     nltk.download('wordnet')
     nltk.download('stopwords')
     nltk.download('omw-1.4')
     ```

### Port Already in Use

If you get `Address already in use` error:

```bash
# Find and kill process using port 5000
# Windows PowerShell:
Get-Process | Where-Object {$_.Handles -match "5000"}

# Or just change port in app.py:
app.run(debug=True, host="0.0.0.0", port=5001)  # Use 5001 instead
```

### Styling Issues

1. **CSS file not loading:**
   - Press F12 → Network tab
   - Verify `style.css` loads (status 200)
   - Check file path: `css/style.css`

2. **Try hard refresh:**
   - `Ctrl + Shift + R` (Windows/Linux)
   - `Cmd + Shift + R` (Mac)

## Development

### Quick Start for Development

**Terminal 1: Run Backend**
```bash
cd final/
python app.py
```

**Terminal 2: Serve Frontend (Optional)**
```bash
cd final/website
python -m http.server 8000
```

**Browser:**
- Visit `http://localhost:8000` (or open `index.html` directly)
- Open F12 Developer Tools to see console logs and network requests

### Testing the Chatbot API

**Using curl (Windows PowerShell):**
```powershell
$body = @{message='What courses do you offer?'} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/chat" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```

**Using Python:**
```python
import requests
import json

response = requests.post('http://localhost:5000/chat', 
    json={'message': 'What courses do you offer?'})
print(json.dumps(response.json(), indent=2))
```

### Chatbot Response Layers

The hybrid chatbot engine prioritizes responses:

1. **Rule-Based** (Highest Priority) - Fastest, most accurate for known patterns
2. **Naive Bayes ML** (Medium Priority) - Flexible learning-based classification
3. **Confidence Gate** (Quality Control) - Rejects low-confidence predictions
4. **Fallback** (Safety Net) - Logs unknown queries for improvement

## Deployment

### For Production Deployment:

**Backend:**
1. Install production WSGI server:
   ```bash
   pip install gunicorn
   ```

2. Update `app.py`:
   ```python
   if __name__ == "__main__":
       app.run(debug=False, host="0.0.0.0", port=5000)  # Set debug=False
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

**Frontend:**
1. Host on web server (IIS, Apache, Nginx, or cloud platform)
2. Update chatbot API URL in `website/js/chatbot.js` if needed:
   ```javascript
   const API_URL = "https://your-production-domain.com/chat";
   ```
3. Minify CSS and JavaScript for production
4. Optimize images

**Security Considerations:**
-  Set `debug=False` in Flask
-  Enable HTTPS/SSL certificates
-  Implement rate limiting on `/chat` endpoint
-  Add input validation and sanitization
-  Use environment variables for sensitive config
-  Implement proper CORS policies
-  Add request logging and monitoring
-  Regular security updates for dependencies

### Deployment Options:
- **Local/On-premise:** Windows Server or Linux Server
- **Cloud:** Heroku, PythonAnywhere, AWS, Azure, Google Cloud
- **Containerized:** Docker + Docker Compose for scalability

## Features Summary

### Core Chatbot Features
-  **Hybrid Engine** - Rule-based + Machine Learning classification
-  **Nepali Language Support** - Roman Nepali text normalization  
-  **Intent Recognition** - Custom intents from `intents_final.json`
-  **Confidence Scoring** - Rejects low-confidence responses
-  **Query Logging** - Saves unmatched queries to `fallback_queries.json`
-  **Chat History** - Maintains conversation context
-  **Typing Indicators** - Shows bot is thinking
-  **Error Handling** - Graceful fallback responses
-  **CORS Support** - Safe cross-origin requests
-  **Real-time Responses** - AJAX-powered chat

### Website Features
-  Modern, responsive design
-  Mobile-friendly interface
-  Floating chatbot widget
-  Smooth animations
-  Professional college layout

## File Reference

| File | Purpose |
|------|---------|
| `app.py` | Main Flask backend server with hybrid chatbot engine |
| `model.pkl` | Trained Naive Bayes classifier |
| `le.pkl` | Label encoder for intent classification |
| `intents_final.json` | Intent definitions, patterns, and responses |
| `fallback_queries.json` | Log of unmatched user queries for improvement |
| `website/index.html` | Main website landing page |
| `website/chatbot.js` | Frontend chatbot widget logic |
| `website/style.css` | Website and chatbot styling |
| `Padmashree_Chatbot_Iterative.ipynb` | Jupyter notebook for model training/retraining |

## Support & Resources

**For Issues:**
1. Check the Troubleshooting section above
2. Review `fallback_queries.json` for unmatched patterns
3. Check browser console (F12) for JavaScript errors
4. Check terminal output for Python/Flask errors

**To Improve Chatbot:**
1. Review `fallback_queries.json` periodically
2. Add new patterns to `RULES` in `app.py` for common questions
3. Update `intents_final.json` with new intents
4. Retrain model using `Padmashree_Chatbot_Iterative.ipynb`

**Contact & Contribution:**
- For college-specific questions: Contact Padmashree College
- For chatbot improvements: Review the Jupyter notebook for model details

## Technologies Used

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python, Flask
- **ML/AI:** Scikit-learn, NLTK
- **Others:** Flask-CORS

---

**Created for Padmashree College - FYP 2026**

# Padmashree College Website with AI Chatbot

## Overview
This project integrates an AI-powered chatbot into the Padmashree College website. The chatbot appears as a floating circular button in the bottom-right corner and provides instant assistance to visitors.

## Project Structure

```
FYP 2026/
├── website/                    # Frontend files
│   ├── index.html             # Main college website
│   ├── css/
│   │   └── style.css          # Styling for website and chatbot
│   └── js/
│       └── chatbot.js         # Chatbot widget functionality
│
├── api/                       # Backend API
│   └── app.py                 # Flask API server
│
├── src/                       # Chatbot source code
│   ├── chatbot.py            # Main chatbot logic
│   ├── model.py              # ML model handling
│   └── ...                   # Other modules
│
├── models/                    # Trained models
│   └── chatbot_model.pkl
│
└── config/                    # Configuration files
    ├── intents_final.json
    └── fallback_queries.json
```

## Features

### Website Features
- ✅ Modern, responsive design
- ✅ Professional college layout with sections:
  - Hero section with call-to-action
  - About section with statistics
  - Courses/Programs showcase
  - Admissions information
  - Contact details
- ✅ Mobile-friendly navigation
- ✅ Smooth scrolling and animations

### Chatbot Features
- ✅ Floating circular button (bottom-right corner)
- ✅ Smooth expand/collapse animations
- ✅ Real-time AI-powered responses
- ✅ Chat history display
- ✅ Typing indicators
- ✅ Welcome message
- ✅ Error handling
- ✅ Responsive design

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Start the Backend API Server

```bash
# Navigate to project root
cd "C:\Users\acer\OneDrive\Desktop\FYP II\FYP 2026"

# Start the Flask API server
python api/app.py
```

The API server will start on `http://localhost:5000`

### Step 3: Open the Website

1. Navigate to the website folder:
   ```
   C:\Users\acer\OneDrive\Desktop\FYP II\FYP 2026\website\
   ```

2. Open `index.html` in your web browser:
   - Double-click the file, OR
   - Right-click → Open with → Your browser, OR
   - Use a local server (recommended for development):
     ```bash
     # Using Python's built-in server
     cd website
     python -m http.server 8000
     ```
     Then visit: `http://localhost:8000`

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

### Changing Colors
Edit `website/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-color: #1e40af;      /* Main blue color */
    --secondary-color: #3b82f6;    /* Light blue */
    --accent-color: #f59e0b;       /* Orange accent */
}
```

### Modifying College Information
Edit `website/index.html` to update:
- College name
- Contact information
- Courses offered
- About section content
- Admissions details

### Updating Chatbot Responses
Edit the training data and intents:
- `config/intents_final.json` - Intent definitions
- `config/fallback_queries.json` - Fallback responses

Then retrain the model:
```bash
python scripts/train_model.py
```

## Troubleshooting

### Chatbot not responding
1. **Check if API server is running:**
   ```bash
   python api/app.py
   ```
   You should see: "PADMASHREE COLLEGE CHATBOT API SERVER"

2. **Check browser console** (F12):
   - Look for error messages
   - Verify API URL is correct (`http://localhost:5000/chat`)

3. **Check CORS**: Make sure `flask-cors` is installed

### Chat window not appearing
1. **Clear browser cache** (Ctrl + Shift + Delete)
2. **Check JavaScript console** for errors (F12)
3. **Verify files are in correct locations**

### Styling issues
1. **Check if CSS file is loaded**: Open browser DevTools → Network tab
2. **Verify CSS file path** in `index.html`
3. **Try hard refresh**: Ctrl + Shift + R

## Development

### Running in Development Mode

1. **Backend (with auto-reload):**
   ```bash
   python api/app.py
   ```
   Flask runs in debug mode by default

2. **Frontend (with live server):**
   ```bash
   cd website
   python -m http.server 8000
   ```

### Testing the API

Using curl:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello\"}"
```

Using Python:
```python
import requests

response = requests.post('http://localhost:5000/chat', 
    json={'message': 'What courses do you offer?'})
print(response.json())
```

## Deployment

### For Production Deployment:

1. **Backend:**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set `debug=False` in `app.py`
   - Use environment variables for configuration
   - Set up proper logging

2. **Frontend:**
   - Host on a web server (Apache, Nginx)
   - Update API URL in `chatbot.js` to production URL
   - Minify CSS and JavaScript
   - Optimize images

3. **Security:**
   - Enable HTTPS
   - Add rate limiting
   - Implement input validation
   - Set up proper CORS policies

## Support

For issues or questions:
- Check the documentation in `/docs` folder
- Review the implementation notes
- Check the project structure documentation

## Technologies Used

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python, Flask
- **ML/AI:** Scikit-learn, NLTK
- **Others:** Flask-CORS

---

**Created for Padmashree College - FYP 2026**

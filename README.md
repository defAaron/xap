Xap - Last Tweet Searching Tool for X
=
Xap is a simple Flask-based web application that allows users to search the most recent tweet posted by a specific handle on a given date.

Features
-
🔍 Tweet Lookup  
- Handle Input: Enter a Twitter handle (without `@`)  
- Date Selection: Choose a date in `YYYY-MM-DD` format  
- Tweet Result: Returns the last tweet posted on that date, or shows "No tweet on that date" if none is found  

🖥️ Web UI  
- Simple form-based interface (Flask + HTML)  
- Real-time results displayed below the search form  

🚧 Future Features (Planned)  
- Integration with Twitter/X API for real tweets  
- Error handling for invalid usernames and missing data  
- UI improvements with Bootstrap/Tailwind  
- Deployment to Heroku/Render for public access 

Technology Stack
-
- **Frontend:** HTML 
- **Backend:** Python Flask  

Getting Started
-

### Prerequisites
- Python 3.9 or higher  
- pip: package manager


### Installation
Clone the repository:
```bash
git clone <repository-url>
cd training_project

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

Install dependencies:

pip install -r requirements.txt


Run the Flask development server:

python3 app.py


Open your browser:

http://127.0.0.1:5000

Project Structure
xap/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── templates/
    └── home.html       # Frontend HTML template

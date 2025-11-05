# QuizNexus

QuizNexus is a comprehensive quiz management system designed for educational institutions and online learning platforms. It features an **AI-powered student advisor** that provides personalized study suggestions, identifies weak areas, and sends intelligent reminders to help students succeed.

## ✨ Key Features

- 📚 **Quiz Management**: Create and manage quizzes with multiple subjects and chapters
- 🤖 **AI Student Advisor**: Personalized study suggestions powered by advanced AI
- 📊 **Real-time Analytics**: Track performance and progress over time
- 📧 **Smart Reminders**: AI-generated daily reminders with personalized insights
- 🎯 **Weak Topic Detection**: Automatically identifies areas needing improvement
- 📈 **Monthly Reports**: Comprehensive performance reports with AI insights
- 👥 **Role-based Access**: Separate interfaces for students and administrators

## Prerequisites

Before running the application, ensure you have:

- **Python 3.8+** installed
- **Node.js 14+** and npm
- **Redis** (for Celery task queue)
- **MailHog** (for email testing)
- **Git** for version control
- **Groq API Key** (for AI features)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/QuizNexus.git
cd QuizNexus
```

### 2. Backend Setup

Navigate to the backend directory and set up the Python environment:

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration (see below)

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. Environment Configuration

Edit the `.env` file in the backend directory:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=sqlite:///quiz_nexus.db

# Redis (for Celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration (MailHog)
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=False
MAIL_USE_SSL=False
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@quiznexus.com

# AI Configuration (Required for AI features)
GROQ_API_KEY=your-groq-api-key-here
```

**Getting Groq API Key:**
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key and copy it to your `.env` file

### 4. Install and Run Redis

**On macOS:**
```bash
brew install redis
brew services start redis
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**On Windows:**
Download and install Redis from [https://github.com/microsoftarchive/redis/releases](https://github.com/microsoftarchive/redis/releases)

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### 5. Install and Run MailHog (Email Testing)

MailHog is a lightweight email testing tool that captures emails sent by the application.

**On macOS:**
```bash
brew install mailhog
mailhog
```

**On Ubuntu/Debian:**
```bash
# Download and install
sudo wget -O /usr/local/bin/mailhog https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
sudo chmod +x /usr/local/bin/mailhog

# Run MailHog
mailhog
```

**On Windows:**
Download from [https://github.com/mailhog/MailHog/releases](https://github.com/mailhog/MailHog/releases)

MailHog will:
- Listen for SMTP connections on port **1025**
- Provide a web UI at **http://localhost:8025**

### 6. Run the Application

You need **4 terminal windows** to run the complete application:

**Terminal 1 - Backend API:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```
Backend runs on: `http://localhost:5000`

**Terminal 2 - Celery Worker (AI Agent & Background Tasks):**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
celery -A app.celery_app worker -B --loglevel=info
```

This starts:
- **Celery Worker**: Processes background tasks
- **Celery Beat**: Schedules periodic tasks (reminders, reports)
- **AI Agent System**: Generates personalized study suggestions

**Terminal 3 - MailHog (Email Testing):**
```bash
mailhog
```
Access email UI at: `http://localhost:8025`

**Terminal 4 - Frontend:**
```bash
cd frontend
npm install
npm run serve
```
Frontend runs on: `http://localhost:8080`

## 🤖 AI Student Advisor Features

The AI-powered student advisor uses **LangChain**, **LangGraph**, and **Groq AI** to provide:

### 1. **Personalized Study Suggestions**
- Analyzes quiz performance trends
- Identifies learning patterns
- Generates specific, actionable study tips
- Adapts recommendations based on progress

### 2. **Weak Topic Detection**
- Automatically identifies subjects where student scored below 70%
- Prioritizes topics needing immediate attention
- Tracks improvement over time
- Provides targeted practice recommendations

### 3. **Daily Reminder Emails**
The AI agent sends intelligent daily reminders that include:
- 📚 Topics that need attention
- 💡 Personalized study suggestions (4-6 actionable tips)
- 🎯 Specific quizzes to focus on
- 🚀 Motivational messages tailored to performance
- 📊 Performance trend analysis

**Example AI-Generated Email Content:**
```
🤖 AI-Powered Study Insights

You're making great progress! Here's how to level up:

📚 Topics That Need Your Attention:
• Algebra fundamentals
• Chemical bonding concepts
• World War II history

💡 Personalized Study Suggestions:
1. Review your mistakes in the Algebra Quiz from last week
2. Focus on practice problems for chemical equations
3. Create flashcards for historical dates and events
4. Set aside 30 minutes daily for focused study sessions
5. Try teaching concepts to a friend to reinforce learning

🎯 Focus on These Quizzes:
• Basic Algebra - Score: 65% (Subject: Mathematics)
• Chemical Reactions - Score: 68% (Subject: Chemistry)
```

### 4. **Monthly Performance Reports**
- Comprehensive activity summaries
- Performance trend analysis
- Ranking among peers
- AI-powered improvement suggestions

### 5. **Multi-Agent Architecture**

The system uses 5 specialized AI agents:

1. **Performance Analyzer Agent**: Analyzes quiz scores and patterns
2. **Weak Topic Identifier Agent**: Detects areas needing improvement
3. **Suggestion Generator Agent**: Creates personalized study plans
4. **Motivational Coach Agent**: Generates encouraging messages
5. **Report Compiler Agent**: Assembles comprehensive reports

## Celery Background Tasks

The application runs the following scheduled tasks:

### Task Schedule

| Task | Frequency | Description |
|------|-----------|-------------|
| `calculate_ended_quiz_scores` | Every 10 seconds | Automatically calculates scores for completed quizzes |
| `send_daily_reminders` | Every 5 seconds (configurable) | Sends AI-powered personalized reminders to students |
| `send_monthly_reports` | 1st of each month at 9 AM | Generates and sends monthly performance reports |
| `test_monthly_reports` | Every 30 seconds | Testing version of monthly reports |

### Configuring Task Schedule

Edit `/home/deondmello/Documents/Github/QuizNexus/backend/app/celeryconfig.py`:

```python
from celery.schedules import crontab

beat_schedule = {
    "send-daily-reminders": {
        "task": "app.tasks.send_daily_reminders",
        "schedule": crontab(hour=18, minute=0),  # Run daily at 6 PM
    },
    # ...other tasks
}
```

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env file with backend API URL

# Start development server
npm run serve
```

Frontend environment variables (.env):
```env
VUE_APP_API_BASE_URL=http://localhost:5000/api
```

## Project Structure

```
QuizNexus/
├── backend/
│   ├── app/
│   │   ├── agent/                    # 🤖 AI Agent System (NEW)
│   │   │   ├── __init__.py
│   │   │   └── student_advisor.py   # Multi-agent advisor
│   │   ├── api/
│   │   │   ├── resource/            # API endpoints
│   │   │   └── validators/          # Request validation
│   │   ├── middleware/              # Authentication middleware
│   │   ├── models/                  # Database models
│   │   ├── tasks.py                 # Celery background tasks
│   │   ├── celery_app.py           # Celery configuration
│   │   ├── celeryconfig.py         # Task scheduling
│   │   ├── email.py                # Email utilities
│   │   └── __init__.py             # App factory
│   ├── migrations/                  # Database migrations
│   ├── requirements.txt
│   ├── .env                        # Environment variables
│   └── app.py                      # Application entry point
├── frontend/
│   ├── public/                     # Static assets
│   ├── src/
│   │   ├── components/             # Vue components
│   │   ├── router/                 # Vue Router
│   │   ├── stores/                 # Vuex store
│   │   └── App.vue                 # Root component
│   └── package.json
└── README.md
```

## API Endpoints

### Authentication

- `POST /api/login` - User login
- `POST /api/register` - User registration
- `POST /api/logout` - User logout
- `POST /api/check_token_valid` - Token validation

### Admin Endpoints

- `GET /api/subjects` - List all subjects
- `POST /api/subjects` - Create new subject
- `GET /api/chapters` - List chapters by subject
- `POST /api/chapters` - Create new chapter
- `GET /api/quizzes` - List quizzes
- `POST /api/quizzes` - Create new quiz
- `GET /api/questions` - List questions by quiz
- `POST /api/questions` - Add question to quiz

### User Endpoints

- `GET /api/dashboard` - User dashboard data
- `GET /api/take_quiz` - Get quiz questions
- `POST /api/take_response` - Submit quiz answers
- `GET /api/scoreboard` - User's score history

### Analytics

- `GET /api/admin/dashboard` - Admin dashboard statistics
- `GET /api/admin/users` - User management
- `POST /api/admin/export` - Generate data exports

## Usage Guide

### For Students

1. **Registration**: Create an account using the registration form
2. **Dashboard**: View upcoming and past quizzes
3. **Take Quiz**: Click on available quizzes to start
4. **Receive AI Insights**: Get personalized study suggestions via email
5. **View Results**: Check scores and AI-generated feedback
6. **Track Progress**: Monitor improvement with AI-powered analytics

### For Administrators

1. **Login**: Access admin panel with administrator credentials
2. **Manage Subjects**: Create and organize academic subjects
3. **Create Chapters**: Structure content within subjects
4. **Build Quizzes**: Create quizzes with multiple choice questions
5. **Monitor Users**: Track user activity and performance
6. **Export Data**: Generate reports for analysis
7. **View Email Activity**: Check MailHog for sent emails

## Testing the AI Features

1. **Create a test account** and take some quizzes
2. **Check MailHog** at `http://localhost:8025` to see AI-generated emails
3. **Score below 70%** on some quizzes to trigger weak topic detection
4. **Wait for scheduled tasks** to run or adjust schedule in `celeryconfig.py`
5. **Monitor Celery logs** to see AI agent activity

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm run test
```

## Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Restart Redis
# macOS: brew services restart redis
# Linux: sudo systemctl restart redis-server
```

### Celery Not Starting
```bash
# Check if Redis is accessible
redis-cli ping

# Verify Celery configuration
celery -A app.celery_app inspect active

# Clear Celery tasks
celery -A app.celery_app purge
```

### MailHog Not Receiving Emails
- Ensure MailHog is running on port 1025
- Check MAIL_PORT in .env is set to 1025
- Verify MAIL_SERVER is set to 'localhost'
- Check MailHog UI at http://localhost:8025

### AI Features Not Working
- Verify GROQ_API_KEY is set in .env
- Check Celery worker logs for AI-related errors
- Ensure all AI dependencies are installed: `pip install langchain langchain-groq langgraph`
- Test AI connection: The worker logs should show "AI Advisor initialized successfully"

### Common Issues

**Backend won't start:**
- Check Python version (3.8+ required)
- Ensure all dependencies are installed
- Verify database connectivity
- Check environment variables

**Frontend build fails:**
- Update Node.js to latest LTS version
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

## Database Schema

### Key Models

- **User**: User accounts with role-based permissions
- **UserPreference**: User settings for email reminders and reports
- **Subject**: Academic subjects for quiz organization
- **Chapter**: Chapters within subjects
- **Quiz**: Quiz instances with timing and metadata
- **Question**: Individual quiz questions with options
- **QuizResponse**: User responses to questions
- **Score**: Calculated quiz scores and timestamps

## Security Considerations

- JWT tokens are stored securely in localStorage
- Password hashing using Werkzeug utilities
- Role-based access control for all endpoints
- Input validation and sanitization
- CORS configuration for API security
- Groq API key is stored securely in environment variables

## Performance Optimization

- Database queries are optimized with proper indexing
- Frontend uses lazy loading for components
- API responses are paginated where appropriate
- Celery handles background tasks asynchronously
- AI agent system caches LLM instances
- Redis provides fast task queue management

## Technologies Used

### Backend
- Flask - Web framework
- SQLAlchemy - ORM
- Celery - Task queue
- Redis - Message broker
- LangChain - AI framework
- LangGraph - Agent orchestration
- Groq AI - LLM provider

### Frontend
- Vue.js 3 - Frontend framework
- Vue Router - Routing
- Vuex - State management
- Chart.js - Data visualization



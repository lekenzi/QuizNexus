# QuizNexus

QuizNexus is a comprehensive quiz management system designed for educational institutions and online learning platforms. It provides a complete solution for creating, managing, and taking quizzes with real-time analytics and role-based access control.

## Features

### 🎯 Core Functionality
- **Quiz Management**: Create, edit, and organize quizzes by subjects and chapters
- **Question Bank**: Support for multiple choice questions with customizable options
- **Real-time Quiz Taking**: Interactive quiz interface with timer functionality
- **Automated Scoring**: Instant score calculation and result display
- **Progress Tracking**: Comprehensive analytics and performance metrics

### 👥 User Management
- **Role-based Access Control**: Separate interfaces for administrators and students
- **Secure Authentication**: JWT-based authentication with refresh tokens
- **User Profiles**: Customizable user profiles with personal information
- **Registration System**: Self-service user registration with validation

### 📊 Analytics & Reporting
- **Performance Dashboard**: Visual charts showing quiz performance by subject and chapter
- **Score History**: Detailed scoring history with timestamps
- **Statistical Analysis**: Average scores, completion rates, and trend analysis
- **Data Export**: CSV export functionality for administrative reporting

### 🔧 Administrative Features
- **Subject Management**: Create and organize academic subjects
- **Chapter Organization**: Structure content by chapters within subjects
- **User Administration**: Manage user accounts and permissions
- **System Analytics**: Overview of system usage and statistics

## Technology Stack

### Frontend
- **Vue.js 3**: Progressive JavaScript framework with Composition API
- **Vue Router 4**: Client-side routing and navigation
- **Vuex 4**: State management for application data
- **Bootstrap 5**: CSS framework for responsive design
- **Chart.js**: Data visualization for analytics
- **Axios**: HTTP client for API communication

### Backend
- **Python Flask**: Lightweight web framework
- **Flask-RESTful**: RESTful API development
- **Flask-JWT-Extended**: JWT authentication and authorization
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database engine (development)
- **Werkzeug**: Password hashing and security utilities

## Prerequisites

Before running the application, ensure you have:

- **Python 3.8+** installed
- **Node.js 14+** and npm
- **Git** for version control

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/QuizNexus_21f3002473.git
cd QuizNexus_21f3002473
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
# Edit .env file with your configuration

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the backend server
python app.py
```

The backend server will start on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

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

The frontend application will be available at `http://localhost:8080`

## Environment Configuration

### Backend (.env)
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///quiz_nexus.db
```

### Frontend (.env)
```env
VUE_APP_API_BASE_URL=http://localhost:5000/api
```

## Project Structure

```
QuizNexus_21f3002473/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── resource/         # API endpoints
│   │   │   └── validators/       # Request validation
│   │   ├── middleware/           # Authentication middleware
│   │   ├── models/              # Database models
│   │   └── __init__.py          # App factory
│   ├── migrations/              # Database migrations
│   ├── requirements.txt
│   └── app.py                   # Application entry point
├── frontend/
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # Vue components
│   │   │   ├── admin/          # Admin components
│   │   │   ├── users/          # User components
│   │   │   ├── fragments/      # Reusable components
│   │   │   └── LandingPage/    # Authentication components
│   │   ├── router/             # Vue Router configuration
│   │   ├── stores/             # Vuex store
│   │   └── App.vue             # Root component
│   ├── package.json
│   └── vue.config.js
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
4. **View Results**: Check scores and performance analytics
5. **Track Progress**: Monitor improvement over time

### For Administrators
1. **Login**: Access admin panel with administrator credentials
2. **Manage Subjects**: Create and organize academic subjects
3. **Create Chapters**: Structure content within subjects
4. **Build Quizzes**: Create quizzes with multiple choice questions
5. **Monitor Users**: Track user activity and performance
6. **Export Data**: Generate reports for analysis

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

### Code Formatting
```bash
# Frontend
cd frontend
npm run lint
npm run format

# Backend
cd backend
black .
flake8 .
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build

# Backend with production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Deployment

### Using Docker (Recommended)
```bash
# Build and run with docker-compose
docker-compose up --build

# Or build individual containers
docker build -t quiznexus-frontend ./frontend
docker build -t quiznexus-backend ./backend
```

### Manual Deployment
1. Set up production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Build frontend assets: `npm run build`
4. Deploy backend with WSGI server (Gunicorn/uWSGI)
5. Serve frontend through web server (Nginx/Apache)

## Database Schema

### Key Models
- **User**: User accounts with role-based permissions
- **Subject**: Academic subjects for quiz organization
- **Chapter**: Chapters within subjects
- **Quiz**: Quiz instances with timing and metadata
- **Question**: Individual quiz questions with options
- **QuizResponse**: User responses to questions
- **Score**: Calculated quiz scores and timestamps

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a Pull Request

### Development Guidelines
- Follow Vue.js and Flask best practices
- Write meaningful commit messages
- Include tests for new features
- Update documentation as needed
- Ensure code is properly formatted

## Troubleshooting

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

**Authentication issues:**
- Verify JWT secret keys match between frontend and backend
- Check token expiration settings
- Ensure CORS is properly configured

**Database errors:**
- Run database migrations: `flask db upgrade`
- Check database permissions
- Verify database URL in environment variables

## Security Considerations

- JWT tokens are stored securely in localStorage
- Password hashing using Werkzeug utilities
- Role-based access control for all endpoints
- Input validation and sanitization
- CORS configuration for API security

## Performance Optimization

- Database queries are optimized with proper indexing
- Frontend uses lazy loading for components
- API responses are paginated where appropriate
- Static assets are served efficiently
- Chart.js is used for optimized data visualization

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for common solutions

## Acknowledgments

- Vue.js community for excellent documentation
- Flask community for robust web framework
- Chart.js for beautiful data visualizations
- Bootstrap team for responsive design components

---

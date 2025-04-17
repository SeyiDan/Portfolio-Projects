# Health Tracker App

A comprehensive health tracking application built with Flask that allows users to monitor their weight, nutrition, workouts, sleep patterns, and set health goals.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Weight Tracking**: Log your weight measurements and visualize trends
- **Nutrition Logging**: Track daily food intake, calories, and macronutrients
- **Workout Tracking**: Record exercise sessions, duration, and calories burned
- **Sleep Monitoring**: Log sleep duration and quality
- **Goal Setting**: Set health and fitness goals with target dates
- **Data Visualization**: View charts and graphs of your health data
- **BMI Calculation**: Automatically calculate BMI based on height and weight

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Database**: SQLite (default), configurable for other databases
- **Data Visualization**: Matplotlib, Pandas
- **Forms Handling**: WTForms, Flask-WTF
- **Authentication**: Flask-Login

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/healthtrackerapp.git
cd healthtrackerapp
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

**Windows**:
```bash
venv\Scripts\activate
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set environment variables (optional):

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///health_tracker.db
FLASK_APP=app.py
FLASK_ENV=development
```

6. Initialize the database:

```bash
flask shell
```

In the shell:
```python
from app import db
db.create_all()
exit()
```

7. Run the application:

```bash
python app.py
```

The application will be available at http://localhost:5000

## Docker Deployment

To run the application using Docker:

1. Build the Docker image:

```bash
docker build -t healthtrackerapp .
```

2. Run the container:

```bash
docker run -p 5000:5000 healthtrackerapp
```

Access the application at http://localhost:5000

## Usage

1. Register a new account
2. Complete your profile with personal details
3. Start tracking your health metrics:
   - Log your weight regularly
   - Record your meals and nutritional intake
   - Track your workouts and physical activities
   - Monitor your sleep patterns
4. Set health goals and track your progress
5. View your health dashboard with data visualizations

## Project Structure

```
healthtrackerapp/
├── app/
│   ├── models/        # Database models
│   ├── routes/        # Route definitions
│   ├── forms/         # Form classes
│   └── utils/         # Utility functions
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
├── tests/             # Test suite
├── .env               # Environment variables
├── app.py             # Application entry point
├── Dockerfile         # Docker configuration
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## License

MIT

## Contact

Your Name - your.email@example.com 
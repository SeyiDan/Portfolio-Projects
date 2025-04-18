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

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Database**: SQLite (development), configurable for PostgreSQL (production)
- **Authentication**: Flask-Login

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd HealthTrackerApp
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Access the application at http://localhost:8000

## Project Structure

```
HealthTrackerApp/
├── app/                # Application package
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── forms/          # Form classes
│   └── utils/          # Utility functions
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── app.py              # Application entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License.

## Contact

For more information, please contact me at oladejo.seyi2@gmail.com

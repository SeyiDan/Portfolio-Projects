# Portfolio Projects

This repository contains a collection of my software development projects that showcase my skills and expertise in web development, data analysis, and application development.

## Projects

### HealthTrackerApp
A Flask-based web application for tracking health metrics including sleep, nutrition, workouts, and weight. Users can set goals, track their progress, and monitor their health journey.

**Technologies**: Python, Flask, SQLAlchemy, HTML, CSS, JavaScript

### JobApplicationTracker
A comprehensive web application for tracking job applications, interviews, and offers. Users can manage their job search process, upload resumes and cover letters, and track progress with different companies.

**Technologies**: Python, Flask, SQLAlchemy, Bootstrap, HTML, CSS, JavaScript

### CodeCollaborationHub
A real-time code collaboration platform that allows developers to work together on coding projects. Features include real-time code sharing, chat functionality, and version control integration.

**Technologies**: Flask, SocketIO, SQLAlchemy, JavaScript, HTML, CSS

## Setup Instructions

Each project has its own setup instructions in their respective directories. Generally, you can set up any project by:

1. Navigate to the project directory:
   ```
   cd ProjectName
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

## Docker Support

The JobApplicationTracker project includes Docker support. To run it using Docker:

1. Navigate to the project directory:
   ```
   cd JobApplicationTracker
   ```

2. Build and start the Docker container:
   ```
   docker-compose up -d
   ```

3. Access the application at http://localhost:5000

## Port Configuration

Each application is configured to run on a different port to avoid conflicts:

- **HealthTrackerApp**: http://localhost:8000
- **JobApplicationTracker**: http://localhost:5000
- **CodeCollaborationHub**: http://localhost:8080

## Contact

For more information about these projects, please contact me at [your.email@example.com]. 
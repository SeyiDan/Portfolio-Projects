# Portfolio Projects

This repository contains a collection of my software development projects that showcase my skills and expertise in web development.

## Projects Overview

| Project | Description | Technologies | Port |
|---------|-------------|--------------|------|
| [HealthTrackerApp](./HealthTrackerApp) | A Flask-based application for tracking health metrics including sleep, nutrition, workouts, and weight. | Python, Flask, SQLAlchemy, HTML/CSS, JavaScript | 8000 |
| [JobApplicationTracker](./JobApplicationTracker) | A web application for managing job applications, interviews, and offers. | Python, Flask, SQLAlchemy, Bootstrap, HTML/CSS, JavaScript | 5000 |
| [CodeCollaborationHub](./CodeCollaborationHub) | A real-time code collaboration platform for developers to work together on coding projects. | Flask, SocketIO, SQLAlchemy, JavaScript, HTML/CSS | 8080 |

## Quick Start

Each project has its own detailed README with specific instructions. Generally, you can set up any project by:

1. Navigate to the project directory:
   ```
   cd ProjectName
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python app.py
   ```

## Docker Support

Both JobApplicationTracker and CodeCollaborationHub include Docker support:

```
cd ProjectName
docker-compose up -d
```

## Port Configuration

Each application is configured to run on a different port to avoid conflicts:

- HealthTrackerApp: http://localhost:8000
- JobApplicationTracker: http://localhost:5000
- CodeCollaborationHub: http://localhost:8080

## Contact

For more information about these projects, please contact me at oladejo.seyi2@gmail.com 
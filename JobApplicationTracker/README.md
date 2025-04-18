# Job Application Tracker

A web application to help job seekers track their job applications, interviews, and offers.

## Features

- **User Authentication**: Register, login, and manage profiles
- **Application Tracking**: Record and monitor application status
- **Document Management**: Upload and store resumes and cover letters
- **Interview Scheduling**: Track upcoming interviews
- **Company Information**: Store details about potential employers
- **Statistics**: View analytics on your job search progress

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (development), configurable for PostgreSQL (production)
- **Authentication**: Flask-Login

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Without Docker

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd JobApplicationTracker
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

7. Access the application at http://localhost:5000

### Setup With Docker

1. Navigate to the project directory:
   ```bash
   cd JobApplicationTracker
   ```

2. Build and run the container:
   ```bash
   docker-compose up -d
   ```

3. Access the application at http://localhost:5000

## Project Structure

```
JobApplicationTracker/
├── app/                # Application package
├── static/             # Static files (CSS, JS, uploads)
├── templates/          # HTML templates
├── app.py              # Main application file
├── application.py      # Alternative entry point for cloud deployments
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License.

## Contact

For more information, please contact me at oladejo.seyi2@gmail.com 
# Job Application Tracker

A web application to help job seekers track their job applications, interviews, and offers.

## Features

- Track job applications with detailed information
- Monitor application status (Applied, Interview, Offer, Rejected)
- Upload and store resumes and cover letters
- View company information
- Get statistics on your job search progress

## Installation

### Running without Docker

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python app.py
   ```
6. Open http://localhost:5000 in your browser

### Running with Docker

1. Clone this repository
2. Build and run the Docker container:
   ```
   docker-compose up -d
   ```
3. Open http://localhost:5000 in your browser

## Usage

1. Register for an account
2. Log in to your account
3. Add your job applications
4. Track the status of your applications
5. Add companies and interviews as needed

## Development

### Project Structure

- `app.py`: Main application file
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, uploads)
- `instance/`: SQLite database

### Technologies Used

- Flask: Web framework
- SQLAlchemy: Database ORM
- Flask-Login: Authentication
- Bootstrap: Frontend framework
- SQLite: Database

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
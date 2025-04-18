# CodeCollaborationHub

A real-time code collaboration platform that allows developers to work together on coding projects.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Project Management**: Create and manage coding projects
- **Real-time Collaboration**: Edit code together with multiple users simultaneously
- **Chat Functionality**: Communicate with team members in real-time
- **Version Control**: Integration with Git for version control
- **Code Highlighting**: Syntax highlighting for multiple programming languages
- **Discussion Forums**: Participate in coding discussions and share knowledge

## Technologies Used

- **Backend**: Python, Flask, SocketIO
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLAlchemy, PostgreSQL
- **Real-time Communication**: Flask-SocketIO
- **Authentication**: Flask-Login
- **Code Highlighting**: Pygments

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/CodeCollaborationHub.git
cd CodeCollaborationHub
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
DATABASE_URL=postgresql://username:password@localhost/codecollaborationhub
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

The application will be available at http://localhost:8080

## Docker Deployment

To run the application using Docker:

1. Build and start the containers using Docker Compose:

```bash
docker-compose up -d
```

2. Access the application at http://localhost:8080

## Usage

1. Register a new account
2. Create a new project or join an existing one
3. Invite collaborators to your project
4. Start coding together in real-time
5. Use the chat function to communicate with team members
6. Save and commit your changes to Git

## Project Structure

```
CodeCollaborationHub/
├── app/
│   ├── models/        # Database models
│   ├── routes/        # Route definitions
│   ├── static/        # Static files (CSS, JS)
│   ├── templates/     # HTML templates
│   └── __init__.py    # Application initialization
├── tests/             # Test suite
├── .env               # Environment variables
├── app.py             # Application entry point
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com 
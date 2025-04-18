# Code Collaboration Hub

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

### Setup Without Docker

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd CodeCollaborationHub
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

7. Access the application at http://localhost:8080

### Setup With Docker

1. Navigate to the project directory:
   ```bash
   cd CodeCollaborationHub
   ```

2. Build and run the containers:
   ```bash
   docker-compose up -d
   ```

3. Access the application at http://localhost:8080

## Project Structure

```
CodeCollaborationHub/
├── app/                # Application package
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   └── __init__.py     # Application initialization
├── tests/              # Test suite
├── app.py              # Application entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
└── README.md           # Project documentation
```

## License

This project is licensed under the MIT License.

## Contact

For more information, please contact me at oladejo.seyi2@gmail.com 
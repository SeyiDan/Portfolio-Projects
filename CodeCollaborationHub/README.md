# CodeCollaborationHub

A collaborative platform for developers to learn, share, and work together on coding projects.

## Features

- User authentication and profiles
- Project creation and management
- Real-time code collaboration
- Version control integration
- Discussion forums and commenting
- Language learning resources

## Technology Stack

- Python 3.9
- Flask web framework
- PostgreSQL database
- Docker for containerization

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CodeCollaborationHub.git
   cd CodeCollaborationHub
   ```

2. Start the application with Docker Compose:
   ```
   docker-compose up -d
   ```

3. Access the application at http://localhost:5000

### Development

To run the application in development mode:

```
docker-compose up
```

This will start the application with live reload enabled.

## Environment Variables

The following environment variables can be configured:

- `FLASK_APP`: Entry point to the Flask application
- `FLASK_ENV`: Application environment (development/production)
- `DATABASE_URL`: PostgreSQL connection string

## License

MIT 
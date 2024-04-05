# Learning Management System (LMS) Backend

Welcome to the Learning Management System (LMS) backend repository! This open-source project aims to provide a robust backend for managing courses, educational content, and student interactions.

## Features

- **Course Management**: Add, edit, and organize courses effortlessly.
- **User Authentication**: Secure user authentication and authorization.
- **API Endpoints**: Define API endpoints for course materials, student enrollment, assessments, and more.
- **Database Models**: Set up database models for users, courses, assignments, and grades.

## Getting Started

1. Clone this repository.
2. Install the required dependencies (`pip install poetry` `poetry install`).
3. Set up your database and configure settings (e.g., database connection, secret key).
4. Run the development server: `poetry run python manage.py runserver`.
5. Set up .env file: 
   (`FROM_EMAIL=<email-id>` 
    `MAILGUN_API_KEY=<add-api-key>` 
    `MAILGUN_SENDER_DOMAIN=<add-domain-url>`
   ).

## Contributing

We welcome contributions! If you'd like to contribute to this project, please follow our CONTRIBUTING guidelines.

## License

This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

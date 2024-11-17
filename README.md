# Custom Email-Sending Application
## Overview

This Django-based application was developed for BreakoutAI to streamline email communication and scheduling. It provides a user-friendly interface for managing bulk email campaigns, with real-time analytics and AI-driven content customization using the Gemini API.

## Features
1. Email Sending:

 - Supports bulk email sending from Google Sheets or CSV uploads.
 - Customizable email templates with dynamic placeholders.
3. Email Scheduling:
   
 - Schedule emails to be sent at specific times.
4. Google Sheets Integration:
   
 - Fetch email data directly from Google Sheets.
5. Throttling:
   
 - Ensure compliance with email rate limits.
6. Real-Time Analytics:
   
 - Track delivery status, bounce rates, and user engagement.
7. Dashboard Interface:
   
 - User-friendly dashboard for managing emails, templates, and schedules.

## Setup Instructions
#### Prerequisites
1.Python 3.10 or higher
2.Django 4.x
3.Virtual environment (recommended)
4.API keys for:
  - Gmail (or other email service provider)
  - Google Sheets API
  - Gemini API (for AI-driven email customization)

  ## Installation
### 1.Clone the Repository:
 
   git clone https://github.com/JyotikaJayani-08/custom-email-sender.git

   cd custom-email-sender
   
### 2.Set Up Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3.Install Dependencies:
pip install -r requirements.txt

### 4.Set Up .env File: Create a .env file in the email_app/ directory with the following:

EMAIL_HOST=smtp.gmail.com

EMAIL_PORT=587

EMAIL_HOST_USER=your_email@gmail.com

EMAIL_HOST_PASSWORD=your_password

SECRET_KEY=your_django_secret_key

GOOGLE_SHEETS_API_KEY=your_google_sheets_api_key


### 5. Run Migrations:
python manage.py migrate

### 6. Start the Development Server:
python manage.py runserver

## Usage

1. Access the Dashboard: Open the browser and navigate to http://127.0.0.1:8000/.

2. Upload CSV:
 
- Go to the Upload CSV page.
- Upload your file with columns like Email, Name, etc.

3. Fetch Data from Google Sheets:

- Provide the Google Sheets URL in the Fetch Data page.
- Authenticate using your API key.

5. Customize Emails:

- Navigate to Send Custom Emails.
- Use placeholders like {name} or {email} for dynamic content.

5.Schedule Emails:

- Go to Schedule Email.
- Select a date and time for sending.

6. Track Analytics:

- View delivery status and performance reports on the dashboard.

## Key Technologies :

- Backend: Django, Celery (for task scheduling)
- Frontend: HTML, CSS, JavaScript
- Email Service: SendGrid/Gmail API
- Database: SQLite (Development) / PostgreSQL (Production)
- External APIs: Google Sheets API, Gemini API

## Future Enhancements

- Add OAuth-based email account integration.
- Enhance analytics with graphs using Chart.js or Plotly.
- Add multi-language support for email templates.
- Improve the UI with a responsive framework (e.g., Bootstrap or Tailwind CSS).

## Acknowledgment

This project was developed for BreakoutAI as part of their assessment to improve and automate email workflows.

## License

This project is licensed under the MIT License.





   

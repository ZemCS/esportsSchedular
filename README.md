# eSports Planner

eSports Planner is a web application that allows users to track and receive notifications for upcoming matches of their favorite Valorant and League of Legends teams. It scrapes match data from popular eSports websites, sends email notifications, sets calendar reminders, and provides a user-friendly interface to select preferred teams.

## Features

- **Team Selection**: Choose your favorite Valorant and League of Legends teams via a React-based frontend.
- **Match Scraping**: Automatically scrapes match schedules from websites like vlr.gg and lolesports.com for selected teams.
- **Notifications**: Sends email notifications and desktop notifications for upcoming matches.
- **Calendar Integration**: Adds match events to your Google Calendar with reminders.
- **Backend API**: Flask-based backend to manage team preferences and serve data.
- **Authentication**: Uses Google OAuth2 for secure Gmail and Google Calendar integration.

## Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: Flask, Python
- **Scraping**: Selenium with Microsoft Edge WebDriver
- **APIs**: Google Gmail API, Google Calendar API
- **Libraries**: `requests`, `plyer`, `google-auth-oauthlib`, `googleapiclient`

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8+
- Node.js 16+
- Microsoft Edge browser
- Google Cloud Project with Gmail and Calendar APIs enabled
- Credentials file (`credentials.json`) for Google OAuth2

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/esports-planner.git
   cd esports-planner
   ```

2. **Backend Setup**:
   - Install Python dependencies:
     ```bash
     pip install flask flask-cors requests selenium plyer google-auth-oauthlib google-api-python-client
     ```
   - Place your Google API `credentials.json` in the `C:/Personal Projects/eSportsPlanner/` directory (or update the path in `server.py`).
   - Run the Flask backend:
     ```bash
     python app.py
     ```

3. **Frontend Setup**:
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Install Node.js dependencies:
     ```bash
     npm install
     ```
   - Start the React development server:
     ```bash
     npm start
     ```

4. **Run the Scraper**:
   - Ensure the Flask server is running.
   - Run the scraper script:
     ```bash
     python server.py
     ```

5. **Google API Configuration**:
   - Create a Google Cloud Project and enable the Gmail and Calendar APIs.
   - Download the OAuth2 credentials and save them as `credentials.json`.
   - The first time you run `server.py`, it will prompt you to authenticate via a browser to generate `token.json` and `calendarToken.json`.

## Usage

1. Open the frontend in your browser (default: `http://localhost:3000`).
2. Select your favorite Valorant and League of Legends teams using the checkboxes.
3. Click "Submit Teams" to save your preferences to the backend.
4. The scraper (`server.py`) will:
   - Fetch match data for your selected teams.
   - Send an email to the configured address with upcoming matches.
   - Create Google Calendar events with reminders.
   - Display a desktop notification with match details.

## File Structure

```
esports-planner/
├── app.py                 # Flask backend API
├── server.py              # Scraper and notification logic
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── ...            # Other frontend files
├── credentials.json       # Google API credentials (not included)
├── token.json             # Gmail API token (generated)
├── calendarToken.json     # Calendar API token (generated)
└── README.md              # This file
```

## Notes

- The scraper targets specific URLs for Valorant and League of Legends matches. Update the `urls` list in `server.py` to include other leagues or events.
- The application is configured to send emails to `znaeem164@gmail.com`. Update the `to` field in `sendMail()` in `server.py` to change the recipient.
- The scraper runs once per execution. To schedule it, consider using a task scheduler like `cron` or `Windows Task Scheduler`.
- Ensure the Microsoft Edge WebDriver is compatible with your browser version.

## Limitations

- The scraper relies on the structure of the target websites (vlr.gg, lolesports.com). Changes to their HTML may break the scraping logic.
- Desktop notifications require the `plyer` library and a supported notification system.
- The application assumes matches occur within a specific timezone (Asia/Karachi). Adjust the timezone in `createCalendarEvents()` in `server.py` as needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.

## License

This project is licensed under the MIT License.

import base64
import os
import time
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from plyer import notification
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

credentialsFile = "C:/Personal Projects/eSportsPlanner/credentials.json"
tokenFile = "C:/Personal Projects/eSportsPlanner/token.json"
calendarTokenFile = "C:/Personal Projects/eSportsPlanner/calendarToken.json"

scopes = ["https://www.googleapis.com/auth/gmail.send"]
calendarScopes = ["https://www.googleapis.com/auth/calendar.events"]


def authenticateGmail():
    creds = None
    if os.path.exists(tokenFile):
        creds = Credentials.from_authorized_user_file(tokenFile, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentialsFile, scopes)
            creds = flow.run_local_server(port=0)
        with open(tokenFile, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def authenticateCalendar():
    creds = None
    if os.path.exists(calendarTokenFile):
        with open(calendarTokenFile, "rb") as token:
            creds = Credentials.from_authorized_user_file(
                calendarTokenFile, calendarScopes
            )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsFile, calendarScopes
            )
            creds = flow.run_local_server(port=0)
        with open(calendarTokenFile, "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def sendMail(matches):
    try:
        service = authenticateGmail()
        message = MIMEText("\n".join(matches))
        message["to"] = "znaeem164@gmail.com"
        message["subject"] = "Upcoming Matches"
        encodedMessage = base64.urlsafe_b64encode(message.as_bytes()).decode()

        createMessage = {"raw": encodedMessage}
        sendMessage = (
            service.users().messages().send(userId="me", body=createMessage).execute()
        )
        print(f"Email sent: {sendMessage['id']}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def createCalendarEvents(service, summary, startTime, endTime):
    event = {
        "summary": summary,
        "start": {
            "dateTime": startTime,
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": endTime,
            "timeZone": "Asia/Karachi",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 30},
            ],
        },
    }
    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event['summary']} at {event['start']['dateTime']}")


def setCalendarReminders(matches):
    service = authenticateCalendar()
    for match in matches:
        try:
            matchDetails, matchTime = match.rsplit(" at ", 1)
            matchTime = f'{date.today().strftime("%B %d, %Y")} at {matchTime}'
            startTime = datetime.strptime(matchTime, "%B %d, %Y at %I:%M %p")
            endTime = startTime + timedelta(hours=1)
            createCalendarEvents(
                service, matchDetails, startTime.isoformat(), endTime.isoformat()
            )
        except ValueError as e:
            print(f"Failed to parse match time: {matchTime}: {e}")
        except Exception as e:
            print(f"Failed to create calendar event for: {matchDetails}: {e}")


def scrape():

    response = requests.get("http://127.0.0.1:5000/get-teams")

    data = response.json()

    listOfInterestedVlrTeams = data.get("vlrTeams", [])
    listOfInterestedLolTeams = data.get("lolTeams", [])

    driver = webdriver.Edge()

    matches = []

    urls = [
        "https://lolesports.com/en-US?leagues=lec&ignored=lta_n",
        "https://lolesports.com/en-US?leagues=lck&ignored=lta_n",
        "https://lolesports.com/en-US?leagues=nlc&ignored=lta_n",
        "https://www.vlr.gg/event/matches/2276/champions-tour-2025-emea-kickoff/?series_id=all",
        "https://www.vlr.gg/event/matches/2274/champions-tour-2025-americas-kickoff/?series_id=all",
    ]

    for url in urls:
        if "vlr.gg" in url:
            driver.get(url)

            time.sleep(2)

            if "americas" in url:
                currentDate = (
                    (date.today() + timedelta(days=1)).strftime("%B %d, %Y").lower()
                )
            else:
                currentDate = date.today().strftime("%B %d, %Y").lower()

            matchCalendar = driver.find_elements(By.CLASS_NAME, "wf-label.mod-large")

            for i, dates in enumerate(matchCalendar):
                matchDate = dates.text.strip().lower()
                if currentDate in matchDate:
                    nextDate = (
                        matchCalendar[i + 1] if i + 1 < len(matchCalendar) else None
                    )

                    sibling = dates.find_element(By.XPATH, "following-sibling::*")

                    while sibling != nextDate and sibling:
                        qualifyingMatches = sibling.find_elements(By.TAG_NAME, "a")
                        for qualifyingMatch in qualifyingMatches:
                            matchState = qualifyingMatch.find_element(
                                By.CSS_SELECTOR, "div.ml-status"
                            ).text.strip()
                            if matchState != "Completed":
                                teams = qualifyingMatch.find_elements(
                                    By.CSS_SELECTOR, "div.match-item-vs-team-name"
                                )

                                currentMatch = ""

                                matchTime = qualifyingMatch.find_element(
                                    By.CSS_SELECTOR, "div.match-item-time"
                                ).text.strip()

                                for i, team in enumerate(teams):
                                    currentMatch += team.text.strip()
                                    if i % 2 == 0:
                                        currentMatch += " vs "
                                    else:
                                        if "americas" in url:
                                            currentMatch = (
                                                "Valorant: "
                                                + currentMatch
                                                + " tonight at "
                                                + matchTime
                                            )
                                        else:
                                            currentMatch = (
                                                "Valorant: "
                                                + currentMatch
                                                + " at "
                                                + matchTime
                                            )
                                        for team in listOfInterestedVlrTeams:
                                            if team in currentMatch:
                                                matches.append(currentMatch)
                        try:
                            sibling = sibling.find_element(
                                By.XPATH, "following-sibling::*"
                            )
                        except:
                            break
        elif "lolesports.com" in url:
            driver.get(url)

            time.sleep(4)

            matchCalendar = driver.find_elements(
                By.CSS_SELECTOR,
                "section.bg_home\\.group.bdr-t_8.d_flex.p_200.mt_300.pos_relative.w_100\\%.smDown\\:bdr-t_0",
            )

            for i, dates in enumerate(matchCalendar):
                matchDate = dates.find_element(
                    By.CSS_SELECTOR, "h4.py_100.textStyle_title\\/md.smDown\\:py_0"
                ).text.strip()
                if matchDate == "Later Today":
                    nextDate = (
                        matchCalendar[i + 1] if i + 1 < len(matchCalendar) else None
                    )

                    sibling = dates.find_element(By.XPATH, "following-sibling::*")

                    while sibling != nextDate and sibling:
                        matchTime = " ".join(
                            sibling.find_element(By.TAG_NAME, "time")
                            .text.strip()
                            .split()
                        )

                        teams = sibling.find_elements(
                            By.CSS_SELECTOR,
                            "p.ai_center.d_inline-flex.ta_center.tt_uppercase",
                        )

                        currentMatch = ""

                        for i, team in enumerate(teams):
                            currentMatch += team.text.strip()
                            if i % 2 == 0:
                                currentMatch += " vs "
                            else:
                                currentMatch = (
                                    "League: " + currentMatch + " at " + matchTime
                                )
                                for team in listOfInterestedLolTeams:
                                    if team in currentMatch:
                                        matches.append(currentMatch)
                        try:
                            sibling = sibling.find_element(
                                By.XPATH, "following-sibling::*"
                            )
                        except:
                            break
    driver.quit()

    if matches == None:
        matches.append("No matches today.")

    notification.notify(
        title="Upcoming Matches", message="\n".join(matches), timeout=10
    )

    sendMail(matches)
    setCalendarReminders(matches)

    return matches


if __name__ == "__main__":
    scrape()

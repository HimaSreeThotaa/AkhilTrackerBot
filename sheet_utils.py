import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from collections import defaultdict

GOOGLE_SHEET_NAME = "AkhilTaskLog"

#Setup & Authentication
def connect_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        try:
            sheet = client.open(GOOGLE_SHEET_NAME).sheet1
            print(f"✅ Found existing sheet: {sheet.title}")
        except gspread.exceptions.SpreadsheetNotFound:
            sheet = client.create(GOOGLE_SHEET_NAME).sheet1
            print(f"📄 Created new sheet: {sheet.title}")
            sheet.append_row(["User ID", "Date", "Time", "Status", "Task"])  # Add headers

        return sheet
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        raise

#Log a new task entry
def log_task(user_id, status, task):
    sheet = connect_sheet()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    row = [user_id, date, time, status.lower(), task]
    sheet.append_row(row)
    print(f"📥 Logged: {row}")

#Daily Summary per user
def get_daily_summary(user_id):
    sheet = connect_sheet()
    today = datetime.now().strftime("%Y-%m-%d")
    records = sheet.get_all_records()

    done, progress, missed = [], [], []

    for row in records:
        if str(row["User ID"]) == str(user_id) and row["Date"] == today:
            status = row["Status"].lower()
            task = row["Task"]
            if status == "done":
                done.append(task)
            elif status == "progress":
                progress.append(task)
            elif status == "missed":
                missed.append(task)

    if not (done or progress or missed):
        return "📭 No tasks logged today!"

    summary = (
        f"📊 *Daily Summary for {today}*\n\n"
        f"✅ *Done* ({len(done)}):\n" + "\n".join(f"• {t}" for t in done) + "\n\n" +
        f"🟡 *In Progress* ({len(progress)}):\n" + "\n".join(f"• {t}" for t in progress) + "\n\n" +
        f"❌ *Missed* ({len(missed)}):\n" + "\n".join(f"• {t}" for t in missed)
    )

    return summary

#Weekly Summary + Streak
def get_weekly_summary(user_id):
    sheet = connect_sheet()
    records = sheet.get_all_records()
    today = datetime.now().date()
    summary = defaultdict(lambda: {"done": 0, "progress": 0, "missed": 0})
    streak = 0

    for row in records:
        try:
            uid = str(row["User ID"])
            date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
            status = row["Status"].lower()

            if uid == str(user_id) and (today - date).days < 7:
                summary[str(date)][status] += 1
        except:
            continue

    for i in range(7):
        date = today - timedelta(days=i)
        day_summary = summary.get(str(date), {})
        if day_summary.get("done", 0) > 0:
            streak += 1
        else:
            break

    return summary, streak

#Multi-user support
def get_all_user_ids():
    sheet = connect_sheet()
    values = sheet.get_all_values()
    user_ids = set()
    for row in values[1:]:  # Skip header row
        if row and row[0]:
            user_ids.add(row[0])
    return list(user_ids)

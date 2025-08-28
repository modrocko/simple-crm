#!/usr/bin/env python3
import os, sys, subprocess
from datetime import datetime, date


# Escape quotes for AppleScript
def esc(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


# Convert text to date
def parse_day(s: str):
    if not s:
        return None
    s = s.strip()
    fmts = []
    fmts += ["%Y-%m-%d", "%m/%d/%Y", "%b %d %Y"]  # ISO, US slashes, Text month
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# Create reminder in reminders app
def make_reminder(title: str, due_day: date):
    mac = due_day.strftime("%B %d, %Y")
    script = f'''
    tell application "Reminders"
        make new reminder with properties {{name:"{esc(title)}", allday due date:(date "{esc(mac)}")}}
    end tell'''
    subprocess.run(["osascript", "-e", script], check=False)


# Check if calendar exists
def is_cal_name_valid(cal_name: str) -> bool:
    check_script = f'tell application "Calendar" to return (exists calendar "{esc(cal_name)}")'
    result = subprocess.run(
        ["osascript", "-e", check_script], capture_output=True, text=True
    )
    if result.stdout.strip().lower() == "true":
        return True
    else:
        notify(f"Calendar '{cal_name}' not found")
        return False


# Create calendar event
def make_event(title: str, due_day: date):
    y = due_day.year
    m = due_day.strftime("%B")   # e.g. August
    d = due_day.day

    cal_name = os.environ.get("reminder_calendar", "")

    if not is_cal_name_valid(cal_name):
        sys.exit(0)

    notify("Adding calendar event...")

    script = f'''
    tell application "Calendar"
        set theCal to calendar "{esc(cal_name)}"
        set startDate to current date
        set year of startDate to {y}
        set month of startDate to {m}
        set day of startDate to {d}
        set time of startDate to (6 * hours)
        set endDate to startDate + (0 * minutes)
        tell theCal
            make new event at end of events with properties {{summary:"{esc(title)}", start date:startDate, end date:endDate}}
        end tell
    end tell'''
    subprocess.run(["osascript", "-e", script], check=False)



# Show macOS notification
def notify(msg: str):
    title = os.environ["alfred_workflow_name"]
    subprocess.run(
        ["osascript","-e",f'display notification "{esc(msg)}" with title "{esc(title)}"'], check=False
    )



# Run workflow logic
def main():
    title = os.environ["alfred_workflow_name"]
    name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    full_title = f"Ping {name} ({title})"

    # must have a day
    due_raw = os.environ["next_action_date"]
    if not due_raw:
        sys.exit(0)

    due_day = parse_day(due_raw)
    if not due_day:
        sys.exit(0)

    target = os.environ.get("reminder_type", "reminder").lower()
    if target == "event":
        make_event(full_title, due_day)
        notify(f"Added calendar event for {name}")
    else:
        make_reminder(full_title, due_day)
        notify(f"Added reminder for {name}")

if __name__ == "__main__":
    main()

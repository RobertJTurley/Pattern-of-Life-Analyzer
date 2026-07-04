import os
import shutil
import sqlite3
import datetime
import csv

browsers = {
    "Google Chrome": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History",
    "Microsoft Edge": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History",
    "Brave": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\History"
}

print("Initiating Multi-Browser Triage and CSV Export...\n")
print("=" * 75)

# 1. Define the name of our final evidence report
report_file = "Forensic_Web_History_Report.csv"

# 2. Open the CSV file and get it ready for writing
with open(report_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the column headers at the very top of the document
    csv_writer.writerow(["Browser", "Timestamp", "Visit Count", "URL", "Page Title"])

    for browser_name, path in browsers.items():
        live_path = os.path.expandvars(path)
        safe_copy_path = f"Triage_{browser_name.replace(' ', '_')}.db"

        if not os.path.exists(live_path):
            print(f"[-] {browser_name} not found. Skipping...")
            continue

        print(f"[+] Extracting {browser_name} history to CSV...")

        try:
            shutil.copy2(live_path, safe_copy_path)
        except PermissionError:
            print(f"[!] Permission denied for {browser_name}. Ensure it is fully closed.")
            continue

        connection = sqlite3.connect(safe_copy_path)
        cursor = connection.cursor()
        query = "SELECT url, title, visit_count, last_visit_time FROM urls"
        
        try:
            cursor.execute(query)
            
            for row in cursor.fetchall():
                url = row[0]
                title = row[1]
                visit_count = row[2]
                webkit_timestamp = row[3]
                
                if webkit_timestamp > 0:
                    unix_time = (webkit_timestamp / 1000000) - 11644473600
                    readable_date = datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    readable_date = "Unknown Time"
                    
                # 3. WRITE THE DATA TO THE FILE INSTEAD OF THE SCREEN
                # We put the variables in brackets to tell Python they are separate columns
                csv_writer.writerow([browser_name, readable_date, visit_count, url, title])
                
        except sqlite3.DatabaseError:
            print(f"[!] Could not read the database for {browser_name}.")
            
        connection.close()

print("=" * 75)
print(f"Extraction complete! Evidence saved to: {report_file}")
input("Press Enter to exit...")

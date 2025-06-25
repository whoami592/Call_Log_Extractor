import sqlite3
import datetime
import sys
import os

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║         CALL LOG EXTRACTOR                           ║
    ║         Coded by Pakistani Ethical Hacker            ║
    ║         Mr. Sabaz Ali Khan                          ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def extract_call_logs(db_path):
    try:
        # Connect to the call log database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to extract call logs
        cursor.execute("""
            SELECT 
                number,
                date,
                duration,
                type,
                name
            FROM calls
        """)

        # Fetch all call records
        call_logs = cursor.fetchall()

        # Print extracted call logs
        print("\nExtracted Call Logs:")
        print("-" * 50)
        print(f"{'Number':<20} {'Date':<25} {'Duration':<10} {'Type':<10} {'Name':<20}")
        print("-" * 50)

        for log in call_logs:
            number, date_ms, duration, call_type, name = log
            
            # Convert timestamp to readable date
            date = datetime.datetime.fromtimestamp(date_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            
            # Convert call type to readable format
            call_type_str = {1: "Incoming", 2: "Outgoing", 3: "Missed"}.get(call_type, "Unknown")
            
            # Handle None values for name
            name = name if name else "Unknown"
            
            print(f"{number:<20} {date:<25} {duration:<10} {call_type_str:<10} {name:<20}")

        # Close the database connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print_banner()
    
    if len(sys.argv) != 2:
        print("Usage: python call_log_extractor.py <path_to_call_db>")
        print("Note: This script requires access to the Android call log database")
        sys.exit(1)

    db_path = sys.argv[1]
    
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found")
        sys.exit(1)

    print(f"Extracting call logs from: {db_path}")
    extract_call_logs(db_path)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import csv
import datetime
import os
from tabulate import tabulate

LOG_FILE = "woody_logs.csv"

def initialize_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Category", "Description"])

def add_log(category, description):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, category, description])
    print(f"Log entry added: {timestamp}, {category}, {description}")

def edit_log(index, category, description):
    logs = read_logs()
    if 0 <= index < len(logs):
        logs[index]["Category"] = category
        logs[index]["Description"] = description
        write_logs(logs)
        print(f"Log entry {index} edited.")
    else:
        print(f"Log entry {index} does not exist.")

def delete_log(index):
    logs = read_logs()
    if 0 <= index < len(logs):
        del logs[index]
        write_logs(logs)
        print(f"Log entry {index} deleted.")
    else:
        print(f"Log entry {index} does not exist.")

def view_logs(category=None):
    logs = read_logs()
    if category:
        logs = [log for log in logs if log["Category"] == category]
    print(tabulate(logs, headers="keys", tablefmt="grid"))

def generate_report():
    logs = read_logs()
    categories = set(log["Category"] for log in logs)
    report = {category: 0 for category in categories}
    for log in logs:
        report[log["Category"]] += 1
    print("Log Report:")
    for category, count in report.items():
        print(f"{category}: {count} entries")

def read_logs():
    with open(LOG_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_logs(logs):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "Category", "Description"])
        writer.writeheader()
        writer.writerows(logs)

def main():
    initialize_log_file()

    parser = argparse.ArgumentParser(description="Woody: A general-purpose logging script")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new log entry")
    add_parser.add_argument("category", help="Category of the log entry")
    add_parser.add_argument("description", help="Description of the log entry")

    edit_parser = subparsers.add_parser("edit", help="Edit an existing log entry")
    edit_parser.add_argument("index", type=int, help="Index of the log entry to edit")
    edit_parser.add_argument("category", help="New category of the log entry")
    edit_parser.add_argument("description", help="New description of the log entry")

    delete_parser = subparsers.add_parser("delete", help="Delete a log entry")
    delete_parser.add_argument("index", type=int, help="Index of the log entry to delete")

    view_parser = subparsers.add_parser("view", help="View log entries")
    view_parser.add_argument("--category", help="Category to filter log entries")

    report_parser = subparsers.add_parser("report", help="Generate a log report")

    args = parser.parse_args()

    if args.command == "add":
        add_log(args.category, args.description)
    elif args.command == "edit":
        edit_log(args.index, args.category, args.description)
    elif args.command == "delete":
        delete_log(args.index)
    elif args.command == "view":
        view_logs(args.category)
    elif args.command == "report":
        generate_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

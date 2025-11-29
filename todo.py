#!/usr/bin/env python3
"""
Simple terminal To-Do list.

Usage examples:
  python todo.py add "Buy milk"
  python todo.py add "Call Alice" -d 2025-11-30 -t 18:00
  python todo.py list
  python todo.py list --all
  python todo.py done 2
  python todo.py delete 3
  python todo.py clear --completed
"""

import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

DEFAULT_STORE = os.path.expanduser("~/.todo_cli.json")


def load_tasks(path: str = DEFAULT_STORE) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If file is corrupted, don't crash
        return []


def save_tasks(tasks: List[Dict[str, Any]], path: str = DEFAULT_STORE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def next_id(tasks: List[Dict[str, Any]]) -> int:
    return (max((t["id"] for t in tasks), default=0) + 1) if tasks else 1


def format_task(task: Dict[str, Any]) -> str:
    status = "✔" if task.get("completed") else " "
    idx = task.get("id")
    title = task.get("title", "")
    due = task.get("due") or ""
    created = task.get("created_at", "")[:10]
    return f"[{status}] {idx:3d}. {title}  (created {created}{f', due {due}' if due else ''})"


def cmd_add(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    task_id = next_id(tasks)

    due_str = ""
    if args.date or args.time:
        # Build ISO-like string "YYYY-MM-DD HH:MM"
        date_part = args.date or datetime.now().strftime("%Y-%m-%d")
        time_part = args.time or "00:00"
        due_str = f"{date_part} {time_part}"

    new_task = {
        "id": task_id,
        "title": args.title,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed_at": "",
        "due": due_str,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Added:")
    print(" ", format_task(new_task))


def cmd_list(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Use `todo.py add \"Your task\"` to add one.")
        return

    if not args.all:
        # filter to only active tasks
        tasks = [t for t in tasks if not t.get("completed")]

    if args.sort == "created":
        tasks.sort(key=lambda t: t.get("created_at", ""))
    elif args.sort == "due":
        tasks.sort(key=lambda t: t.get("due") or "9999-12-31 23:59")

    print()
    print("To-Do List")
    print("----------")
    for t in tasks:
        print(format_task(t))

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    print()
    print(f"Total shown: {total} | Completed in file: {completed}")


def find_task(tasks: List[Dict[str, Any]], task_id: int) -> Dict[str, Any]:
    for t in tasks:
        if t.get("id") == task_id:
            return t
    return {}


def cmd_done(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if not task:
        print(f"No task with id {args.id}.")
        return
    if task.get("completed"):
        print("Task already marked as done:")
        print(" ", format_task(task))
        return
    task["completed"] = True
    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_tasks(tasks)
    print("Marked as done:")
    print(" ", format_task(task))


def cmd_undone(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if not task:
        print(f"No task with id {args.id}.")
        return
    if not task.get("completed"):
        print("Task is already active:")
        print(" ", format_task(task))
        return
    task["completed"] = False
    task["completed_at"] = ""
    save_tasks(tasks)
    print("Marked as active again:")
    print(" ", format_task(task))


def cmd_delete(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t.get("id") != args.id]
    if len(tasks) == before:
        print(f"No task with id {args.id}.")
        return
    save_tasks(tasks)
    print(f"Deleted task {args.id}.")


def cmd_clear(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    if args.completed:
        before = len(tasks)
        tasks = [t for t in tasks if not t.get("completed")]
        removed = before - len(tasks)
        save_tasks(tasks)
        print(f"Removed {removed} completed task(s).")
    elif args.all:
        confirm = input("This will delete ALL tasks. Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            save_tasks([])
            print("All tasks deleted.")
        else:
            print("Aborted.")
    else:
        print("Specify --completed or --all.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple terminal To-Do list (stored in ~/.todo_cli.json)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description, in quotes if it has spaces")
    p_add.add_argument("-d", "--date", help="Due date (YYYY-MM-DD)", default=None)
    p_add.add_argument("-t", "--time", help="Due time (HH:MM, 24h)", default=None)
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument(
        "--all",
        action="store_true",
        help="Show all tasks (default shows only active tasks)",
    )
    p_list.add_argument(
        "--sort",
        choices=["created", "due"],
        default="created",
        help="Sort tasks by created or due time",
    )
    p_list.set_defaults(func=cmd_list)

    # done
    p_done = sub.add_parser("done", help="Mark task as completed")
    p_done.add_argument("id", type=int, help="Task id")
    p_done.set_defaults(func=cmd_done)

    # undone
    p_undone = sub.add_parser("undone", help="Mark a completed task as active again")
    p_undone.add_argument("id", type=int, help="Task id")
    p_undone.set_defaults(func=cmd_undone)

    # delete
    p_del = sub.add_parser("delete", help="Delete a task by id")
    p_del.add_argument("id", type=int, help="Task id")
    p_del.set_defaults(func=cmd_delete)

    # clear
    p_clear = sub.add_parser("clear", help="Clear tasks")
    p_clear_group = p_clear.add_mutually_exclusive_group(required=True)
    p_clear_group.add_argument(
        "--completed", action="store_true", help="Remove only completed tasks"
    )
    p_clear_group.add_argument(
        "--all", action="store_true", help="Remove all tasks"
    )
    p_clear.set_defaults(func=cmd_clear)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


📝 Local To-Do List App

A simple and clean To-Do List web app that runs directly on your local machine. No backend, no installation, no accounts. Your tasks are saved automatically in your browser using localStorage.

This project includes:

- Add tasks with title, date, and time
- Mark tasks as completed
- Filter by All / Active / Completed
- Clear completed tasks
- Automatic saving in browser
- 100% offline and private

📁 Project Structure

```pgsql
todo-app/
│
├── index.html
├── style.css
└── script.js
```

🚀 How to Run

Option 1: Open in Browser (recommended)

- Download or clone this repository
- Open index.html by double-clicking
- Start adding tasks

Option 2: Run with a Local Server

Using Python:
```bash
python -m http.server 8000
```

Then open
```arduino
http://localhost:8000
```

✨ Features
✔ Add Tasks

Enter a task name, an optional due date, and optional due time.
Tasks appear instantly.

✔ Auto-Saving

Everything saves to localStorage.
Your tasks stay even after refresh or browser restart.

✔ Filters

- All
- Active
- Completed

✔ Mark Complete / Delete

Click checkbox → mark done
Click Delete → remove task

✔ Clear Completed

One click removes all completed tasks.

✔ Clean UI

Responsive and minimal interface designed to be easy and comfortable to use.

🧩 Code Overview

index.html

Defines the user interface layout.

style.css

Handles the responsive layout, theme, and component styling.

script.js

Implements:

- Task creation
- Task storage (localStorage)
- Rendering
- Filtering
- Completion logic
- Deletion
- Cleanup

Tasks are stored as:

```json
{
  "id": 1732561812345,
  "title": "Finish documentation",
  "dueDate": "2025-11-30",
  "dueTime": "18:00",
  "completed": false
}
```
🛡 Privacy

All data stays in your browser.
Nothing is uploaded anywhere.

📄 License

MIT License — free to use, modify, and build upon.

🙌 Contributions

Pull requests and improvement suggestions are welcome!

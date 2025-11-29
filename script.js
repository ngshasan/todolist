// Simple To-Do app using localStorage

const STORAGE_KEY = "todo_tasks_v1";

let tasks = [];
let currentFilter = "all"; // all | active | completed

// ---- DOM elements ----
const taskTitleInput = document.getElementById("taskTitle");
const taskDueInput = document.getElementById("taskDue");
const taskTimeInput = document.getElementById("taskTime");
const addTaskBtn = document.getElementById("addTaskBtn");
const taskListEl = document.getElementById("taskList");
const filterButtons = document.querySelectorAll(".filter-btn");
const clearCompletedBtn = document.getElementById("clearCompletedBtn");

// ---- Load tasks from localStorage on startup ----
function loadTasks() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      tasks = JSON.parse(saved);
    } else {
      tasks = [];
    }
  } catch (e) {
    console.error("Failed to load tasks:", e);
    tasks = [];
  }
}

// ---- Save tasks to localStorage ----
function saveTasks() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

// ---- Render tasks ----
function renderTasks() {
  taskListEl.innerHTML = "";

  let visibleTasks = tasks;
  if (currentFilter === "active") {
    visibleTasks = tasks.filter((t) => !t.completed);
  } else if (currentFilter === "completed") {
    visibleTasks = tasks.filter((t) => t.completed);
  }

  if (visibleTasks.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No tasks.";
    li.style.color = "#9ca3af";
    li.style.fontSize = "0.9rem";
    taskListEl.appendChild(li);
    return;
  }

  visibleTasks.forEach((task) => {
    const li = document.createElement("li");
    li.className = "task-item";

    const left = document.createElement("div");
    left.className = "task-left";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.addEventListener("change", () => toggleTask(task.id));

    const titleWrapper = document.createElement("div");

    const title = document.createElement("div");
    title.className = "task-title";
    title.textContent = task.title;
    if (task.completed) {
      title.classList.add("completed");
    }

    titleWrapper.appendChild(title);

    if (task.dueDate) {
      const meta = document.createElement("div");
      meta.className = "task-meta";
      meta.textContent = `Due: ${task.dueDate}`;
      titleWrapper.appendChild(meta);
    }

    left.appendChild(checkbox);
    left.appendChild(titleWrapper);

    const actions = document.createElement("div");
    actions.className = "task-actions";

    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.addEventListener("click", () => deleteTask(task.id));

    actions.appendChild(delBtn);

    li.appendChild(left);
    li.appendChild(actions);

    taskListEl.appendChild(li);
  });
}

// ---- Add a new task ----
function addTask() {
  const title = taskTitleInput.value.trim();
  const due = taskDueInput.value;

  if (!title) {
    alert("Please enter a task.");
    return;
  }

  const newTask = {
    id: Date.now(), // simple unique id
    title,
    dueDate: due || "",
    completed: false,
  };

  tasks.unshift(newTask); // add to top
  saveTasks();
  renderTasks();

  taskTitleInput.value = "";
  taskDueInput.value = "";
  taskTitleInput.focus();
}

// ---- Toggle task completion ----
function toggleTask(id) {
  tasks = tasks.map((t) =>
    t.id === id ? { ...t, completed: !t.completed } : t
  );
  saveTasks();
  renderTasks();
}

// ---- Delete a task ----
function deleteTask(id) {
  tasks = tasks.filter((t) => t.id !== id);
  saveTasks();
  renderTasks();
}

// ---- Clear completed tasks ----
function clearCompleted() {
  const hasCompleted = tasks.some((t) => t.completed);
  if (!hasCompleted) return;

  if (!confirm("Delete all completed tasks?")) {
    return;
  }
  tasks = tasks.filter((t) => !t.completed);
  saveTasks();
  renderTasks();
}

// ---- Change filter ----
function setFilter(filter) {
  currentFilter = filter;
  filterButtons.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === filter);
  });
  renderTasks();
}

// ---- Event listeners ----
addTaskBtn.addEventListener("click", addTask);

taskTitleInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    addTask();
  }
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => setFilter(btn.dataset.filter));
});

clearCompletedBtn.addEventListener("click", clearCompleted);

// ---- Init ----
loadTasks();
renderTasks();


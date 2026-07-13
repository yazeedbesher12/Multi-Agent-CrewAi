# Simple Task Management Web App for University Students  
## Executive Summary  
This project outlines a lightweight task management web app designed for university students, emphasizing simplicity and functionality. The app allows users to add, edit, delete, and mark tasks as completed. The proposed technology stack prioritizes open-source tools, minimal infrastructure, and offline-first capabilities while avoiding complex setups like payments, AI, or distributed systems. The 2-week implementation plan focuses on incremental progress, starting with frontend development and optionally building backend integrations for synchronization.  

---

## Requirements  
### Core Features  
- Add tasks (title, description, due date).  
- Edit existing tasks.  
- Delete tasks.  
- Mark tasks as completed.  

### User Experience  
- Lightweight and distraction-free interface.  
- Accessible design for mobile and desktop.  
- Offline functionality via browser-local storage.  

### Technical Constraints  
- No payments or AI integrations.  
- No complex infrastructure (e.g., databases, microservices).  
- Cross-device compatibility without requiring synchronization.  

---

## Recommended Technology Stack  
| **Category**       | **Tools**                                  | **Rationale**                              |  
|---------------------|--------------------------------------------|--------------------------------------------|  
| **Frontend**        | HTML5, CSS3, Vanilla JavaScript (JS)       | Zero dependencies; easy to learn/deploy.   |  
| **Storage**         | `localStorage`                             | Offline-first; no backend required.        |  
| **Build/Hosting**   | Vercel/Netlify (static hosting), Vite.js   | Free tiers available; rapid deployment.    |  
| **Optional Backend**| Node.js, Express.js (for future scaling)   | Simple API layer for cross-device sync.    |  

---

## System Architecture  
### Component Responsibilities  
1. **Frontend (`client/`)**:  
   - Renders the UI (task list, input forms, buttons).  
   - Handles user interactions (e.g., clicking "Mark Completed").  
   - Stores task data in `localStorage` (key-based task ID).  

2. **Backend (Optional: `server/`)**:  
   - Node.js + Express.js server to handle API requests (if syncing across devices).  
   - Uses JSON files (`tasks.json`) as a lightweight data store.  

3. **Hosting**:  
   - Frontend: Deployed to Vercel/Netlify for static hosting.  
   - Backend: Optional deployment via Vercel or local testing with `nodemon`.  

### Interaction Flow  
1. **Frontend Interaction**:  
   - User clicks "Add Task" → Frontend generates a unique ID and saves data to `localStorage`.  
   - Task list re-renders dynamically via JavaScript.  

2. **Backend Integration (Optional)**:  
   - Server syncs tasks to `tasks.json` via Express.js routes (`/tasks`).  
   - Frontend fetches tasks from the backend using `fetch()` during initialization.  

---

## Implementation Roadmap  
### Week 1: Frontend Development  
**Day 1–2**  
- Set up project structure:  
  ```plaintext  
  task-manager/  
  ├── index.html  
  ├── style.css  
  └── app.js  
  ```  
- Design responsive UI with HTML/CSS:  
  - Task list (dynamic `<ul>` element).  
  - Form for adding tasks (title, description, due date).  

**Day 3–5**  
- Implement core functionality in `app.js`:  
  ```javascript  
  // LocalsStorage CRUD operations  
  const saveTask = (task) => {  
    const tasks = JSON.parse(localStorage.getItem("tasks")) || [];  
    tasks.push(task);  
    localStorage.setItem("tasks", JSON.stringify(tasks));  
  };  

  // Render tasks  
  const renderTasks = () => {  
    const tasks = JSON.parse(localStorage.getItem("tasks")) || [];  
    const ul = document.getElementById("task-list");  
    ul.innerHTML = tasks  
      .map(task =>  
        `<li class="${task.completed ? 'completed' : ''}" data-id="${task.id}">  
          <input type="checkbox">  
          <span>${task.title}</span>  
          <button onclick="deleteTask('${task.id}')">Delete</button>  
        </li>`  
      )  
      .join("");  
  };  
  ```  

**Day 6–7**  
- Add edit/delete features:  
  - Clicking "Edit" opens a modal/form for updates.  
  - LocalStorage updated real-time on interaction.  

**Day 8–10**  
- Add UI polish (hover effects, mobile responsiveness).  
- Basic QA testing (cross-browser compatibility).  

---  

### Week 2: Backend & Deployment  
**Day 15–16**  
- Initialize backend with Node.js/Express:  
  ```javascript  
  // server/app.js  
  const express = require("express");  
  const fs = require("fs");  
  const app = express();  
  app.use(express.json());  

  // Read tasks from tasks.json  
  app.get("/tasks", (req, res) => {  
    res.send(JSON.parse(fs.readFileSync("tasks.json", "utf8")));  
  });  

  // Save tasks to JSON file  
  app.post("/tasks", (req, res) => {  
    const tasks = JSON.parse(fs.readFileSync("tasks.json", "utf8"));  
    tasks.push(req.body);  
    fs.writeFileSync("tasks.json", JSON.stringify(tasks));  
    res.sendStatus(201);  
  });  
  ```  

**Day 17–18**  
- Integrate frontend with backend:  
  ```javascript  
  // Fetch tasks on load  
  document.addEventListener("DOMContentLoaded", () => {  
    fetch("/tasks")  
      .then(response => response.json())  
      .then(renderTasks);  
  });  
  ```  

**Day 19–20**  
- Deploy frontend via Vercel.  
- (Optional) Deploy backend to a serverless function via Vercel.  

**Day 21–22**  
- Final testing (edge cases: empty storage, rapid edits).  
- Documentation generation (README.md, usage guide).  

---  

## Testing Plan  
- **Unit Testing**: Manual validation of CRUD operations.  
- **Integration Testing**:  
  - Verify `localStorage` persistence.  
  - Test API calls (if backend is implemented).  
- **User Testing**: 3–5 students to validate usability.  

---

## Risks & Mitigation  
| **Risk**                     | **Impact**                   | **Mitigation**                     |  
|------------------------------|------------------------------|------------------------------------|  
| Data loss on browser close   | Low user confidence          | Auto-save tasks via periodic sync. |  
| Lack of cross-device sync    | Reduced usability            | Backend sync (optional integration).|  
| Styling inconsistencies      | Unpolished UI                | Use CSS variables for theming.     |  

---

## Practical Alternatives  
- **Sync Requirement**: Replace `localStorage` with **Firebase Realtime Database** (free tier available) for cross-device sync.  
- **UI Enhancements**: Use **React + Tailwind CSS** for faster component development.  

---

## Final Recommendations  
- **MVP Focus**: Prioritize frontend features in Week 1; backend sync is optional.  
- **Post-Launch**: Expand with notifications, category tags, or dark mode.  
- **Cost**: $0 (free tools: Vercel, Node.js, localStorage).  

This plan ensures a functional, student-friendly app built within 2 weeks using minimalistic tooling.

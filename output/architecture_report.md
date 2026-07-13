# System Architecture & Implementation Plan: Student Task Manager

## Executive Summary
This document outlines the professional system design and implementation roadmap for a **Simple Task Management Web App** tailored for university students. The objective is to deliver a functional, high-quality MVP (Minimum Viable Product) within a **2-week development cycle** using a **zero-cost, low-complexity technology stack**. 

By leveraging a "Hypermedia-driven" architecture (Flask + HTMX), we eliminate the overhead of complex JavaScript frameworks and separate API/Frontend build pipelines, ensuring the project remains maintainable by a student team with minimal DevOps experience.

---

## 1. Project Requirements & Scope

### 1.1 Functional Requirements
*   **User Authentication:** Secure registration, login, and logout functionality.
*   **Task CRUD Operations:** 
    *   **Create:** Add tasks with title, description, and due date.
    *   **Read:** View a personalized list of tasks.
    *   **Update:** Edit task details or toggle "completed" status.
    *   **Delete:** Remove tasks from the list.
*   **Task Filtering:** Ability to view tasks by status (All, Active, Completed).
*   **Responsive UI:** Seamless operation on both desktop laptops and mobile smartphones.

### 1.2 Non-Functional Requirements
*   **Zero Cost:** Use only free-tier or open-source software.
*   **Minimal Infrastructure:** No Docker, Kubernetes, or complex CI/CD pipelines required.
*   **Maintainability:** High-level readability and minimal moving parts.
*   **Security:** Implementation of password hashing and CSRF protection.

---

## 2. Recommended Technology Stack

After analyzing various candidates, the **Flask + HTMX** stack was selected as the optimal solution for speed, cost, and simplicity.

| Layer | Technology | Role | Rationale |
| :--- | :--- | :--- | :--- |
| **Frontend** | **HTMX** | Dynamic Updates | Allows partial page updates (AJAX) via HTML attributes; eliminates the need for React/Vue. |
| **Frontend** | **Tailwind CSS** | Styling | Utility-first CSS allows rapid UI building without writing custom CSS files. |
| **Frontend** | **Alpine.js** | Micro-reactivity | Handles tiny client-side logic (e.g., opening a modal) without a heavy framework. |
| **Backend** | **Flask (Python)** | Logic & Routing | A micro-framework that provides the bare essentials, perfect for rapid prototyping. |
| **Database** | **PostgreSQL** | Data Persistence | Robust relational database; easily available on free tiers (Render/Railway). |
| **ORM** | **SQLAlchemy** | DB Management | Simplifies database queries and makes switching from SQLite (dev) to Postgres (prod) trivial. |
| **Hosting** | **Render** | Deployment | Supports Python/Flask out-of-the-box with a generous free tier. |

---

## 3. System Architecture

### 3.1 Architectural Pattern: Server-Side Rendering (SSR) with Hypermedia
Unlike a modern Single Page Application (SPA) which communicates via JSON, this system uses **Hypermedia**. When a user clicks "Complete Task," HTMX sends an AJAX request, and the Flask server returns a **snippet of HTML** representing only the updated task row. HTMX then swaps that snippet into the existing page.

### 3.2 Component Diagram (Logical)
```text
[ User Browser ]
       |
       | (HTTP Requests: GET/POST/DELETE)
       v
[ Flask Web Server ] <---> [ SQLAlchemy ORM ] <---> [ PostgreSQL DB ]
       |
       | (Returns HTML Fragments)
       v
[ HTMX Engine ] <--- [ Alpine.js (for UI state) ]
```

### 3.3 Component Responsibilities
*   **Web Server (Flask):** Manages routing, session handling (Flask-Login), and business logic.
*   **Templates (Jinja2):** Generates HTML content on the server side.
*   **HTMX (Client):** Intercepts specific clicks/submits to perform asynchronous updates without page reloads.
*   **Database (PostgreSQL):** Maintains persistent storage for users and tasks.

---

## 4. Implementation Roadmap (2-Week Sprint)

### Week 1: Core Infrastructure & Authentication
*Goal: Establish a working environment and secure user access.*

*   **Day 1-2: Scaffolding**
    *   Initialize Git repository.
    *   Set up Python Virtual Environment (`venv`).
    *   Configure Flask basic routing and Tailwind CSS via CDN or CLI.
    *   Setup SQLAlchemy models for `User` and `Task`.
*   **Day 3-4: Identity Management**
    *   Implement Registration and Login forms using `Flask-WTF`.
    *   Integrate `Flask-Bcrypt` for secure password hashing.
    *   Implement `Flask-Login` to manage user sessions.
*   **Day 5-7: Basic Task CRUD (The "Read" and "Create" phase)**
    *   Develop the main Dashboard view (List all tasks for logged-in user).
    *   Implement the "Add Task" functionality.
    *   **Milestone:** A user can log in and see an empty task list.

### Week 2: Dynamic Interaction & Polishing
*Goal: Enable seamless updates and prepare for deployment.*

*   **Day 8-10: Dynamic CRUD (The "HTMX" phase)**
    *   Implement "Toggle Complete" using HTMX (replaces the row with a "strikethrough" version).
    *   Implement "Delete" (removes the row from DOM upon server confirmation).
    *   Implement "Edit" via an inline form (swapping a text span for an input field).
*   **Day 11-12: UI/UX & Responsiveness**
    *   Apply Tailwind CSS classes to ensure mobile responsiveness.
    *   Add Alpine.js for small interactions (e.g., mobile menu toggles, confirmation modals).
*   **Day 13-14: Testing & Deployment**
    *   **Testing:** Run `pytest` for core logic (Auth and CRUD).
    *   **Deployment:** Configure `render.yaml` and deploy to Render.com.
    *   **Final QA:** Test on a mobile browser to ensure responsiveness.

---

## 5. Testing Strategy

| Test Type | Focus | Tool |
| :--- | :--- | :--- |
| **Unit Testing** | Logic for password hashing, task status toggling, and date validation. | `pytest` |
| **Integration Testing** | The flow from submitting a login form to reaching the dashboard. | `pytest` + `Flask-Testing` |
| **Manual UI Testing** | Testing the responsiveness of the task list on various screen widths. | Manual (Mobile/Desktop) |
| **Security Testing** | Verifying that users cannot access other users' tasks via URL manipulation. | Manual |

---

## 6. Risk Management & Alternatives

### 6.1 Risk Assessment
| Risk | Impact | Mitigation |
| :--- | :--- | :--- |
| **HTMX Learning Curve** | Low | The syntax is minimal HTML; use documentation and "HTML-over-the-wire" patterns. |
| **Database Connection** | Medium | Use SQLite for local development and PostgreSQL for production to ensure parity. |
| **Hosting Downtime** | Low | Use Render/Railway; if one goes down, the logic is easily portable to another provider. |

### 6.2 Alternatives Considered
*   **MERN Stack (React/Node):** Rejected. Too much "plumbing" (JSON APIs, State Management, Bundlers) for a simple CRUD app.
*   **Django:** Considered. While excellent, Flask was chosen to keep the codebase "light" and more intuitive for students learning the fundamentals of web requests.
*   **Next.js:** Considered. Great for scale, but introduces unnecessary complexity (Server vs. Client components) for this specific scope.

---

## 7. Final Recommendations
1.  **Keep it Lean:** Do not add "extra" features (like social login or AI summaries) during this 2-week sprint.
2.  **Standardize Styling:** Use Tailwind utility classes consistently to prevent the "CSS spaghetti" problem.
3.  **Automate Deployment:** Use GitHub Actions to automatically deploy to Render whenever the `main` branch is updated.
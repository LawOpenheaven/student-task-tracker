function register() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("message").innerText = data.message || data.error;
        })
        .catch(error => console.log(error));
}

function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                window.location.href = "dashboard.html";
            } else {
                document.getElementById("message").innerText = data.error;
            }

        })
        .catch(error => console.log(error));
}

function addTask() {

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const due_date = document.getElementById("due_date").value;
    const token = localStorage.getItem("token");

    fetch("http://127.0.0.1:5000/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                title: title,
                description: description,
                due_date: due_date
            })
        })
        .then(() => {
            document.getElementById("title").value = "";
            document.getElementById("description").value = "";
            document.getElementById("due_date").value = "";
            loadTasks();
        });
}

function loadTasks() {

    const token = localStorage.getItem("token");

    fetch("http://127.0.0.1:5000/tasks", {
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(response => response.json())
        .then(data => {

            // ✅ Safety check: backend might return error object
            if (!Array.isArray(data)) {
                console.log("Backend error:", data);
                return;
            }

            const tasks = data;

            const list = document.getElementById("taskList");
            list.innerHTML = "";

            tasks.forEach(task => {
                const li = document.createElement("li");
                li.innerHTML = `
                <strong>${task.title}</strong><br>
                ${task.description || ""}<br>
                <small>Due: ${task.due_date}</small>
            `;

                const btn = document.createElement("button");
                btn.innerText = "Delete";
                btn.onclick = () => deleteTask(task.id);

                li.appendChild(btn);
                list.appendChild(li);
            });

        })
        .catch(error => console.log(error));
}


function deleteTask(id) {

    const token = localStorage.getItem("token");

    fetch(`http://127.0.0.1:5000/tasks/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(() => loadTasks());
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

window.onload = function () {

    const token = localStorage.getItem("token");

    if (!token && document.getElementById("taskList")) {
        window.location.href = "login.html";
        return;
    }

    if (document.getElementById("taskList")) {
        loadTasks();
    }
};
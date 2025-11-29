const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

todoForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const task = todoInput.value.trim();
    if (task !== "") {
        addTodo(task);
        todoInput.value = "";
    }
});

function addTodo(task) {
    const li = document.createElement("li");
    li.textContent = task;
    li.addEventListener("click", function() {
        li.classList.toggle("completed");
    });
    const delBtn = document.createElement("button");
    delBtn.textContent = "✕";
    delBtn.className = "delete-btn";
    delBtn.addEventListener("click", function(e) {
        e.stopPropagation();
        li.remove();
    });
    li.appendChild(delBtn);
    todoList.appendChild(li);
}

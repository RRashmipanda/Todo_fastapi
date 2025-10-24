import { useEffect, useState } from "react";
import API from "./api";
import "./App.css";

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const res = await API.get("/todos");
      setTodos(res.data.map(t => ({ ...t, id: t._id })));
    } catch (err) {
      console.error("Fetch todos error:", err);
    }
  };

  const addTodo = async () => {
    if (!title.trim()) return;
    try {
      await API.post("/todos", { title });
      setTitle("");
      fetchTodos();
    } catch (err) {
      console.error("Add todo error:", err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await API.delete(`/todos/${id}`);
      fetchTodos();
    } catch (err) {
      console.error("Delete error:", err);
    }
  };

  const toggleCompleted = async (todo) => {
    try {
      await API.put(`/todos/${todo.id}`, {
        ...todo,
        completed: !todo.completed,
      });
      fetchTodos();
    } catch (err) {
      console.error("Update error:", err);
    }
  };

  return (
    <div className="container">
      <h2 className="title">My Tasks</h2>

      <div className="input-box">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Add a task"
        />
        <button className="add-btn" onClick={addTodo}>+</button>
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          <li className="todo-item" key={todo.id}>
            <label className="checkbox-container">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleCompleted(todo)}
              />
              <span className={todo.completed ? "completed" : ""}>
                {todo.title}
              </span>
            </label>
            <button className="delete-btn" onClick={() => deleteTodo(todo.id)}>
              🗑️
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

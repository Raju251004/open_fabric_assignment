import { useState } from "react";
import { addPermission } from "../api";

export default function AddPermissionForm() {
  const [form, setForm] = useState({
    user_id: "",
    action: "read",
    resource: "",
    effect: "allow",
  });

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await addPermission(form);
      alert("Permission added!");
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-4">
      <h2 className="text-lg font-semibold mb-2">4. Add Permission</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <input
          type="text"
          placeholder="User ID"
          value={form.user_id}
          onChange={(e) => setForm({ ...form, user_id: e.target.value })}
          className="border px-2 py-1 rounded-lg"
        />
        <select
          value={form.action}
          onChange={(e) => setForm({ ...form, action: e.target.value })}
          className="border px-2 py-1 rounded-lg"
        >
          <option>read</option>
          <option>write</option>
          <option>delete</option>
          <option>*</option>
        </select>
        <input
          type="text"
          placeholder="Resource (e.g., transactions)"
          value={form.resource}
          onChange={(e) => setForm({ ...form, resource: e.target.value })}
          className="border px-2 py-1 rounded-lg"
        />
        <select
          value={form.effect}
          onChange={(e) => setForm({ ...form, effect: e.target.value })}
          className="border px-2 py-1 rounded-lg"
        >
          <option>allow</option>
          <option>deny</option>
        </select>
        <button
          type="submit"
          className="bg-indigo-600 text-white px-3 py-1 rounded-lg hover:bg-indigo-700"
        >
          Add
        </button>
      </form>
    </div>
  );
}

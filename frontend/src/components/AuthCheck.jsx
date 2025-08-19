import { useState } from "react";
import { checkAuthorization } from "../api";

export default function AuthCheck({ token }) {
  const [method, setMethod] = useState("GET");
  const [path, setPath] = useState("/transactions");
  const [result, setResult] = useState(null);

  async function handleCheck() {
    try {
      const res = await checkAuthorization(token, method, path);
      setResult(res);
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-4 mb-4">
      <h2 className="text-lg font-semibold mb-2">2. Check Authorization</h2>
      <div className="flex gap-2 mb-2">
        <select
          value={method}
          onChange={(e) => setMethod(e.target.value)}
          className="border rounded-lg px-2 py-1"
        >
          <option>GET</option>
          <option>POST</option>
          <option>PUT</option>
          <option>PATCH</option>
          <option>DELETE</option>
        </select>
        <input
          type="text"
          placeholder="/path"
          value={path}
          onChange={(e) => setPath(e.target.value)}
          className="flex-1 border px-2 py-1 rounded-lg"
        />
        <button
          onClick={handleCheck}
          className="bg-green-600 text-white px-3 py-1 rounded-lg hover:bg-green-700"
        >
          Check
        </button>
      </div>

      {result && (
        <div
          className={`p-3 rounded-xl ${
            result.decision === "ALLOW" ? "bg-green-100" : "bg-red-100"
          }`}
        >
          <p>
            <strong>Decision:</strong> {result.decision}
          </p>
          <p>
            <strong>User:</strong> {result.user_id}
          </p>
          <p>
            <strong>Reason:</strong> {result.reason}
          </p>
        </div>
      )}
    </div>
  );
}

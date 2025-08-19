import { useState } from "react";
import { getToken } from "../api";

export default function TokenFetcher({ onToken }) {
  const [userId, setUserId] = useState("");

  async function handleFetch() {
    try {
      const data = await getToken(userId);
      onToken(data.token, data.user_id);
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-4 mb-4">
      <h2 className="text-lg font-semibold mb-2">1. Get Token</h2>
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Enter userId (e.g., user123)"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="flex-1 border px-2 py-1 rounded-lg"
        />
        <button
          onClick={handleFetch}
          className="bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700"
        >
          Get Token
        </button>
      </div>
    </div>
  );
}

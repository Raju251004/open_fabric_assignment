import { useState } from "react";
import { getUserPermissions } from "../api";

export default function PermissionsTable({ userId }) {
  const [perms, setPerms] = useState([]);

  async function fetchPerms() {
    try {
      const data = await getUserPermissions(userId);
      setPerms(data);
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-4 mb-4">
      <h2 className="text-lg font-semibold mb-2">3. User Permissions</h2>
      <button
        onClick={fetchPerms}
        className="bg-purple-600 text-white px-3 py-1 rounded-lg hover:bg-purple-700 mb-2"
      >
        Load Permissions
      </button>
      <table className="w-full border-collapse border text-sm">
        <thead>
          <tr className="bg-gray-200">
            <th className="border px-2 py-1">Action</th>
            <th className="border px-2 py-1">Resource</th>
            <th className="border px-2 py-1">Effect</th>
          </tr>
        </thead>
        <tbody>
          {perms.map((p) => (
            <tr key={p.id} className="odd:bg-gray-50">
              <td className="border px-2 py-1">{p.action}</td>
              <td className="border px-2 py-1">{p.resource}</td>
              <td className="border px-2 py-1">{p.effect}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

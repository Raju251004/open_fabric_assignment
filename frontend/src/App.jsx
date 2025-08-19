import { useState } from "react";
import TokenFetcher from "./components/TokenFetcher";
import AuthCheck from "./components/AuthCheck";
import PermissionsTable from "./components/PermissionsTable";
import AddPermissionForm from "./components/AddPermissionForm";

export default function App() {
  const [token, setToken] = useState(null);
  const [userId, setUserId] = useState(null);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold text-center mb-6">
        🔑 Auth & Permissions UI
      </h1>
      <TokenFetcher
        onToken={(t, u) => {
          setToken(t);
          setUserId(u);
        }}
      />

      {token && (
        <>
          <div className="bg-yellow-50 border border-yellow-200 p-3 rounded-xl text-sm">
            <strong>Token:</strong> <code className="break-all">{token}</code>
          </div>
          <AuthCheck token={token} />
          <PermissionsTable userId={userId} />
          <AddPermissionForm />
        </>
      )}
    </div>
  );
}

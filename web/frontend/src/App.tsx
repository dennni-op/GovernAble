// web/frontend/src/App.tsx

// We import tools from React, a library for building user interfaces.
import React, { useEffect, useState } from "react";
// This defines the shape of a single scan result that we expect from our API.
type ScanResult = { id: number; filename: string; scanned_at: string; findings: string };
function App() {
  // 'useState' is a React hook to store data that can change.
  // We'll store the list of scan results here.
  const [rows, setRows] = useState<ScanResult[]>([]);
  // 'useEffect' is a hook that runs code after the component loads.
  // This is the perfect place to fetch data from our API.
  useEffect(() => {
    // We call the '/api/v1/scan/results' endpoint we created earlier.
    fetch("http://localhost:8000/api/v1/scan/results")
      .then(r => r.json()) // Convert the response to JSON
      .then(setRows)      // Update our 'rows' state with the data
      .catch(console.error); // If there's an error, just log it.
  }, []); // The empty array [] means this runs only once.
  // This is the HTML structure of our page.
  return (
    <div>
      <h1>GovernAble — Recent scans</h1>
      <table>
        <thead><tr><th>ID</th><th>Filename</th><th>When</th><th>Findings</th></tr></thead>
        <tbody>
          {/* We loop through each result in our 'rows' state and create a table row for it. */}
          {rows.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.filename}</td>
              <td>{new Date(r.scanned_at).toLocaleString()}</td>
              {/* The findings are a JSON string, so we format them nicely. */}
              <td><pre>{JSON.stringify(JSON.parse(r.findings || "[]"), null, 2)}</pre></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default App;
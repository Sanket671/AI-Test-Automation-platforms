import { useState } from "react";

const API = "http://127.0.0.1:5002";

function App() {
  const [tests, setTests] = useState([]);
  const [report, setReport] = useState(null);
  const [mode, setMode] = useState("");
  const [loading, setLoading] = useState(false);

  const request = async (url) => {
    setLoading(true);

    try {
      const response = await fetch(url, {
        method: "POST"
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || "Request failed");
        return;
      }

      return data;
    } finally {
      setLoading(false);
    }
  };

  const generateTests = async () => {
    const data = await request(`${API}/api/generate`);

    if (data) {
      setMode("OpenAPI");
      setTests(data.tests);
      setReport(null);
    }
  };

  const generateAITests = async () => {
    const data = await request(`${API}/api/ai-generate`);

    if (data) {
      setMode("Gemini AI");
      setTests(data.tests);
      setReport(null);
    }
  };

  const runTests = async () => {
    const data = await request(
      mode === "Gemini AI"
        ? `${API}/api/ai-run`
        : `${API}/api/run`
    );

    if (data) {
      setReport(data);
    }
  };

  return (
    <div style={{
      maxWidth: "1100px",
      margin: "auto",
      padding: "40px",
      fontFamily: "Arial"
    }}>

      <h1>AI Test Automation Platform</h1>

      <p>
        OpenAPI → AI → Test Generation → Validation → Execution → Reporting
      </p>

      <button onClick={generateTests}>
        Generate OpenAPI Tests
      </button>

      <button
        onClick={generateAITests}
        style={{ marginLeft: "10px" }}
      >
        Generate AI Tests
      </button>

      <button
        onClick={runTests}
        style={{ marginLeft: "10px" }}
        disabled={tests.length === 0}
      >
        Run Tests
      </button>

      {loading && <p>Processing...</p>}

      {mode && (
        <h2>
          Mode: {mode}
        </h2>
      )}

      {tests.length > 0 && (
        <>
          <h2>Generated Tests ({tests.length})</h2>

          {tests.map((test, index) => (
            <div
              key={index}
              style={{
                border: "1px solid #ddd",
                padding: "15px",
                marginBottom: "10px",
                borderRadius: "8px"
              }}
            >
              <strong>
                {test.method} {test.url}
              </strong>

              <p>{test.name}</p>

              <p>{test.reason}</p>

              <b>
                Expected: {test.expected_status}
              </b>
            </div>
          ))}
        </>
      )}

      {report && (
        <>
          <h2>Execution Report</h2>

          <div style={{
            display: "flex",
            gap: "20px",
            marginBottom: "20px"
          }}>
            <div>
              <h3>Total</h3>
              <p>{report.total}</p>
            </div>

            <div>
              <h3>Passed</h3>
              <p>{report.passed}</p>
            </div>

            <div>
              <h3>Failed</h3>
              <p>{report.failed}</p>
            </div>
          </div>

          {report.results.map((result, index) => (
            <div
              key={index}
              style={{
                border: "1px solid #ddd",
                padding: "12px",
                marginBottom: "8px",
                borderRadius: "6px"
              }}
            >
              <strong>
                {result.status}
              </strong>

              {" — "}

              {result.method} {result.url}

              <br />

              Expected: {result.expected_status}
              {" | "}
              Actual: {result.actual_status}

              {result.error && (
                <p>
                  Error: {result.error}
                </p>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  );
}

export default App;
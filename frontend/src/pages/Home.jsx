import { useEffect, useState } from "react";
import { getHealth } from "../api/health";

export default function Home() {
  const [health, setHealth] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getHealth()
      .then((data) => {
        setHealth(data);
        setError(null);
      })
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h1>Frontend is running</h1>
      <p>
        Backend health:{" "}
        {error
          ? `Error: ${error}`
          : health
            ? JSON.stringify(health)
            : "Loading..."}
      </p>
    </div>
  );
}

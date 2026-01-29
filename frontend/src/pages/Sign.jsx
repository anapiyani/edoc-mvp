import { useParams } from "react-router-dom";

export default function Sign() {
  const { token } = useParams();

  return (
    <div>
      <h1>Sign page</h1>
      <p>Token: {token}</p>
      <button type="button">Download PDF</button>
      <button type="button">Accept</button>
      <button type="button">Reject</button>
    </div>
  );
}

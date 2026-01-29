import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Sign from "./pages/Sign";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/sign/:token" element={<Sign />} />
    </Routes>
  );
}

export default App;

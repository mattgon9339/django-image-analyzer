import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Cookies from "js-cookie";
import Home from "./components/home";
import Image from "./components/image";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const headers = {
    headers: {
      'content-type': 'multipart/form-data',
      'X-CSRFToken': Cookies.get('csrftoken')
    }
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home headers={headers} />} />
        <Route path="/image/:id" element={<Image headers={headers} />} />
      </Routes>
    </Router>
  );
}

export default App;

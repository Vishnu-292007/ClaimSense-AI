import { FaShieldAlt, FaUserCircle } from "react-icons/fa";

function Navbar() {
  return (
    <nav className="navbar">
      <div>
        <h1 className="logo">
          <FaShieldAlt />
          ClaimSense AI
        </h1>

        <p className="subtitle">AI Powered Insurance Claim Verification</p>
      </div>

      <div className="profile">
        <FaUserCircle size={38} />

        <div>
          <strong>Insurance Officer</strong>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

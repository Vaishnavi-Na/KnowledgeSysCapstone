import React from 'react';
import './navbarHome.css';

const NavbarHome: React.FC = () => {
  return (
    <nav className="navbarHome">
      {/* This div is our horizontal line, sitting behind everything */}
      <div className="nav-line"></div>
      
      {/* Left side links */}
      <div className="nav-left">
        <a href="#" className="nav-link">About</a>
        <a href="#" className="nav-link">Search</a>
      </div>

      {/* Center logo */}
      <div className="nav-center">
        <img src="/logo.png" alt="Logo" className="nav-logo" />
      </div>

      {/* Right side links */}
      <div className="nav-right">
        <a href="#" className="nav-link">Upload</a>
        <a href="#" className="nav-link">Build</a>
      </div>
    </nav>
  );
};

export default NavbarHome;

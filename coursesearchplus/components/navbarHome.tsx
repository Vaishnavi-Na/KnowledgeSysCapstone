import Link from 'next/link';
import Image from 'next/image';
import './navbarHome.css';

const NavbarHome: React.FC = () => {
  return (
    <nav className="navbarHome">
      {/* This div is our horizontal line, sitting behind everything */}
      <div className="nav-line"></div>
      
      {/* Left side links */}
      <div className="nav-left">
        <Link href="/about" className="nav-link">About</Link>
        <Link href="/search" className="nav-link">Search</Link>
      </div>

      {/* Center logo */}
      <div className="nav-center">
        <Link href="/">
          <img src="/logo.png" alt="Logo" className="nav-logo" />
        </Link>
      </div>

      {/* Right side links */}
      <div className="nav-right">
        <Link href="/upload" className="nav-link">Upload</Link>
        <Link href="/buildschedule" className="nav-link">Build</Link>
        <Link href="/tips" className="nav-link">Tips</Link>
      </div>
    </nav>
  );
};

export default NavbarHome;

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import './navbarElse.css';  // Changed from module import to direct import

export default function NavbarElse() {
  // get the current pathname (e.g. '/about', '/search', etc.)
  const pathname = usePathname();
  
  // A small helper that returns 'active-link' if the current route matches
  const isActive = (href: string) => {
    return pathname === href ? 'activeLink' : '';  // Removed styles.
  };

  return (
    <nav className="navbarElse">
      {/* Left: Logo linking back to home ("/") */}
      <div className="navLeft">
        <Link href="/" legacyBehavior> 
          <a>
            <img src="/logo2.png" alt="Logo" className="navLogo" />
          </a>
        </Link>
      </div>

      {/* Center: nav links */}
      <div className="navCenter">
        <Link href="/about" legacyBehavior>
          <a className={`navLink ${isActive('/about')}`}>
            About
          </a>
        </Link>
        
        <Link href="/search" legacyBehavior>
          <a className={`navLink ${isActive('/search')}`}>
            Search
          </a>
        </Link>

        <Link href="/upload" legacyBehavior>
          <a className={`navLink ${isActive('/upload')}`}>
            Upload
          </a>
        </Link>

        <Link href="/buildschedule" legacyBehavior>
          <a className={`navLink ${isActive('/buildschedule')}`}>
            Build
          </a>
        </Link>
      </div>

      {/* Right: Log in to account */}
      <div className="navRight">
        <Link href="/login" legacyBehavior> 
          <a className={`navLink ${isActive('/login')}`}>
            Login
          </a>
        </Link>
      </div>
      
    </nav>
  );
}

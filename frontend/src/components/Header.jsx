import React from 'react';
import { NavLink } from 'react-router-dom';

const Header = () => {
  return (
    <nav style={{ padding: '0 2rem' }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', height: '80px' }}>
        <div className="logo" style={{ fontSize: '1.8rem', letterSpacing: '0.1em' }}>
           <svg width="42" height="42" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ color: 'var(--accent-primary)', marginRight: '0.75rem' }}>
              <path d="M12 2L3 7V17L12 22L21 17V7L12 2Z" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 22V12M12 12L21 7M12 12L3 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M12 6.5C12 6.5 10 9 10 11.5C10 14 12 15.5 12 15.5C12 15.5 14 14 14 11.5C14 9 12 6.5 12 6.5Z" fill="currentColor" fillOpacity="0.3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
           </svg>
           TOXI<span>GUARD</span>
        </div>
        
        <div className="nav-links" style={{ gap: '3rem' }}>
          <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''} style={{ fontSize: '1rem', letterSpacing: '0.05em' }}>PREDICTOR</NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? 'active' : ''} style={{ fontSize: '1rem', letterSpacing: '0.05em' }}>ANALYTICS</NavLink>
        </div>
        
        <div style={{ display: 'flex', gap: '1.25rem', alignItems: 'center', background: 'rgba(34, 197, 94, 0.05)', padding: '0.5rem 1.25rem', borderRadius: '100px', border: '1px solid rgba(34, 197, 94, 0.1)' }}>
          <div style={{ width: '10px', height: '10px', background: '#22c55e', borderRadius: '50%', boxShadow: '0 0 12px #22c55e' }}></div>
          <span style={{ fontSize: '0.85rem', color: '#22c55e', fontWeight: '700' }}>Tox21 ENGINE ACTIVE</span>
        </div>
      </div>
    </nav>
  );
};

export default Header;

import React, { useState, useEffect } from 'react';
import { NAV_LINKS } from '../constants';
import { Scale } from 'lucide-react';

export const Header: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled 
          ? 'bg-navy-900/95 backdrop-blur-md py-4 shadow-lg border-b border-navy-700' 
          : 'bg-navy-900 py-6'
      }`}
    >
      <div className="container mx-auto px-6 flex justify-between items-center">
        <div className="flex items-center gap-2 group cursor-default">
          <Scale className="w-6 h-6 text-gold-500" />
          <span className="text-xl font-serif font-bold tracking-wide text-white">
            EquiLaw
          </span>
        </div>

        <nav className="hidden md:flex gap-8">
          {NAV_LINKS.map((link) => (
            <a 
              key={link.label}
              href={link.href}
              className="text-sm font-medium text-slate-300 hover:text-gold-400 transition-colors uppercase tracking-widest relative group"
            >
              {link.label}
              <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gold-500 transition-all duration-300 group-hover:w-full"></span>
            </a>
          ))}
        </nav>
      </div>
    </header>
  );
};
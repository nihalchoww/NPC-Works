import React from 'react';
import { TeamMember } from '../types';
import { Mail } from 'lucide-react';

interface TeamCardProps {
  member: TeamMember;
}

export const TeamCard: React.FC<TeamCardProps> = ({ member }) => {
  return (
    <div className="group relative bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 flex flex-col h-[450px]">
      
      {/* Image Container - Takes up top 65% */}
      <div className="relative h-[65%] overflow-hidden">
         {/* Overlay Gradient */}
         <div className="absolute inset-0 bg-navy-900/10 group-hover:bg-transparent transition-all duration-500 z-10 mix-blend-multiply" />
         
         {/* Image: Grayscale to Color on Hover */}
         <img 
            src={member.image} 
            alt={member.name} 
            className="w-full h-full object-cover grayscale group-hover:grayscale-0 transform group-hover:scale-110 transition-all duration-700 ease-out"
         />
         
         {/* Gold Border Bottom of Image */}
         <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-navy-900 via-gold-500 to-navy-900" />
      </div>

      {/* Content Container - Bottom 35% */}
      <div className="relative h-[35%] bg-white p-6 flex flex-col items-center justify-center text-center z-20">
        
        {/* Floating Tag */}
        <div className="absolute -top-4 bg-navy-900 text-gold-500 text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-widest shadow-md">
            {member.role || "Co-Creator"}
        </div>

        <h3 className="text-xl font-serif font-bold text-navy-900 mb-1 leading-tight">{member.name}</h3>
        
        {/* ID Display */}
        <p className="font-mono text-xs text-slate-400 mb-4 tracking-wider">ID: {member.id}</p>
        
        {/* Email Link */}
        <a 
          href={`mailto:${member.email}`}
          className="group/link flex items-center gap-2 text-sm text-slate-500 hover:text-gold-600 transition-colors duration-300 border border-slate-200 px-4 py-2 rounded-lg hover:border-gold-500/50 hover:bg-gold-50"
        >
          <Mail className="w-4 h-4" />
          <span className="font-medium">Contact</span>
        </a>
      </div>
    </div>
  );
};
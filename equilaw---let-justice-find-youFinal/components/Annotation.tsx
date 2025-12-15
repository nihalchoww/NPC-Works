import React from 'react';

interface AnnotationProps {
  device: string;
  className?: string;
}

export const Annotation: React.FC<AnnotationProps> = ({ device, className = "text-gold-500" }) => {
  return (
    <span className={`inline-block ml-2 text-sm font-mono tracking-wider opacity-90 ${className}`}>
      [{device}]
    </span>
  );
};
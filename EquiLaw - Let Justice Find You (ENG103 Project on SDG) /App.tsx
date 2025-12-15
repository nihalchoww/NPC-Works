import React from 'react';
import { CONTENT, TEAM_MEMBERS, IMAGES, DEEP_DIVE_CONTENT } from './constants';
import { Header } from './components/Header';
import { Annotation } from './components/Annotation';
import { TeamCard } from './components/TeamCard';
import { Reveal } from './components/Reveal';
import { Scale, Brain, Users, Scale as ScaleIcon, BookOpen, HeartHandshake, ShieldCheck, Gavel, Landmark, ScrollText, ChevronDown, FileWarning, Shield } from 'lucide-react';

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col font-sans text-slate-600">
      <Header />

      {/* 1. Hero Section */}
      <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden text-center">
        {/* Background Image with Parallax-like fixity */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat fixed"
          style={{ backgroundImage: `url(${IMAGES.hero})` }}
        />
        <div className="absolute inset-0 bg-navy-900/85" /> 
        
        <div className="container mx-auto px-6 relative z-10 max-w-5xl py-20">
          <div className="mb-12 inline-flex items-center justify-center w-20 h-20 rounded-full bg-gold-500/10 border border-gold-500/30 text-gold-500 animate-fade-in-up backdrop-blur-sm shadow-[0_0_15px_rgba(245,158,11,0.3)]">
             <Scale className="w-10 h-10" />
          </div>
          
          <h1 className="text-4xl md:text-5xl lg:text-7xl font-serif font-bold text-white mb-10 leading-tight drop-shadow-lg">
            For too long, the legal system has been a labyrinth without a map.
            <Annotation device={CONTENT.hero.title.device} />
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-200 font-light max-w-3xl mx-auto leading-relaxed drop-shadow-md pb-8">
            Our AI agent makes understanding your rights as clear as crystal.
            <Annotation device={CONTENT.hero.subtext.device} />
          </p>

          {/* Animated Scroll Indicator - Moved down to prevent overlap */}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-white/50 animate-bounce">
            <div className="flex flex-col items-center gap-2">
                <span className="text-xs uppercase tracking-widest text-gold-500">Scroll</span>
                <ChevronDown className="w-6 h-6" />
            </div>
          </div>
        </div>
      </section>

      {/* 2. The Problem Deep Dive - ENHANCED: Layered Imagery & Icons */}
      <section id="problem" className="py-24 bg-slate-50 relative overflow-hidden">
         {/* Decorative Floating Icons for Problem Section */}
         <div className="absolute top-10 -left-10 opacity-[0.03] animate-float pointer-events-none hidden lg:block">
            <Scale className="w-96 h-96 text-navy-900" />
         </div>
         <div className="absolute bottom-10 -right-10 opacity-[0.03] animate-float-delayed pointer-events-none hidden lg:block">
            <FileWarning className="w-80 h-80 text-navy-900 rotate-12" />
         </div>

         <div className="container mx-auto px-6 max-w-6xl relative z-10">
            {/* Header Area */}
            <Reveal>
              <div className="mb-16 md:mb-24">
                 <h2 className="text-sm font-bold tracking-widest text-gold-600 uppercase mb-4">The Challenge</h2>
                 <h3 className="text-3xl md:text-5xl font-serif font-bold text-navy-900 leading-tight max-w-4xl">
                    Justice has been sleeping, but it is time to wake her up.
                    <Annotation device={CONTENT.literary.header1.device} className="text-gold-600/80 block mt-2 text-xl" />
                 </h3>
              </div>
            </Reveal>

            {/* Deep Dive Content Grid */}
            <div className="grid lg:grid-cols-2 gap-16 items-center mb-24">
               {/* Left: Enhanced Layered Images */}
               <Reveal>
                 <div className="relative h-[550px] w-full hidden md:block">
                    {/* Back Image: The Chaos/Paperwork */}
                    <div className="absolute top-0 right-10 w-3/4 h-3/4 rounded-2xl overflow-hidden shadow-xl opacity-60">
                         <img 
                          src={IMAGES.problem_chaos} 
                          alt="Chaotic legal paperwork" 
                          className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
                        />
                         <div className="absolute inset-0 bg-navy-900/30"></div>
                    </div>
                    {/* Front Image: The System/Gavel */}
                    <div className="absolute bottom-0 left-5 w-3/4 h-3/4 rounded-2xl overflow-hidden shadow-2xl border-4 border-white">
                        <img 
                          src={IMAGES.problem} 
                          alt="Gavel and books" 
                          className="w-full h-full object-cover transform hover:scale-105 transition-transform duration-700"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-navy-900/60 to-transparent"></div>
                    </div>
                    {/* Decorative Element */}
                    <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-gold-500/10 rounded-full blur-3xl"></div>
                 </div>
                 {/* Mobile only single image fallback */}
                 <div className="relative rounded-2xl overflow-hidden shadow-xl h-[400px] md:hidden">
                    <img src={IMAGES.problem} alt="Legal problem" className="w-full h-full object-cover" />
                 </div>
               </Reveal>

               {/* Right: Text Content */}
               <Reveal delay={200}>
                 <div className="space-y-6 relative">
                    {/* Decorative Scroll Icon Floating */}
                    <div className="absolute -top-12 -right-6 text-gold-500/10 animate-pulse-slow hidden md:block pointer-events-none">
                        <ScrollText className="w-24 h-24 -rotate-12" />
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-sm border-l-4 border-gold-500 mb-8 transform hover:-translate-y-1 transition-transform duration-300 relative z-10">
                       <p className="text-xl text-navy-800 font-medium leading-relaxed italic">
                         You are drowning in a million pages of confusing legal paperwork.
                         <Annotation device={CONTENT.literary.text1.device} className="text-slate-400 block mt-2 text-base not-italic" />
                       </p>
                    </div>
                    {DEEP_DIVE_CONTENT.problem.map((paragraph, idx) => (
                      <p key={idx} className="text-lg text-slate-700 leading-relaxed font-light">
                        {paragraph}
                      </p>
                    ))}
                 </div>
               </Reveal>
            </div>
            
            <div className="w-full h-px bg-slate-200 my-16" />

             {/* Importance */}
             <Reveal>
                <div className="max-w-4xl mx-auto text-center relative">
                    <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-20 h-20 bg-gold-500/10 rounded-full blur-2xl"></div>
                    <h4 className="text-2xl font-serif font-bold text-navy-800 mb-6 relative z-10">Why This Matters</h4>
                    <p className="text-xl text-slate-600 leading-relaxed relative z-10">
                       {DEEP_DIVE_CONTENT.importance}
                    </p>
                </div>
             </Reveal>
         </div>
      </section>


      {/* 3. The Solution / Product - ENHANCED: Moving Blobs & Icons */}
      <section id="product" className="py-24 bg-white relative overflow-hidden">
        {/* Subtle Legal Background with Icons */}
        <div className="absolute inset-0 opacity-5 pointer-events-none" style={{ backgroundImage: `url(${IMAGES.library})`, backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
        
        {/* Animated Background Blobs for "Tech" feel */}
        <div className="absolute top-0 -left-4 w-72 h-72 bg-gold-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-navy-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000"></div>

        {/* Floating Animated Icons - ENHANCED */}
        <div className="absolute top-20 left-10 text-navy-200 animate-float opacity-30 hidden lg:block z-0">
           <Gavel className="w-32 h-32" />
        </div>
        <div className="absolute bottom-20 right-10 text-gold-200 animate-float-delayed opacity-30 hidden lg:block z-0">
           <Landmark className="w-40 h-40" />
        </div>
        <div className="absolute top-1/2 left-20 text-navy-200 animate-float opacity-20 hidden lg:block z-0">
           <ScrollText className="w-20 h-20" />
        </div>
        <div className="absolute top-40 right-20 text-navy-300 animate-pulse-slow opacity-20 hidden lg:block z-0">
           <Scale className="w-28 h-28 rotate-6" />
        </div>

        <div className="container mx-auto px-6 max-w-6xl relative z-10">
          <Reveal>
            <div className="text-center mb-16 max-w-3xl mx-auto">
              <h2 className="text-sm font-bold tracking-widest text-gold-600 uppercase mb-4">The Innovation</h2>
              <h3 className="text-3xl md:text-5xl font-serif font-bold text-navy-900 mb-6">
                 Laws should be logical, luminous, and life-changing.
                 <Annotation device={CONTENT.literary.header2.device} className="text-gold-600/80 block mt-2 text-xl" />
              </h3>
              <p className="text-lg text-slate-700 leading-relaxed">
                {CONTENT.product.intro}
              </p>
            </div>
          </Reveal>

          {/* AI Visual */}
          <Reveal>
             <div className="w-full h-80 md:h-96 rounded-2xl overflow-hidden shadow-2xl mb-16 relative group border border-slate-100">
                <div className="absolute inset-0 bg-navy-900/30 group-hover:bg-navy-900/10 transition-colors duration-500 z-10" />
                <img 
                   src={IMAGES.solution} 
                   alt="AI Technology Abstract" 
                   className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
                />
                <div className="absolute bottom-8 left-8 z-20 bg-white/90 backdrop-blur-md px-6 py-3 rounded-lg shadow-lg border border-white/50">
                   <div className="flex items-center gap-2 text-navy-900 font-bold">
                      <Brain className="w-5 h-5 text-gold-500" />
                      AI-Powered Legal Clarity
                   </div>
                </div>
             </div>
          </Reveal>

          {/* Literary Device Cards (Solution Philosophy) */}
          <div className="grid md:grid-cols-2 gap-8 mb-20">
             <Reveal delay={200}>
                <div className="bg-slate-50/80 backdrop-blur-sm p-10 rounded-xl shadow-lg border-t-4 border-navy-900 h-full flex flex-col justify-center hover:bg-white transition-colors duration-300">
                    <p className="text-2xl text-navy-900 font-serif font-bold italic mb-4">
                      "{CONTENT.literary.card1.text}"
                    </p>
                    <div className="text-right">
                      <Annotation device={CONTENT.literary.card1.device} />
                    </div>
                </div>
             </Reveal>
             
             <Reveal delay={400}>
                <div className="bg-navy-900 p-10 rounded-xl shadow-lg border-t-4 border-gold-500 text-white h-full flex flex-col justify-center relative overflow-hidden">
                    {/* Texture overlay */}
                    <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>
                    <p className="text-2xl text-slate-100 font-serif font-bold italic mb-4 relative z-10">
                      "{CONTENT.literary.card2.text}"
                    </p>
                    <div className="text-right relative z-10">
                      <Annotation device={CONTENT.literary.card2.device} />
                    </div>
                </div>
             </Reveal>
          </div>

          {/* Product Tiers */}
          <div className="grid md:grid-cols-2 gap-12">
            <Reveal delay={200}>
              <div className="bg-white p-8 rounded-xl border border-slate-100 hover:border-gold-500/30 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 shadow-md h-full flex flex-col group relative overflow-hidden">
                {/* Subtle Tier Icon Background */}
                <div className="absolute -bottom-10 -right-10 text-slate-100 group-hover:text-gold-500/10 transition-colors duration-500">
                    <ScrollText className="w-48 h-48" />
                </div>

                <div className="flex items-center gap-4 mb-6 relative z-10">
                  <div className="bg-navy-50 p-4 rounded-full text-navy-900 group-hover:scale-110 group-hover:bg-gold-500 group-hover:text-white transition-all duration-300">
                    <Brain className="w-8 h-8" />
                  </div>
                  <h3 className="text-2xl font-bold text-navy-900">{CONTENT.product.tier1.title}</h3>
                </div>
                <p className="text-slate-600 leading-relaxed text-lg mb-4 flex-grow relative z-10">
                  {CONTENT.product.tier1.description}
                </p>
                <div className="text-gold-600 font-semibold text-sm tracking-wide uppercase mt-4 relative z-10">
                    Features: 24/7 Availability • Multi-Language Support
                </div>
              </div>
            </Reveal>

            <Reveal delay={400}>
              <div className="bg-gradient-to-br from-navy-900 to-navy-800 p-8 rounded-xl border border-navy-700 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 text-white relative overflow-hidden group h-full flex flex-col">
                <div className="absolute top-0 right-0 w-40 h-40 bg-gold-500/10 rounded-bl-full transition-all duration-500 group-hover:bg-gold-500/20 group-hover:scale-110" />
                
                {/* Decorative Shield Icon for Security/Defense */}
                <div className="absolute -bottom-5 -left-5 text-white/5 group-hover:text-gold-500/10 transition-colors duration-500 rotate-12">
                    <Shield className="w-48 h-48" />
                </div>

                <div className="flex items-center gap-4 mb-6 relative z-10">
                  <div className="bg-white/10 p-4 rounded-full text-gold-500 backdrop-blur-sm group-hover:scale-110 group-hover:bg-white group-hover:text-navy-900 transition-all duration-300">
                    <Gavel className="w-8 h-8" />
                  </div>
                  <h3 className="text-2xl font-bold text-white">{CONTENT.product.tier2.title}</h3>
                </div>
                <p className="text-slate-300 leading-relaxed relative z-10 text-lg mb-4 flex-grow">
                  {CONTENT.product.tier2.description}
                </p>
                <div className="text-gold-400 font-semibold text-sm tracking-wide uppercase mt-4 relative z-10">
                    Features: NGO Partnerships • Pro-Bono Matching
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>


      {/* 4. Our Vision - FIXED: Darker Background & High Contrast with Parallax Image */}
      <section id="vision" className="py-32 bg-navy-950 text-white relative overflow-hidden">
        {/* Background Image Parallax */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20 mix-blend-overlay fixed"
          style={{ backgroundImage: `url(${IMAGES.vision_bg})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-navy-950 via-navy-900/95 to-navy-950"></div>
        
        <div className="container mx-auto px-6 text-center max-w-4xl relative z-10">
          <Reveal>
            <div className="inline-block p-4 rounded-full border-2 border-gold-500/30 mb-10 animate-pulse-slow">
               <HeartHandshake className="w-12 h-12 text-gold-500" />
            </div>
            
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-serif mb-16 leading-tight drop-shadow-lg">
              We need more hands on deck to build a fairer society.
              <Annotation device={CONTENT.vision.text1.device} className="text-gold-500 font-bold ml-4" />
            </h2>
          </Reveal>

          <Reveal delay={200}>
            {/* Increased opacity of background for better legibility against any potential bleed */}
            <div className="bg-navy-800/80 p-12 rounded-3xl backdrop-blur-md border border-navy-700/50 inline-block shadow-2xl hover:bg-navy-800 transition-colors duration-500 group hover:-translate-y-1 transform">
              <p className="text-2xl md:text-3xl text-white font-light leading-relaxed drop-shadow-md">
                We are here for the poor. We are here for the lost. We are here for you.
                <Annotation device={CONTENT.vision.text2.device} className="block mt-6 text-gold-500 font-bold text-xl group-hover:text-gold-400 transition-colors" />
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      {/* 5. Team Section */}
      <section id="team" className="py-24 bg-slate-50 relative">
        {/* Abstract pattern background */}
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage: 'radial-gradient(#1e293b 1px, transparent 1px)', backgroundSize: '24px 24px'}}></div>
        
        <div className="container mx-auto px-6 relative z-10">
          <Reveal>
            <div className="text-center mb-16">
              <h2 className="text-3xl font-serif font-bold text-navy-900 mb-2">The Creators</h2>
              <div className="w-20 h-1 bg-gold-500 mx-auto" />
            </div>
          </Reveal>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {TEAM_MEMBERS.map((member, index) => (
              <Reveal key={member.id} delay={index * 150}>
                <TeamCard member={member} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* 6. Footer */}
      <footer className="bg-navy-900 text-slate-400 py-20 border-t border-navy-800 relative overflow-hidden">
        {/* Decorative footer glow */}
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px] bg-gold-500/5 rounded-full blur-[100px] pointer-events-none"></div>

        <div className="container mx-auto px-6 text-center relative z-10">
          <Reveal>
            <div className="mb-10">
                <div className="inline-block p-3 rounded-full bg-navy-800 border border-navy-700 mb-6 shadow-lg">
                  <ScaleIcon className="w-8 h-8 text-gold-600" />
                </div>
                <h3 className="text-2xl font-serif text-white mb-2 tracking-wide">EquiLaw</h3>
                <p className="text-sm opacity-60">Let Justice Find You</p>
            </div>
            
            <div className="w-full h-px bg-gradient-to-r from-transparent via-navy-700 to-transparent max-w-xs mx-auto mb-10" />

            <blockquote className="text-xl md:text-2xl font-serif italic text-slate-300 max-w-3xl mx-auto mb-10">
              "{CONTENT.footer.quote.text}"
              <Annotation device={CONTENT.footer.quote.device} />
            </blockquote>

            <div className="mb-12 inline-flex items-center gap-3 px-6 py-3 rounded-full bg-navy-950/50 border border-navy-700 hover:bg-navy-950 transition-all duration-300 group cursor-default shadow-lg hover:shadow-gold-500/10 hover:border-gold-500/30">
              <div className="w-2 h-2 rounded-full bg-gold-500 animate-pulse" />
              <p className="text-sm font-medium text-slate-300 tracking-wide uppercase group-hover:text-white transition-colors">
                {CONTENT.footer.sdg}
              </p>
            </div>

          </Reveal>
          
          <div className="text-xs tracking-widest uppercase opacity-40 hover:opacity-100 transition-opacity">
            &copy; {new Date().getFullYear()} EquiLaw. All Rights Reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
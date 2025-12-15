import { ContentSection, TeamMember } from './types';

export const IMAGES = {
  hero: "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=2940", // Cinematic Courtroom/Scales
  problem: "https://images.unsplash.com/photo-1589994965851-a8f479c573a9?auto=format&fit=crop&q=80&w=1974", // Gavel and Books
  problem_chaos: "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&q=80&w=2070", // Chaotic Paperwork/Mess
  solution: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80&w=1965", // AI/Network Abstract
  library: "https://images.unsplash.com/photo-1453928582365-b6ad33cbcf64?auto=format&fit=crop&q=80&w=2073", // Old Law Library Background
  vision_bg: "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?auto=format&fit=crop&q=80&w=2070", // Helping Hands/Humanity
  texture: "https://www.transparenttextures.com/patterns/cubes.png" // Optional texture if needed
};

export const DEEP_DIVE_CONTENT = {
  problem: [
    "In Bangladesh, the legal system is buckling under the weight of a staggering crisis. With over 3.8 million pending cases clogging the courts, justice is often delayed for decades, effectively denying it to those who need it most. For the average citizen, a plea for help becomes a generational waiting game.",
    "The disconnect between the rural majority and the centralized legal infrastructure in cities like Dhaka is profound. Villagers are forced to navigate a labyrinthine system that operates in a language they do not speak and follows procedures they cannot comprehend, leaving them vulnerable and unheard.",
    "Cost remains the ultimate barrier. For the millions of working-class people—from rickshaw pullers to garment workers—hiring a competent lawyer in the capital is a financial impossibility. EquiLaw exists to dismantle these barriers, ensuring that justice is not a luxury for the wealthy, but a right for all."
  ],
  importance: "In a country where the legal gap widens every day, EquiLaw is a necessary lifeline. By democratizing legal knowledge and providing free access to rights information, we empower the people of Bangladesh to stand tall against injustice, embodying the spirit of SDG 16: promoting just, peaceful, and inclusive societies."
};

export const CONTENT = {
  hero: {
    title: { text: "For too long, the legal system has been a labyrinth without a map.", device: "Metaphor" },
    subtext: { text: "Our AI agent makes understanding your rights as clear as crystal.", device: "Simile" },
  },
  product: {
    title: "How EquiLaw Works: Bridging the Gap",
    intro: "The crisis of 'Access to Justice' leaves millions vulnerable simply because they cannot afford counsel. EquiLaw acts as a digital bridge, transforming the impenetrable wall of legal statute into a welcoming open door.",
    tier1: {
      title: "Tier 1: Instant AI Legal Scholar",
      description: "Our AI-integrated web agent is not just a chatbot; it is a legal scholar in your pocket. Available 24/7, it instantly translates complex Bengali and English penal codes into simple, actionable advice. Whether it is a land dispute in a rural village or a labor rights violation in the city, the AI demystifies the law, providing clarity without cost."
    },
    tier2: {
      title: "Tier 2: Pro-Bono Representation",
      description: "Technology has limits; justice does not. For critical cases requiring actual courtroom presence, our system identifies merit and automatically connects users with our network of partner NGOs and pro-bono lawyers. We facilitate the transition from digital advice to physical defense, ensuring that no legitimate grievance goes unheard due to poverty."
    }
  },
  literary: {
    header1: { text: "Justice has been sleeping, but it is time to wake her up.", device: "Personification" },
    text1: { text: "You are drowning in a million pages of confusing legal paperwork.", device: "Hyperbole" },
    header2: { text: "Laws should be logical, luminous, and life-changing.", device: "Alliteration" },
    card1: { text: "We provide a voice for the voiceless and strength for the weak.", device: "Antithesis" },
    card2: { text: "We do not just serve the law; the law serves us.", device: "Chiasmus" },
  },
  vision: {
    text1: { text: "We need more hands on deck to build a fairer society.", device: "Synecdoche" },
    text2: { text: "We are here for the poor. We are here for the lost. We are here for you.", device: "Anaphora" },
  },
  footer: {
    quote: { text: "It is a strange paradox that the most powerful laws are often the most fragile.", device: "Paradox" },
    sdg: "SDG 16 Goal Followed - Promote just, peaceful and inclusive societies."
  }
};

import ahanafImg from './ahanaf.jpg';
import saminImg from './samin.jpg';
import dewanImg from './dewan.jpg';

export const TEAM_MEMBERS: TeamMember[] = [
  {
    name: "Ahanaf Chowdhury Nihal",
    id: "24241052",
    role: "Co-Creator",
    email: "ahanaf.chowdhury.nihal@g.bracu.ac.bd",
    // 2. USE THE IMPORTED VARIABLE (No Quotes!)
    image: ahanafImg 
  },
  {
    name: "Samin Tanzim Rahman",
    id: "24305019",
    role: "Co-Creator",
    email: "samin.tanzim.rahman@g.bracu.ac.bd",
    image: saminImg
  },
  {
    name: "Dewan Barnil Alif Dimitre",
    id: "24305040",
    role: "Co-Creator",
    email: "dewan.barnil.alif.dimitre@g.bracu.ac.bd",
    image: dewanImg
  }
];

export const NAV_LINKS = [
  { label: "Home", href: "#home" },
  { label: "The Problem", href: "#problem" },
  { label: "The Solution", href: "#product" },
  { label: "Vision", href: "#vision" },
  { label: "Team", href: "#team" },
];

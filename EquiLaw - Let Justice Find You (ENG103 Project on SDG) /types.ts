export interface TeamMember {
  name: string;
  id: string;
  role?: string;
  email: string;
  image: string;
}

export interface NavLink {
  label: string;
  href: string;
}

export interface ContentSection {
  text: string;
  device: string;
}
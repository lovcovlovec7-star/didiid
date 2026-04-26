import {
  Clapperboard,
  Package,
  Sparkles,
  Image as ImageIcon,
  Store,
  WandSparkles
} from 'lucide-react';

// Replace contact links here.
export const CONTACTS = {
  telegram: 'https://t.me/yourusername',
  email: 'mailto:yourmail@example.com'
};

// Replace media file names and text for portfolio items here.
export const works = [
  {
    title: 'Furniture Brand Video',
    category: 'AI Video',
    description: 'Vertical ad concept for premium furniture storytelling and launches.',
    tags: ['AI commercial', '9:16 video'],
    type: 'video',
    src: '/assets/work-1.mp4'
  },
  {
    title: 'Product Poster Campaign',
    category: 'Posters',
    description: 'Bold campaign frames with cinematic light for product highlights.',
    tags: ['Product visual', 'Poster'],
    type: 'image',
    src: '/assets/work-2.jpg'
  },
  {
    title: 'AI Character Drama',
    category: 'Social Media',
    description: 'Fast-cut emotional story crafted for retention on short-form feeds.',
    tags: ['TikTok', 'Reels content'],
    type: 'video',
    src: '/assets/work-3.mp4'
  },
  {
    title: 'Marketplace Product Card',
    category: 'Product',
    description: 'Clean conversion-first product card design for marketplaces.',
    tags: ['E-commerce design', 'Card visual'],
    type: 'image',
    src: '/assets/work-4.jpg'
  },
  {
    title: 'Luxury Product Shot',
    category: 'Product',
    description: 'Premium key visual with controlled reflections and sharp composition.',
    tags: ['Advertising image', 'Studio feel'],
    type: 'image',
    src: '/assets/work-5.jpg'
  },
  {
    title: 'Brand Intro Video',
    category: 'AI Video',
    description: 'Hero motion opener built for websites, campaigns and launches.',
    tags: ['Motion', 'Website hero'],
    type: 'video',
    src: '/assets/work-6.mp4'
  }
];

export const filters = ['All', 'AI Video', 'Product', 'Posters', 'Social Media'];

export const services = [
  {
    icon: Clapperboard,
    title: 'AI Video Ads',
    description: 'Ad-ready short videos with premium pacing, hooks and narrative clarity.',
    outcomes: ['Ready for TikTok / Reels / Shorts', 'Vertical 9:16 and square formats', 'Premium visual style']
  },
  {
    icon: Package,
    title: 'Product Visuals',
    description: 'High-end product imagery for launches, websites and campaigns.',
    outcomes: ['Clean composition', 'Brand-consistent look', 'Conversion-focused frames']
  },
  {
    icon: Sparkles,
    title: 'Social Media Creatives',
    description: 'Scroll-stopping creative sets tailored to platform behavior.',
    outcomes: ['Hook-first opening frames', 'Fast adaptation cycles', 'Template-friendly packs']
  },
  {
    icon: ImageIcon,
    title: 'Posters & Key Visuals',
    description: 'Campaign-level posters with cinematic tone and strong hierarchy.',
    outcomes: ['Hero poster styles', 'Series-ready visual language', 'Print and digital options']
  },
  {
    icon: Store,
    title: 'Marketplace Cards',
    description: 'Clear, compelling cards designed for better click-through and trust.',
    outcomes: ['Platform-compliant ratios', 'Structured product messaging', 'Premium catalog consistency']
  },
  {
    icon: WandSparkles,
    title: 'Photo Restoration / Enhancement',
    description: 'Upscale, repair and improve source materials for polished delivery.',
    outcomes: ['Sharper details', 'Color and contrast refinement', 'Ready for ad usage']
  }
];

export const processSteps = [
  {
    title: 'Brief',
    description: 'You send references, product info, goals and style preferences.'
  },
  {
    title: 'Concept',
    description: 'I create a visual direction, scenes, prompts and structure.'
  },
  {
    title: 'Production',
    description: 'AI images, videos, edits and design are generated and refined.'
  },
  {
    title: 'Delivery',
    description: 'You receive ready-to-use content for ads, website or social media.'
  }
];

export const stats = [
  { value: '50+', label: 'visuals created' },
  { value: '10+', label: 'content formats' },
  { value: '9:16 / 1:1 / 16:9', label: 'supported ratios' },
  { value: 'Ads / social / website', label: 'content targets' }
];

export const testimonials = [
  'The visuals looked much more expensive than we expected.',
  'Fast, creative and very clear communication.',
  'The final video was perfect for social media.'
];

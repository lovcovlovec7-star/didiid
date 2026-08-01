'use client';

import { useState } from 'react';

export default function MediaBlock({ src, type, fallbackTitle, className = '' }) {
  const [failed, setFailed] = useState(false);

  return (
    <div className={`relative h-full w-full overflow-hidden ${className}`}>
      {!failed && type === 'video' ? (
        <video
          autoPlay
          muted
          loop
          playsInline
          preload="metadata"
          className="h-full w-full object-cover transition duration-700 group-hover:scale-105"
          onError={() => setFailed(true)}
        >
          <source src={src} />
        </video>
      ) : null}

      {!failed && type === 'image' ? (
        <img
          src={src}
          alt={fallbackTitle}
          loading="lazy"
          className="h-full w-full object-cover transition duration-700 group-hover:scale-105"
          onError={() => setFailed(true)}
        />
      ) : null}

      {failed ? (
        <div className="flex h-full min-h-56 w-full items-center justify-center bg-gradient-to-br from-panel via-[#14182a] to-[#090b12] p-6 text-center">
          <div>
            <p className="mb-2 text-sm uppercase tracking-[0.3em] text-cyan/70">Preview</p>
            <p className="text-lg font-medium text-white/90">{fallbackTitle}</p>
          </div>
        </div>
      ) : null}

      <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-black/20" />
    </div>
  );
}

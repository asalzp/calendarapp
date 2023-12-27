// ParticleComponent.js
import React, { useEffect } from 'react';
import Particles from 'particles.js';
import './ParticleComponent.css'; // Import the CSS file

const ParticleComponent = () => {
  useEffect(() => {
    // Initialize particles.js
    Particles.init({
      selector: '.particles',
      color: '#ffffff',
      connectParticles: true,
      responsive: [
        {
          breakpoint: 800,
          options: {
            color: '#00ff00',
            maxParticles: 80,
            connectParticles: false,
          },
        },
      ],
    });
  }, []);

  return <div className="particles" />;
};

export default ParticleComponent;

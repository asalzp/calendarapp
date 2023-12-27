// WelcomePage.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function WelcomePage() {
  const [authUrl, setAuthUrl] = useState('');
  const navigate = useNavigate();

  const handleIntegrationClick = async () => {
    try {
      const response = await axios.post('http://localhost:8000/get-credentials/');
      setAuthUrl(response.data.auth_url);

      // Redirect to the main page after successful integration
      navigate('/main');
    } catch (error) {
      console.error('Error initiating Google Calendar integration:', error);
    }
  };

  return (
    <div>
      <div className="header">
        <h1>Welcome to Automated Calendar Invite!</h1>
      </div>
      <p>Click below to get started.</p>
      <div className="button-div">
        <button class="btn btn-primary button-api" onClick={handleIntegrationClick}>Integrate API</button>
      </div>
    </div>
  );
}

export default WelcomePage;

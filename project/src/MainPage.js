// MainPage.js
import React from 'react';
import axios from 'axios';
import './MainApp.css';

class MainPage extends React.Component {
  state = {
    userInput: '',
    errorMessage: '', // Added state for error message
    loading: false, // Added state for loading spinner
    resultData: null, // Added state for result data
  };

  handleInputChange = (event) => {
    // Clear the error message and result data when the user starts typing
    this.setState({ userInput: event.target.value, errorMessage: '', resultData: null });
  }

  postData = async () => {
    try {
      if (!this.state.userInput.trim()) {
        // If the message is empty or only contains whitespace
        this.setState({ errorMessage: 'Please enter a message.' });
        return; // Don't proceed with API call
      }

      // Set loading state to true to show the spinner
      this.setState({ loading: true });

      const userInput = encodeURIComponent(this.state.userInput);
      const res = await axios.post(`http://localhost:8000/create-event/${userInput}/`, {
        userInput: this.state.userInput,
      });
      
      console.log(res);

      // Set loading state to false to hide the spinner
      this.setState({
        userInput: '',
        errorMessage: '', // Clear error message on successful submission
        loading: false,
        resultData: res.data, // Save result data
      });
    } catch (error) {
      console.error('Error posting data:', error);

      // Set loading state to false and show an error message
      this.setState({ loading: false, errorMessage: 'Error processing request.' });
    }
  }

  render() {
    return (
      <div>
        <div className="header">
          <h1>Calendar Event Automation</h1>
        </div>
        <p>Enter your message here to automatically create a Google Calendar meeting invite.</p>
        <div className="input input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text" id="inputGroup-sizing-default">Message</span>
          </div>
          <input
            value={this.state.userInput}
            onChange={this.handleInputChange}
            type="text"
            className="form-control"
            aria-label="Default"
            aria-describedby="inputGroup-sizing-default"
          />
        </div>
        {this.state.errorMessage && (
          <div className="alert alert-danger" role="alert">
            {this.state.errorMessage}
            <i className="bi bi-exclamation-circle-fill"></i>
          </div>
        )}
        <div className="button-div">
          <button
            className="btn btn-primary button-post"
            onClick={this.postData}
            disabled={this.state.loading} // Disable button during loading
          >
            {this.state.loading ? (
              <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            ) : (
              'Submit'
            )}
          </button>
        </div>
        {this.state.resultData && (
          <div className="result">
            <p className="result-link">Your Google Calendar event link:</p>
            <a target="_blank" href={this.state.resultData}>Click to view your event on the calendar</a>
          </div>
        )}
      </div>
    );
  }
}

export default MainPage;

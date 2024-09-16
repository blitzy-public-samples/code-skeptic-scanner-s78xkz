import React, { useState, useEffect } from 'react';
import { fetchSettings, updateSettings } from '../services/api';
import { Settings } from '../schema/types';

// HUMAN ASSISTANCE NEEDED
// The following component may need additional refinement for production readiness.
// Please review and enhance form validation, error handling, and UI/UX as needed.

const SettingsPanel: React.FC = () => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const fetchedSettings = await fetchSettings();
        setSettings(fetchedSettings);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to load settings. Please try again.');
        setIsLoading(false);
      }
    };

    loadSettings();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (settings) {
      setSettings({
        ...settings,
        [e.target.name]: e.target.value,
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (settings) {
      try {
        await updateSettings(settings);
        setSuccessMessage('Settings updated successfully!');
        setError(null);
      } catch (err) {
        setError('Failed to update settings. Please try again.');
        setSuccessMessage(null);
      }
    }
  };

  if (isLoading) {
    return <div>Loading settings...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!settings) {
    return <div>No settings available.</div>;
  }

  return (
    <div className="settings-panel">
      <h2>Application Settings</h2>
      <form onSubmit={handleSubmit}>
        {Object.entries(settings).map(([key, value]) => (
          <div key={key} className="form-group">
            <label htmlFor={key}>{key}</label>
            <input
              type="text"
              id={key}
              name={key}
              value={value}
              onChange={handleInputChange}
            />
          </div>
        ))}
        <button type="submit">Save Settings</button>
      </form>
      {successMessage && <div className="success">{successMessage}</div>}
    </div>
  );
};

export default SettingsPanel;
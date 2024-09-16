import React, { useState, useEffect } from 'react';
import { SettingsPanel } from '../components/SettingsPanel';
import { fetchSettings, updateSettings } from '../services/api';
import { useSelector, useDispatch } from '../store/settingsSlice';

// HUMAN ASSISTANCE NEEDED
// The confidence level is below 0.8, so this component may need review and potential improvements.
// Additionally, the exact structure of the settings object and the implementation of the Redux slice are not provided,
// so some assumptions have been made. Please review and adjust as necessary.

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const dispatch = useDispatch();
  const storedSettings = useSelector((state: any) => state.settings);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        setIsLoading(true);
        const fetchedSettings = await fetchSettings();
        setSettings(fetchedSettings);
        dispatch({ type: 'settings/setSettings', payload: fetchedSettings });
      } catch (err) {
        setError('Failed to load settings. Please try again.');
        console.error('Error fetching settings:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadSettings();
  }, [dispatch]);

  const handleSettingsUpdate = async (updatedSettings: any) => {
    try {
      setIsLoading(true);
      await updateSettings(updatedSettings);
      setSettings(updatedSettings);
      dispatch({ type: 'settings/setSettings', payload: updatedSettings });
    } catch (err) {
      setError('Failed to update settings. Please try again.');
      console.error('Error updating settings:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div>Loading settings...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Settings</h1>
      {settings && (
        <SettingsPanel
          settings={settings}
          onUpdate={handleSettingsUpdate}
        />
      )}
    </div>
  );
};

export default Settings;
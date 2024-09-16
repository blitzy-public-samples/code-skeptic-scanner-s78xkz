import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import ResponseList from '../components/ResponseList';
import { fetchResponses, updateResponse } from '../services/api';
import { setResponses } from '../store/responseSlice';

// HUMAN ASSISTANCE NEEDED
// The confidence level is below 0.8, so this component might need further refinement or additional features.
// Please review and enhance as necessary.

const ResponseManagement: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const responses = useSelector((state: any) => state.responses.items);
  const dispatch = useDispatch();

  useEffect(() => {
    const loadResponses = async () => {
      try {
        setLoading(true);
        const fetchedResponses = await fetchResponses();
        dispatch(setResponses(fetchedResponses));
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch responses');
        setLoading(false);
      }
    };

    loadResponses();
  }, [dispatch]);

  const handleResponseUpdate = async (id: string, approved: boolean) => {
    try {
      await updateResponse(id, { approved });
      const updatedResponses = responses.map((response: any) =>
        response.id === id ? { ...response, approved } : response
      );
      dispatch(setResponses(updatedResponses));
    } catch (err) {
      setError('Failed to update response');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Response Management</h1>
      <ResponseList responses={responses} onUpdateResponse={handleResponseUpdate} />
    </div>
  );
};

export default ResponseManagement;
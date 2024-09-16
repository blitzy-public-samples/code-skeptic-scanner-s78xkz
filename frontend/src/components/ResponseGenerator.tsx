import React, { useState } from 'react';
import { Tweet, Response, ResponseGeneratorProps } from '../schema/types';
import { generateResponse } from '../services/api';

// HUMAN ASSISTANCE NEEDED
// The following component needs review and potential improvements for production readiness.
// The confidence level is below 0.8, indicating that some aspects might need refinement.

const ResponseGenerator: React.FC<ResponseGeneratorProps> = ({ selectedTweet, onResponseApproved }) => {
  const [customPrompt, setCustomPrompt] = useState('');
  const [context, setContext] = useState('');
  const [generatedResponse, setGeneratedResponse] = useState<Response | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  const handleGenerateResponse = async () => {
    try {
      const response = await generateResponse(selectedTweet, customPrompt, context);
      setGeneratedResponse(response);
    } catch (error) {
      console.error('Error generating response:', error);
      // TODO: Implement proper error handling and user feedback
    }
  };

  const handleEditResponse = () => {
    setIsEditing(true);
  };

  const handleSaveEdit = () => {
    setIsEditing(false);
    // TODO: Implement logic to save edited response
  };

  const handleApproveAndPost = () => {
    if (generatedResponse) {
      onResponseApproved(generatedResponse);
    }
  };

  return (
    <div className="response-generator">
      <div className="selected-tweet">
        <h3>Selected Tweet</h3>
        <p>{selectedTweet.text}</p>
        <p>By: {selectedTweet.author}</p>
      </div>

      <div className="custom-inputs">
        <input
          type="text"
          value={customPrompt}
          onChange={(e) => setCustomPrompt(e.target.value)}
          placeholder="Custom prompt"
        />
        <textarea
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Additional context"
        />
      </div>

      <button onClick={handleGenerateResponse}>Generate Response</button>

      {generatedResponse && (
        <div className="generated-response">
          <h3>Generated Response</h3>
          {isEditing ? (
            <>
              <textarea
                value={generatedResponse.text}
                onChange={(e) => setGeneratedResponse({ ...generatedResponse, text: e.target.value })}
              />
              <button onClick={handleSaveEdit}>Save Edit</button>
            </>
          ) : (
            <>
              <p>{generatedResponse.text}</p>
              <button onClick={handleEditResponse}>Edit</button>
            </>
          )}
          <button onClick={handleApproveAndPost}>Approve and Post</button>
        </div>
      )}
    </div>
  );
};

export default ResponseGenerator;
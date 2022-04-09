import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const Transcribe = ({ parentCallback }) => {

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  async function stopClicked() {
    SpeechRecognition.stopListening();
    parentCallback(transcript);
  }

  async function resetClicked() {
    resetTranscript();
    parentCallback('');
  }

  return (
    <div>
      <h4>Transcribe speech to search</h4>
      <p>Microphone: {listening ? 'on' : 'off'}</p>
      <button onClick={SpeechRecognition.startListening} style={{width: '100px', margin: '2px'}}>Start</button>
      <button onClick={() => stopClicked()} style={{width: '100px', margin: '2px'}}>Stop</button>
      <button onClick={() => resetClicked()} style={{width: '100px', margin: '2px'}}>Reset</button>
    </div>
  );
};
export default Transcribe;
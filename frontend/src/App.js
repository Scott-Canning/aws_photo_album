import React, { useCallback } from 'react';
import './App.css';
import axios from 'axios';
import UploadImage from './UploadImage';
import Transcribe from './Transcribe';

function App() {
  const [search, setSearch] = React.useState("");
  const [searchResponse, setSearchResponse] = React.useState([]);

  async function searchClicked() {
    const base_url = 'https://<REST-API-ID>.execute-api.us-east-1.amazonaws.com/prod/search?q=';
    const params = search;
    const url = base_url + params;
    let response;
    try {
      response = await axios.get(url);
      setSearchResponse(response.data);
    } catch(err) {
      alert("No pictures matched your query.")
      setSearchResponse([]);
    }

    setSearchResponse(response.data);
    console.log(response.data);
  };

  const callback = useCallback((search) => {
    setSearch(search);
  }, []);

  return (
    <div>
      <div className="App">
        <div className="header-container">
          <h1 style={{padding: '5px', margin: 'auto', fontFamily: 'futura'}}>Photo Search</h1>
        </div>
          <div className="container">
            <div className="sub-container">
              <div className="search-wrapper">
                <div className="search">
                    <input value={search} onInput={e => setSearch(e.target.value)} 
                                          onKeyDown={e => {if(e.key ==='Enter'){searchClicked()}}}/>

                    <div className="search-button">
                      <button  onClick={searchClicked}> Search </button>
                    </div>
                </div>

              </div>
          </div>
        </div>
        <div className="container" style={{height: '102px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <Transcribe parentCallback={callback}/>
        </div>
        <div className="container" style={{height: '250px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          {
            searchResponse.map((_, i) => {
              return (
                <img src={searchResponse[i]} alt="display" style={{width: '200px', padding: '1px', borderRadius: '5px'}}/>
              )
            })
          }
        </div>
        <div className="header-container">
          <h1 style={{padding: '5px', margin: 'auto', fontFamily: 'futura'}}>Photo Upload</h1>
        </div>
        <div className="container">
          <UploadImage/>
        </div>
      </div>
    </div>

  );
}

export default App;

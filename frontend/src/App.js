import React from 'react';
import './App.css';

function App() {
  const [search, setSearch] = React.useState("");
  
  // placeholder search function to be piped to the SDK
  function searchClicked() {
    console.log(search);
  }

  return (
    <div className="App">
      <div className="header-container">
          <h1 style={{padding: '5px', margin: 'auto', fontFamily: 'futura'}}>Photo Search</h1>
      </div>
        <div className="container">
          <div className="sub-container">
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
  );
}

export default App;

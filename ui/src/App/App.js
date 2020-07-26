import React, { useState, useEffect } from 'react'; // eslint-disable-line

// this comment tells babel to use emotion's jsx function instead of React.createElement
/** @jsx jsx */
import { css, jsx } from '@emotion/core';

const CLIPS = [
  ['00:01:19.193', '00:01:23.463', 'my name is peter parker'],
  ['00:02:28.162', '00:02:33.798', "there's only one spider-man"],
  ['00:06:16.724', '00:06:23.828', 'i love you, dad'],
].map((x) => ({ start: x[0], end: x[1], label: x[2] }));

class GenericAPI {
  constructor() {
    this.urlBase = '/api/';
  }

  async cut(start, end) {
    const response = await fetch(
      this.urlBase + 'cut?' + new URLSearchParams({ start, end }).toString()
    );
    return response.text();
  }

  async subtitles() {
    const response = await fetch(this.urlBase + 'subtitles?movie_id=0');
    return response.json();
  }

  async search(serachTerm) {
    const response = await fetch(
      this.urlBase +
        'search?' +
        new URLSearchParams({ search_term: serachTerm }).toString(),
    );
    return response.json();
  }
}

const API = new GenericAPI();

const appStyle = css`
  position: absolute;
  height: 100%;
  width: 100%;
  max-width: 1200px;
  display: grid;
  grid-template-rows: [header] 100px [output] 1fr [end];
  grid-template-columns: [left] 50% [right] 50%;
`;

const headerStyle = css`
  grid-row: header;
  grid-column-start: left;
  grid-column-end: end;
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const titleStyle = css`
  margin-right: 30px;
`;

const linesStyle = css`
  grid-row: output;
  grid-column: left;
  overflow: scroll;
  background-color: #efefef;
`;

const viewerStyle = css`
  grid-row: output;
  grid-column: right;
`;

const GifState = { none: 'none', loading: 'loading', ready: 'ready' };

function App() {
  const [gifURL, setGIFURL] = useState(null);
  return (
    <div css={appStyle}>
      <div css={headerStyle}>
        <h1 css={titleStyle}>Quipper</h1>
        <Search />
      </div>
      <div css={linesStyle}>
        <Lines setGIFURL={setGIFURL} />
      </div>
      <div css={viewerStyle}>
        <GIFLoader src={gifURL} />
      </div>
    </div>
  );
}

const searchStyle = css`
  flex: 1;
  display: flex;
`;

const inputStyle = css`
  border: solid #ccc 1px;
  padding: 0 8px;
  height: 30px;
  flex: 1;
  margin-right: 8px;
  line-height: 32px;
  font-size: 18px;
`;

function Search() {
  const [searchTerm, setSearchTerm] = useState('');
  const onSearchTermChange = (event) => {
    const value = event.target.value;
    setSearchTerm(value);
  };
  const onClickSearch = () => {
    API.search(searchTerm);
  };
  return (
    <div css={searchStyle}>
      <input
        value={searchTerm}
        onChange={onSearchTermChange}
        css={inputStyle}
      />
      <button onClick={onClickSearch}>Search!</button>
    </div>
  );
}

const lineStyle = css`
  &:hover {
    background-color: rgb(200, 200, 255);
    cursor: pointer;
  }
`;

function Lines({ setGIFURL }) {
  const [loading, setLoading] = useState(true);
  const [lines, setLines] = useState([]);

  useEffect(() => {
    API.subtitles().then((data) => {
      setLines(data);
    });
  }, []);

  // TODO: obviously the dangerouslySetInnerHTML, below, must go!

  return (
    <div>
      {lines.map((line) => (
        <div
          css={lineStyle}
          key={line.start}
          onClick={async (e) => {
            setGIFURL(await API.cut(line.start, line.end));
          }}
        >
          <span dangerouslySetInnerHTML={{ __html: line.text }} />
        </div>
      ))}
    </div>
  );
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function GIFLoader({ src }) {
  const [status, setStatus] = useState(src ? GifState.loading : GifState.none);

  async function fetchGIF() {
    while (true) {
      const response = await fetch(src);
      const mime = response.headers.get('Content-Type');
      if (mime.startsWith('text/plain')) {
        await delay(1000);
        continue;
      } else if (mime === 'image/gif') {
        setStatus(GifState.ready);
        break;
      } else {
        console.error('unexpected mime-type:', mime);
      }
    }
  }

  useEffect(() => {
    if (src) {
      setStatus(GifState.loading);
      fetchGIF();
    }
  }, [src]);

  if (status === GifState.none || !src) {
    return null;
  } else if (status === GifState.loading) {
    return <div>loading...</div>;
  } else if (status === GifState.ready) {
    return <img src={src} />;
  }
}

export default App;

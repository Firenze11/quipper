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
}

const API = new GenericAPI();

const appStyle = css`
  padding: 10px;
`;

const lineStyle = css`
  color: blue;
  cursor: pointer;
  margin-bottom: 10px;
`;

const GifState = { none: 'none', loading: 'loading', ready: 'ready' };

function App() {
  //useEffect(() => fetch('http://localhost:3000/subtitles/?movie_id=123'), []);
  return (
    <div css={appStyle}>
      <ClipDemo />
    </div>
  );
}

function ClipDemo() {
  const [gifURL, setGIFURL] = useState(null);
  //useEffect(() => fetch('http://localhost:3000/subtitles/?movie_id=123'), []);
  return (
    <div>
      {CLIPS.map((clip) => (
        <div
          key={clip.start}
          css={lineStyle}
          onClick={async (e) => {
            setGIFURL(await API.cut(clip.start, clip.end));
          }}
        >
          {clip.label}
        </div>
      ))}

      <GIFLoader src={gifURL} />
    </div>
  );
}

function GIFLoader({ src }) {
  const [status, setStatus] = useState(src ? GifState.loading : GifState.none);

  useEffect(() => {
    console.log('effect', status, src);
    //setStatus(src ? GifState.loading : GifState.none);
    if (status !== GifState.ready && src) {
      console.log('making request now');
      fetch(src).then((response) => {
        const mime = response.headers.get('Content-Type');
        console.log('we got a response');
        if (mime === 'text/plain') {
          console.log('still waiting...');
        } else if (mime === 'image/gif') {
          console.log('got a gif');
          setStatus(GifState.ready);
        } else {
          console.log(mime);
        }
      });
    } else {
      console.log('not loading', status, src);
    }
  });

  console.log('render', status, src);

  if (status === GifState.none || !src) {
    return null;
  } else if (status === GifState.loading) {
    return <div>loading...</div>;
  } else if (status === GifState.ready) {
    return <img src={src} />;
  }
}

export default App;

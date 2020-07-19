import React from 'react'
import AppHome from './App'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={AppHome}></Route>
      </Switch>
    </Router>
  )
}

export default App

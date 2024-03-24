import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Login';
import Profile from './components/Profile';
import GameUpload from './components/GameUpload';
import Insights from './components/Insights';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/" exact component={Login} />
                    <Route path="/profile" component={Profile} />
                    <Route path="/upload" component={GameUpload} />
                    <Route path="/insights" component={Insights} />
                    {/* Redirect user to Login page if route does not exist and user is not authenticated */}
                    <Route path="*" component={Login} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;

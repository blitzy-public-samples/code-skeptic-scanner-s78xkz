import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Provider } from '@reduxjs/toolkit';
import { store } from './store';
import Dashboard from './components/Dashboard';
import TweetManagement from './pages/TweetManagement';
import ResponseManagement from './pages/ResponseManagement';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import Header from './components/Header';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <div className="app-container">
          <Header />
          <main>
            <Switch>
              <Route exact path="/" component={Dashboard} />
              <Route path="/tweets" component={TweetManagement} />
              <Route path="/responses" component={ResponseManagement} />
              <Route path="/analytics" component={Analytics} />
              <Route path="/settings" component={Settings} />
            </Switch>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </Provider>
  );
};

export default App;
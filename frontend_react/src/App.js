import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import React from 'react';
import { Container } from 'react-bootstrap';

import WorldAPI from './api';
import { AreaSearch, Country } from './components';


export default class App extends React.Component {
  state = {
    countrySearchParams: null,
  }

  constructor(props) {
    super(props);
    this.worldAPI = new WorldAPI();
  }

  onCountrySelected(countrySearchParams) {
    this.setState({ countrySearchParams });
  }

  render() {
    return (
      <Container className="App">
        <AreaSearch api={this.worldAPI} onCountrySelected={(countrySearchParams) => this.onCountrySelected(countrySearchParams)}/>
        { this.state.countrySearchParams &&
          <Country searchParams={this.state.countrySearchParams} api={this.worldAPI}/>
        }
      </Container>
    )
  }
}

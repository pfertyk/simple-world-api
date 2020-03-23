import React from 'react';
import { ListGroup, Badge, Button, Modal, Form } from 'react-bootstrap';

export class AreaSearch extends React.Component {
  state = {
    header: '',
    searchParams: [],
    searchResults: [],
  }

  constructor(props) {
    super(props);
    this.api = props.api;
    this.onCountrySelected = props.onCountrySelected;
  }

  componentDidMount() {
    this.search();
  }

  search() {
    // With the current API structure it is possible to reach a country by
    // providing subsequent parameters: continent, region, country code
    // The frontend part reflects this structure
    if (this.state.searchParams.length === 3) {
      this.onCountrySelected(this.state.searchParams);
      return;
    } else {
      this.onCountrySelected(null);
    }

    let headerMap = {
      0: 'Continents',
      1: 'Regions',
      2: 'Countries'
    }

    this.api.search(this.state.searchParams).then((results) => {
      this.setState({
        searchResults: results,
        header: headerMap[this.state.searchParams.length],
      });
    });
  }

  searchDeeper(param) {
    let newParams = this.state.searchParams;
    newParams.push(param);
    this.setState({ searchParams: newParams });
    this.search();
  }

  searchBack() {
    let newParams = this.state.searchParams;
    newParams.pop();
    this.setState({ searchParams: newParams });
    this.search();
  }

  render() {
    return (
      <>
        { this.state.searchParams.length > 0 &&
          <Button className={'float-right'} onClick={() => this.searchBack()}>Back</Button>
        }
        { this.state.searchParams.length < 3 &&
          <>
          <h2>{this.state.header}</h2>
          <ListGroup>
            {this.state.searchResults.map(result => (
              <ListGroup.Item key={result.name} onClick={() => this.searchDeeper(result.code)}>{result.name}</ListGroup.Item>
            ))}
          </ListGroup>
          </>
        }
      </>
    )
  }
}

export class Country extends React.Component {
  state = {
    country: {},
    showModal: false,
    city: {},
  }

  constructor(props) {
    super(props);
    this.api = props.api;
  }

  componentDidMount() {
    this.getCountry();
  }

  getCountry() {
    this.api.search(this.props.searchParams).then(country => {
      this.setState({ country });
    });
  }

  deleteCity(cityId) {
    this.api.deleteCity(cityId).then(() => {
      this.getCountry();
    });
  }

  showCityModal(city) {
    let cityClone = Object.assign({}, city);
    this.setState({ showModal: true, city: cityClone });
  }

  saveCity() {
    this.setState({ showModal: false });
    let city = this.state.city;
    // Make sure that the city will be assigned to the current country
    city.country = this.state.country.code;

    let action = null

    if (city.id) {
      action = this.api.updateCity(city);
    } else {
      action = this.api.createCity(city);
    }

    action.then(() => {
      this.getCountry();
      this.setState({ city: {} });
    });
  }

  onCityChange(e) {
    let city = this.state.city;

    const value = e.target.value;
    const name = e.target.name;
    city[name] = value;

    this.setState({ city });
  }

  render() {
    let country = this.state.country;
    if (!country.name) {
      return <></>
    }
    country.cities.sort((a, b) => { return a.name.localeCompare(b.name); });
    country.languages.sort((a, b) => { return a.name.localeCompare(b.name); });

    return (
      <>
        <h2>{country.name}</h2>
        <div>
          <strong>Code:</strong> {country.code}
        </div>
        <div>
          <strong>ISO code:</strong> {country.iso_code}
        </div>
        <div>
          <strong>Local name:</strong> {country.local_name}
        </div>
        <div>
          <strong>Form of government:</strong> {country.government_form}
        </div>
        <div>
          <strong>Head of state:</strong> {country.head_of_state}
        </div>
        <div>
          <strong>Surface:</strong> {country.surface_area}km2
        </div>
        <div>
          <strong>Year of independence:</strong> {country.independence_year}
        </div>
        <div>
          <strong>Population:</strong> {country.population}
        </div>
        <div>
          <strong>Life expectancy:</strong> {country.life_expectancy} years
        </div>
        <div>
          <strong>GNP:</strong> {country.GNP} {country.gnp_old &&
            <span>(old {country.gnp_old})</span>
          }
        </div>
          <h3>Cities
            <Button className={'float-right'} onClick={() => this.showCityModal({})}>New</Button>
          </h3>
          <ListGroup>
            {country.cities.map(city => (
              <ListGroup.Item key={city.id}>
                <div>{city.name}
                {city.id === country.capital &&
                    <span>&nbsp;
                      <Badge variant="primary">capital</Badge>
                    </span>
                }
                <Button className={'float-right'} variant="danger" size="sm" onClick={()=>this.deleteCity(city.id)}>Delete</Button>
                <Button className={'float-right'} variant="primary" size="sm" onClick={()=>this.showCityModal(city)}>Edit</Button>
                </div>
                <div>District {city.district}</div>
                <div>Population {city.population}</div>
              </ListGroup.Item>
            ))}
          </ListGroup>
          <h3>Languages</h3>
          <ListGroup>
            {country.languages.map(language => (
              <ListGroup.Item key={language.name}>
                {language.name} ({language.percentage}%)
                {language.is_official &&
                    <span>&nbsp;
                      <Badge variant="info">official</Badge>
                    </span>
                }
              </ListGroup.Item>
            ))}
          </ListGroup>
        <Modal show={this.state.showModal}>
          <Modal.Header>{this.state.city.id ? "Edit city" : "Add city"}</Modal.Header>
          <Modal.Body>
            <Form.Label>Name</Form.Label>
              <Form.Control required type="text" name="name" value={this.state.city.name} onChange={(e) => this.onCityChange(e)}/>
            <Form.Label>District</Form.Label>
              <Form.Control required type="text" name="district" value={this.state.city.district} onChange={(e) => this.onCityChange(e)}/>
            <Form.Label>Population</Form.Label>
              <Form.Control required type="number" name="population" min="1" step="1" value={this.state.city.population} onChange={(e) => this.onCityChange(e)}/>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => this.setState({ showModal: false }) }>Cancel</Button>
            <Button variand="primary" onClick={() => this.saveCity() }>Save</Button>
          </Modal.Footer>
        </Modal>
      </>
    )
  }
}

import axios from 'axios';

const BASE_API_URL = 'http://127.0.0.1:8000/api/';

export default class WorldAPI {
  constructor() {
    this.client = axios.create({
      baseURL: BASE_API_URL,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  search(params) {
    let path = params.join('/') + '/';

    return this.client.get(path).then(response => {
      return response.data;
    });
  }

  getCountry(params) {
    return this.search(params);
  }

  deleteCity(cityId) {
    return this.client.delete('cities/' + cityId +'/');
  }

  updateCity(city) {
    return this.client.patch('cities/' + city.id +'/', city);
  }

  createCity(city) {
    return this.client.post('cities/', city);
  }
}

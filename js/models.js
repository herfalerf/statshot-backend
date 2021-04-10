"use strict";

const BASE_URL = "http://localhost:5000";

let tt;

// Setup User class and related functions
class User {
  constructor({ username, userId, favTeamId }) {
    this.username = username;
    this.userId = userId;
  }

  static async signup(username, password) {
    let response = await axios.post(
      `${BASE_URL}/api/users/register`,
      {
        username,
        password,
      },
      { withCredentials: true }
    );
    console.log(`this is the signup ${response}`);
    let newUser = new User(response.data.user);
    console.log(`this is a new user from signup`, newUser);
    return newUser;
  }

  static async login(username, password) {
    let response = await axios.post(
      `${BASE_URL}/api/users/login`,
      {
        username,
        password,
      },
      { withCredentials: true }
    );
    console.log(`this is the login ${response}`);
    let returnUser = new User(response.data.user);
    console.log(`this is a new user from signup`, returnUser);
    return returnUser;
  }

  static async checkSession() {
    let response = await axios({
      method: "get",
      url: `${BASE_URL}/api/users/session`,
      withCredentials: true,
    });

    let sessUser = new User(response.data.user);

    return sessUser;
  }

  static async testSession() {
    let response = await axios.get(`${BASE_URL}/api/users/session`, {
      withCredentials: true,
    });
    let testSess = response.data.user;
    return testSess;
  }

  static async logout() {
    let response = await axios({
      method: "post",
      url: `${BASE_URL}/api/users/logout`,
      withCredentials: true,
    });

    console.log(response.data);
    return response;
  }
}

// Setup Team class and related functions
class Team {
  constructor({ name, id }) {
    this.name = name;
    this.id = id;
  }

  static async getTeams() {
    let response = await axios.get(`${BASE_URL}/api/teams`, {
      withCredentials: true,
    });
    console.log(response.data.teams);

    return response.data.teams;
  }
  static async getTeamStats(teamId) {
    let response = await axios.get(`${BASE_URL}/api/teams/${teamId}`, {
      withCredentials: true,
    });
    console.log(response.data.teams[0].teamStats[0].splits[0].stat);
  }
}

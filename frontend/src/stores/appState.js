import Vuex from "vuex";

const store = new Vuex.Store({
  state: {
    BASEURL: "http://localhost:5000",
    TOKEN: "",
    USER: {
      id: null,
      username: "",
      role: "",
      isAuthenticated: false,
    },
  },
  getters: {
    getToken: (state) => state.TOKEN,
    getUser: (state) => state.USER,
    isAuthenticated: (state) => state.USER.isAuthenticated,
    getBaseUrl: (state) => state.BASEURL,
    getUserId: (state) => state.USER.id,
    getUsername: (state) => state.USER.username,
    getRole: (state) => state.USER.role,
  },
  mutations: {
    setToken(state, token) {
      state.TOKEN = token;
    },
    setUser(state, user) {
      state.USER = { ...state.USER, ...user };
    },
    setIsAuthenticated(state, isAuthenticated) {
      state.USER.isAuthenticated = isAuthenticated;
    },
  },
  actions: {
    updateToken({ commit }, token) {
      commit("setToken", token);
    },
    updateUser({ commit }, user) {
      commit("setUser", user);
    },
    updateAuthentication({ commit }, isAuthenticated) {
      commit("setIsAuthenticated", isAuthenticated);
    },
  },
});

export default store;

export function getToken() {
  return store.state.TOKEN;
}

export function getUser() {
  return store.state.USER;
}

export function isAuthenticated() {
  return store.state.USER.isAuthenticated;
}

export function getBaseUrl() {
  return store.state.BASEURL;
}

export function getUserId() {
  return store.state.USER.id;
}

export function getUsername() {
  return store.state.USER.username;
}

export function getEmail() {
  return store.state.USER.email;
}

export function getRole() {
  return store.state.USER.role;
}

export function setToken(token) {
  store.dispatch("updateToken", token);
}

export function setUser(user) {
  store.dispatch("updateUser", user);
}

export function setIsAuthenticated(isAuthenticated) {
  store.dispatch("updateAuthentication", isAuthenticated);
}

export function setBaseUrl(baseUrl) {
  store.state.BASEURL = baseUrl;
}

export function setUserId(id) {
  store.state.USER.id = id;
}

export function setUsername(username) {
  store.state.USER.username = username;
}

export function setEmail(email) {
  store.state.USER.email = email;
}

export function setRole(role) {
  store.state.USER.role = role;
}

export function logout() {
  store.state.TOKEN = "";
  store.state.USER = {
    id: null,
    username: "",
    role: "",
    isAuthenticated: false,
  };
}
export async function make_getrequest(url, params = {}) {
  // Build query string from params
  const queryString = Object.keys(params).length
    ? "?" + new URLSearchParams(params).toString()
    : "";
  const response = await fetch(`${store.state.BASEURL}${url}${queryString}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${store.state.TOKEN}`,
    },
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const data = await response.json();
  return data;
}

export async function make_postrequest(url, data = {}) {
  const response = await fetch(`${store.state.BASEURL}${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${store.state.TOKEN}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const responseData = await response.json();
  return responseData;
}

export function returnStoreData() {
  return {
    BASEURL: store.state.BASEURL,
    TOKEN: store.state.TOKEN,
    USER: store.state.USER,
  };
}

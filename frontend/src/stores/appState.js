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

export function resetUser() {
  store.state.USER = {
    id: null,
    username: "",
    role: "",
    isAuthenticated: false,
  };
}

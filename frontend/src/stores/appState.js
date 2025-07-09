import axios from "axios";
import Vuex from "vuex";

const store = new Vuex.Store({
  state: {
    BASEURL: "http://localhost:5000/api",
    TOKEN: localStorage.getItem("token") || "",
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
    clearUserState(state) {
      state.TOKEN = "";
      state.USER = {
        id: null,
        username: "",
        role: "",
        isAuthenticated: false,
      };
    },
  },
  actions: {
    updateToken({ commit }, token) {
      commit("setToken", token);
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },
    updateUser({ commit }, user) {
      commit("setUser", user);
    },
    updateAuthentication({ commit }, isAuthenticated) {
      commit("setIsAuthenticated", isAuthenticated);
    },
    clearAll({ commit }) {
      commit("clearUserState");
      localStorage.removeItem("token");
    },
  },
});

export default store;

// Helper functions
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

export function setToken(token) {
  store.dispatch("updateToken", token);
}

export function setUser(user) {
  store.dispatch("updateUser", user);
}

export function setIsAuthenticated(isAuthenticated) {
  store.dispatch("updateAuthentication", isAuthenticated);
}

export async function logout() {
  try {
    const token = store.state.TOKEN;

    if (token) {
      const response = await axios.post(
        `${store.state.BASEURL}/logout`,
        {
          subject: token, // or whatever string the server expects
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Logout API response:", response.data);
    } else {
      console.log("No token found, skipping API call");
    }
  } catch (error) {
    console.error("Logout API call failed:", error);
  } finally {
    console.log("Clearing client-side state...");
    store.dispatch("clearAll");
  }

  return store.state.USER;
}

export async function make_getrequest(url, params = {}) {
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

// Initialize authentication state on app start
export function initializeAuth() {
  const token = localStorage.getItem("token");
  if (token) {
    store.dispatch("updateToken", token);
    // You might want to validate the token here by making an API call
    // For now, just set authenticated to true if token exists
    store.dispatch("updateAuthentication", true);
  }
}

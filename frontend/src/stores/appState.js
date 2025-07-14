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
    isTokenValidating: false,
  },
  getters: {
    getToken: (state) => state.TOKEN,
    getUser: (state) => state.USER,
    isAuthenticated: (state) => state.USER.isAuthenticated,
    getBaseUrl: (state) => state.BASEURL,
    getUserId: (state) => state.USER.id,
    getUsername: (state) => state.USER.username,
    getRole: (state) => state.USER.role,
    isTokenValidating: (state) => state.isTokenValidating,
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
    setTokenValidating(state, isValidating) {
      state.isTokenValidating = isValidating;
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

    async validateToken({ commit, state }) {
      const token = state.TOKEN;
      if (!token) {
        commit("setIsAuthenticated", false);
        return false;
      }

      commit("setTokenValidating", true);

      try {
        const response = await axios.post(
          `${state.BASEURL}/check_token_valid`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status === 200) {
          commit("setIsAuthenticated", true);

          if (response.data.claims) {
            const userInfo = {
              id: response.data.claims.sub || response.data.claims.user_id,
              username:
                response.data.claims.username || response.data.claims.identity,
              role: response.data.claims.role,
            };
            commit("setUser", userInfo);
          }
          return true;
        } else {
          throw new Error("Token validation failed");
        }
      } catch (error) {
        console.error("Token validation error:", error);
        commit("setIsAuthenticated", false);
        commit("clearUserState");
        localStorage.removeItem("token");
        return false;
      } finally {
        commit("setTokenValidating", false);
      }
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
  return store.getters.getBaseUrl;
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

export function validateToken() {
  return store.dispatch("validateToken");
}

export async function logout() {
  try {
    const token = store.state.TOKEN;

    if (token) {
      const response = await axios.post(
        `${store.state.BASEURL}/logout`,
        {
          subject: token,
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
  console.log("API call successful:", response.data);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const data = await response.json();
  return data;
}

export async function make_postrequest(url, data = {}) {
  const token = localStorage.getItem("token") || store.state.TOKEN;
  const response = await fetch(`${store.state.BASEURL}${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  console.log("API call successful:", response);

  const responseData = await response.json();
  return responseData;
}

export async function make_putrequest(url, data = {}) {
  const token = localStorage.getItem("token") || store.state.TOKEN;
  const response = await fetch(`${store.state.BASEURL}${url}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
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

export async function initializeAuth() {
  const token = localStorage.getItem("token");
  if (token) {
    store.dispatch("updateToken", token);

    const isValid = await store.dispatch("validateToken");
    return isValid;
  }
  return false;
}

import { createSignal } from "solid-js";

const AUTH_COOKIE_NAME = "auth_token";

const [isAuthenticated, setIsAuthenticated] = createSignal(false);

async function login(token: string) {
  await cookieStore.set(AUTH_COOKIE_NAME, token);
  setIsAuthenticated(true);
  console.log("User logged in");
}

async function logout() {
  await cookieStore.delete(AUTH_COOKIE_NAME);
  setIsAuthenticated(false);
  console.log("User logged out");
}

export const authStore = {
  isAuthenticated,
  login,
  logout,
};
import { Show, type Component } from "solid-js";
import CallyDatePicker from "./DatePicker";
import { authStore } from "./stores/auth";

const App: Component = () => {
  const handleDateChange = (date: string) => {
    console.log("Selected date:", date);
  };

  const handleLoginClick = async () => {
    await authStore.login("example_token");
  };

  const handleLogoutClick = async () => {
    await authStore.logout();
  };
  return (
    <div class="text-center py-10">
      <Show
        when={authStore.isAuthenticated()}
        fallback={
          <div>
            <p class="text-lg text-red-600 md-4">You are not logined in</p>
            <button
              onClick={handleLoginClick}
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              log in
            </button>
          </div>
        }
      >
        <div>
          <p class="text-lg text-green-600 md-4">You are logined in</p>
          <button
            onclick={handleLogoutClick}
            class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red"
          >
            log out
          </button>
        </div>
      </Show>
    </div>
  );
};

export default App;

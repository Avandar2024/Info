import type { Component } from "solid-js";
import CallyDatePicker from "./test";

const App: Component = () => {
  const handleDateChange = (date: string) => {
    console.log("Selected date:", date);
  };
  return (
    <div>
      <p class="text-4xl text-green-700 text-center py-20">Hello tailwind!</p>
      <CallyDatePicker onDateChange={handleDateChange} />
    </div>
  );
};

export default App;

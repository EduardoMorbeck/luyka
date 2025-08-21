import { createApp } from "vue";
import { supabase } from "./supabaseClient.js";
import "./style.css";
import App from "./App.vue";
import router from "./router";

createApp(App).use(router).mount("#app");

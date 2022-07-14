<script>
  import Router, { link } from "svelte-spa-router";

  import Main from "./routes/Main.svelte";
  import Login from "./routes/Login.svelte";
  import Register from "./routes/Register.svelte";
  import Settings from "./routes/Settings.svelte";
  import News from "./routes/News.svelte";
</script>

<main>
  <Router
    routes={{
      "/": Main,
      "/login": Login,
      "/register": Register,
      "/settings": Settings,
      "/news/:id": News,
    }}
  />
</main>

<style>
  :global(body) {
    position: absolute;
    top: 0;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
</style>

<script>
  export let navbarType;
  export let navbarItems;
  export let background;
  export let color;
  export let isLogged;

  let active = false;
  const toggleMenu = () => {
    active ? (active = false) : (active = true);

    if (active) {
      document.getElementById("sideMenu").classList.remove("hide");
      document.getElementById("darkBg").classList.remove("hideBg");
    } else {
      document.getElementById("sideMenu").classList.add("hide");
      document.getElementById("darkBg").classList.add("hideBg");
    }
  };

  function logout() {
    localStorage.setItem("userLoginned", null);
    window.location.reload(true);
  }
</script>

<header style="background-color: {background};">
  {#if navbarType === "horizontal"}
    <div class="nav-container" style="padding: 0 20px;">
      <img class="icon" src="icon.png" alt="" />
    </div>
    <nav class="nav-container">
      <div class="nav-links nav-container" style="width: 100%;">
        {#each navbarItems as item}
          <a style="color: {color}" href={item.navbarLink}>{item.navbarText}</a>
        {/each}
      </div>
    </nav>

    {#if isLogged}
      <div class="links nav-container">
        <a
          href="/#/Settings"
          class="linkLogin"
          style="color: {color}; border-color:{color};">Settings</a
        >
        <a
          href="/#/"
          on:click={logout}
          class="linkRegister"
          style="color: {color}; border-color:{color};">Log Out</a
        >
      </div>
    {:else}
      <div class="links nav-container">
        <a
          href="/#/Login"
          class="linkLogin"
          style="color: {color}; border-color:{color};">Login</a
        >
        <a
          href="/#/Register"
          class="linkRegister"
          style="color: {color}; border-color:{color};">Register</a
        >
      </div>
    {/if}
  {:else}
    <div class="nav-container" style="padding: 0 20px; justify-content:start;">
      <img class="icon" src="icon.png" alt="" />
    </div>
    <div
      class="nav-container hamburger-menu"
      style="padding: 0 20px; justify-content:end;"
    >
      <div on:click={toggleMenu} class="menu-button">
        {#if active}
          <i class="fa fa-close" style="font-size:36px" />
        {:else}
          <i class="fa fa-bars" style="font-size:36px" />
        {/if}
      </div>
    </div>
  {/if}
</header>

{#if navbarType === "hamburger"}
  <div class="dark-bg hideBg" id="darkBg" />
  <div
    class="side-menu hide"
    style="background-color: {background};"
    id="sideMenu"
  >
    <nav>
      {#each navbarItems as item}
        <a style="color: {color}" href={item.navbarLink}>{item.navbarText}</a>
      {/each}
      {#if isLogged}
        <div class="side-links">
          <a
            href="/#/Settings"
            class="linkLogin"
            style="color: {color}; border-color:{color};">Settings</a
          >
          <a
            href="/#/"
            on:click={logout}
            class="linkRegister"
            style="color: {color}; border-color:{color};">Log Out</a
          >
        </div>
      {:else}
        <div class="side-links">
          <a
            href="/#/Login"
            class="linkLogin"
            style="color: {color}; border-color:{color};">Login</a
          >
          <a
            href="/#/Register"
            class="linkRegister"
            style="color: {color}; border-color:{color};">Register</a
          >
        </div>
      {/if}
    </nav>
  </div>
{/if}

<style>
  .dark-bg {
    transition: all ease 0.8s;
    position: fixed;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    z-index: 10;
    display: block;
    top: 116;
    opacity: 1;
  }
  .hideBg {
    opacity: 0;
    display: none;
  }
  header {
    position: fixed;
    display: flex;
    justify-content: space-around;
    z-index: 100;
    height: 120px;
    width: 100%;
  }
  .icon {
    width: 50px;
  }
  .nav-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  nav {
    width: 70%;
    max-width: 500px;
    z-index: 100;
  }
  .nav-links {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
  .nav-links a {
    text-decoration: none;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.4em;
    font-weight: 500;
  }
  .linkLogin {
    padding: 5px 10px;
    margin: 0 6px;
    border-radius: 10px;
    border: 1px solid green;
    text-decoration: none;
    color: green;
  }
  .linkRegister {
    padding: 5px 10px;
    border-radius: 10px;
    border: 1px solid #4747ff;
    text-decoration: none;
    color: #4747ff;
  }
  .menu-button {
    transition: all ease 0.8s;
    cursor: pointer;
  }
  .side-menu {
    width: 500px;
    height: 100%;
    z-index: 20;
    position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    transition: all ease 1s;
    right: 0px;
  }
  .side-menu nav {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .side-menu nav > a {
    margin: 20px;
  }
  .side-links {
    margin-top: 200px;
  }
  .hide {
    right: -500px;
  }
</style>

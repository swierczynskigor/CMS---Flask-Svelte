<script>
  import Themes from "../components/settings/themes.svelte";
  import Blocks from "../components/settings/blocks.svelte";
  import Menu from "../components/settings/menu.svelte";
  import Slider from "../components/settings/slider.svelte";
  import News from "../components/settings/news.svelte";
  import Content from "../components/settings/content.svelte";
  import Footer from "../components/settings/footer.svelte";
  import UserList from "../components/settings/userList.svelte";

  let username,
    permissionLevel,
    permission,
    selectedSetting,
    settingProps,
    menuHeight,
    importInput,
    importSubmit,
    importedSettings;

  username = localStorage.getItem("userLoginned");
  if (username == null || username == "null")
    document.location.href = "/#/Login";

  permissionLevel = "0";
  getPermission();

  async function getPermission() {
    const res = await fetch("./getPermission", {
      method: "POST",
      body: username,
    });

    permissionLevel = await res.text();

    if (permissionLevel == 0) {
      permission = "User";
      selectedSetting = "";
    } else if (permissionLevel == 1) {
      permission = "Privileged User";
      selectedSetting = News;
    } else if (permissionLevel == 2) {
      permission = "Admin";
      selectedSetting = Themes;
    }
  }

  function logout() {
    localStorage.setItem("userLoginned", null);
    document.location.href = "/#/Login";
  }

  function open(x) {
    switch (x) {
      case "themes":
        selectedSetting = Themes;
        settingProps = {};
        break;
      case "blocks":
        selectedSetting = Blocks;
        settingProps = {};
        break;
      case "menu":
        selectedSetting = Menu;
        settingProps = {};
        break;
      case "slider":
        selectedSetting = Slider;
        settingProps = {};
        break;
      case "news":
        selectedSetting = News;
        settingProps = {};
        break;
      case "content":
        selectedSetting = Content;
        settingProps = {};
        break;
      case "footer":
        selectedSetting = Footer;
        settingProps = {};
        break;
      case "userList":
        selectedSetting = UserList;
        settingProps = { permissionLevel: permissionLevel, username: username };
        break;
      default:
        console.log(`Failed to open: ${x}`);
    }
  }
</script>

<div class="settingsBox">
  <div class="nav flex-row">
    <div class="data flex-row">
      <div id="username">Username: <b id="dataUsername">{username}</b></div>
      <div id="permission">Permission: <b>{permission}</b></div>
    </div>

    <div class="control flex-row">   
      <form method=post enctype=multipart/form-data action="/importSettings">
        <input bind:this={importInput} bind:files={importedSettings} on:change={()=>importSubmit.click()} type="file" name="file" accept=".sql" style="display: none;">
        <button type="button" class="controlButton" on:click={()=>importInput.click()}>Import</button>
        <input bind:this={importSubmit} type=submit style="display: none;">
      </form>

      <button class="controlButton" on:click={() => {document.location = "/exportSettings"}}>Export</button>
      <a class="controlButton" href="/">Go to page</a>
      <button class="controlButton" on:click={logout}>Logout</button>
    </div>
  </div>

  <div class="flex-row">
    <div class="menu" bind:clientHeight={menuHeight}>
        {#if permissionLevel == 2}
            <div on:click={() => open("themes")}>Themes</div>
            <div on:click={() => open("blocks")}>Blocks</div>
            <div on:click={() => open("menu")}>Menu</div>
            <div on:click={() => open("slider")}>Slider</div>
        {/if}

        {#if permissionLevel > 0}
            <div on:click={() => open("news")}>News</div>
        {/if}

        {#if permissionLevel == 2}
            <div on:click={() => open("content")}>Content</div>
            <div on:click={() => open("footer")}>Footer</div>
        {/if}         
      
        <div on:click={() => open("userList")}>
            {#if permissionLevel == 2}
            User List
            {:else}
            Account settings
            {/if}
        </div>
    </div>

    <div class="settings" style="height: {menuHeight}px;">
      <svelte:component this={selectedSetting} {...settingProps} bind:selectedSetting={selectedSetting} />
    </div>
  </div>
</div>

<style>
  .settingsBox {
    width: 60%;

    margin: auto;
    margin-top: 100px;

    box-shadow: 0 0 20px 4px rgba(0, 0, 0, 0.25);
    /* box-shadow: 0 0 20px 4px rgba(255, 75, 43, 0.25); */
    border: 2px solid #ff4b2b;
    border-radius: 15px;

    overflow: hidden;
  }

  .nav {
    flex-wrap: wrap;
    justify-content: center;
    padding: 10px 10px;
    background-color: #ebebeb;
    border-bottom: 2px solid #ff4b2b;
  }

  .data {
    width: 50%;
    min-width: 210px;
    justify-content: left;
  }

  .data div {
    margin: 0px 20px;
  }

  .control {
    width: 50%;
    min-width: 200px;
    justify-content: right;
  }

  .controlButton {
    margin: 0px 10px;
    padding: 5px 10px;
    background-color: #f4f4f4;
    color: #333;
    white-space: nowrap;
    user-select: none;
    text-decoration: none;
    cursor: pointer;
    border: 1px solid #ccc;
    transition: all 0.2s ease-in-out;
  }

  .controlButton:hover {
    background-color: rgb(235, 235, 235);
  }

  .flex-row {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .menu {
    height: 100%;
    min-height: 600px;

    display: flex;
    flex-direction: column;
    align-items: center;
    /* justify-content: left; */
    justify-content: space-evenly;

    background-color: #ebebeb;
    border-right: 2px solid #ff4b2b;
  }

  .menu div {
    margin: 20px 15px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s ease-in-out;
    font-weight: bold;
  }

  .menu div:hover {
    color: #ff4b2b;
    transform: scale(1.1);
    transition: all 0.2s ease-in-out;
  }

  .settings {
    width: 100%;
    position: relative;

    display: flex;
    justify-content: center;
    align-items: center;

    overflow-y: auto;
    overflow-x: auto;
  }

  @media (max-width: 500px) {
    .settingsBox {
      width: 100%;
    }
  }
</style>

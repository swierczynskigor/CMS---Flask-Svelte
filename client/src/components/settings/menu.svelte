<script>
    import MenuElement from "./menuElement.svelte";
    
    let menuType, checkbox, menuList = [];   
    menuType = '0';

    loadMenu();
    getMenuType();

    async function loadMenu() {
        const res = await fetch('./getMenu', {
			method: 'POST'
        })

        menuList = await res.json()    
    }

    async function getMenuType() {
        const res = await fetch('./getMenuType', {
			method: 'POST'
        })

        let result = await res.text();
        if(result == 'horizontal') {
            menuType = '0';
            checkbox.checked = false;
        }else {
            menuType = '1';
            checkbox.checked = true;
        }
    }

    async function changeMenuType() {
        let menuString = "";

        if(menuType == '1') {
            menuType = '0';
            menuString = "horizontal";
        }else {
            menuType = '1';
            menuString = "hamburger";
        }

        

        const res = await fetch("./changeMenuType", {
            method: "POST",
            body: menuString,
            headers: {"content-type": "application/json"}
        });

        let result = await res.json();
        if (result.type != "success") {
            alert(result.message);
            return;
        }
    }
</script>

<div class="menuContainer">
    <label class="switch btn-color-mode-switch">
        <p>Menu type:</p> 
        <input bind:this={checkbox} on:change={changeMenuType} bind:value={menuType} type="checkbox" name="color_mode" id="color_mode">
        <label for="color_mode" data-on="Hamburger" data-off="Horizontal" class="btn-color-mode-switch-inner"></label>
    </label>

    <div class="menuList">
        <p>Menu Items:</p>
        {#each menuList as menu}
            <MenuElement {menu} bind:menuList={menuList}/>
	    {/each}
        <MenuElement menu={['','']} bind:menuList={menuList} />
    </div>
</div>

<style>
    .menuContainer {
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-evenly;
    }

    .menuList {
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
    }

    .btn-color-mode-switch p {
        width: 100%;
        text-align: center;
        margin: 0;
        margin-bottom: 5px;
    }

    #color_mode {
        display: none;
    }

    label {
        font-size: 13px;
        color: #424242;
        font-weight: 500;
        cursor: pointer;
    }

    .btn-color-mode-switch{
        display: inline-block;
        margin: 0;
        position: relative;  
    }

    .btn-color-mode-switch > label.btn-color-mode-switch-inner{
        margin: 0px;
        width: 180px;
        height: 30px;
        background: #E0E0E0;
        border-radius: 26px;
        overflow: hidden;
        position: relative;
        transition: all 0.3s ease;
        /*box-shadow: 0px 0px 8px 0px rgba(17, 17, 17, 0.34) inset;*/
        display: block;
    }

    .btn-color-mode-switch > label.btn-color-mode-switch-inner:before{
        content: attr(data-on);
        position: absolute;
        font-size: 12px;
        font-weight: 500;
        top: 7px;
        right: 20px;
    }

    .btn-color-mode-switch > label.btn-color-mode-switch-inner:after{
        content: attr(data-off);
        width: 90px;
        height: 16px;
        background: white;
        border-radius: 26px;
        position: absolute;
        left: 2px;
        top: 2px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0px 0px 6px -2px #111;
        padding: 5px 0px;
    }

    .btn-color-mode-switch input[type="checkbox"]{
        opacity: 0;
    }

    .btn-color-mode-switch input[type="checkbox"]:checked + label.btn-color-mode-switch-inner{
        left: 0;
    }

    .btn-color-mode-switch input[type="checkbox"]:checked + label.btn-color-mode-switch-inner:after{
        content: attr(data-on);
        left: 88px;
        background: white;
    }

    .btn-color-mode-switch input[type="checkbox"]:checked + label.btn-color-mode-switch-inner:before{
        content: attr(data-off);
        right: auto;
        left: 20px;
        color: white;
    }

    .btn-color-mode-switch label.btn-color-mode-switch-inner:before{
        color: white;
    }
</style>
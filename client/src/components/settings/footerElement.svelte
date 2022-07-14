<script>
    export let footer;
    export let footerList;
    let text, link, id, addOrSave, toSave, thisFooter;

    toSave = false;

    text = footer[0]
    link = footer[1]

    addOrSave = "Save";
    if(footer.length == 2) {
        addOrSave = 'Add';
    }else {
        id = footer[2];
    }
    
    async function save() {
        if(toSave == false) return;
        if(addOrSave == "Add") {
            const res = await fetch("./saveFooter", {
                method: "POST",
                body: JSON.stringify({
                    text: text,
                    link: link
                }),
                headers: {"content-type": "application/json"}
            });

            let result = await res.json();
            if (result.type != "success") {
                alert(result.message);
                return;
            }
            
            footerList = [...footerList, [text, link, result.message]]
            text = "";
            link = "";
            toSave = false;
        }else {
            const res = await fetch("./updateFooter", {
                method: "POST",
                body: JSON.stringify({
                    text: text,
                    link: link,
                    id: id
                }),
                headers: {"content-type": "application/json"}
            });

            let result = await res.json();
            if (result.type != "success") {
                alert(result.message);
                return;
            }

            toSave = false;
        }    
    }

    async function deleteFooter() {
        const res = await fetch("./deleteFooter", {
            method: "POST",
            body: id,
            headers: {"content-type": "application/json"}
        });

        let result = await res.json();
        if (result.type != "success") {
            alert(result.message);
            return;
        }   
        thisFooter.style.display = 'none';
    }

    function changed() {
       if(text != '' && link != ''){
           toSave = true;
       }else {
           toSave = false;
       }
    }
</script>

<div bind:this={thisFooter}> 
    <input bind:value={text} on:input={changed} type="text" name="text" placeholder="Item text" required>
    <input bind:value={link} on:input={changed} type="text" name="link" placeholder="Link url" required> 
    <button on:click={save} style='{toSave==true ? "color: white; background-color: #ff4b2b; border-color: #ff4b2b;" : ""} {addOrSave=="Add" ? "width: 110px;" : undefined}' disabled={!toSave}>{addOrSave}</button>
    {#if addOrSave == "Save"}
        <button on:click={deleteFooter} style='color: white; background-color: #262626; border-color: #262626; width: 60px;'>Delete</button>
    {/if} 
</div>

<style>
    button {
        width: 50px;
    }
</style>
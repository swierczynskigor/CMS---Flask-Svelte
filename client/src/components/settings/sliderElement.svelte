<script>
    import Slider from "./slider.svelte"
    export let slide;
    export let sliderList;
    export let selectedSetting;
    export let sortSlider = () => {};
    let text, image, order, id, fileInput, saveOrAdd, thisSlide, base64Image;

    text = "";
    image = "";
    order = -1;
    saveOrAdd = "Add"
    base64Image = "";

    if(slide != undefined) {
        text = slide[0];
        base64Image = slide[1]
        order = slide[2]
        id = slide[3]
        saveOrAdd = "Save";
    }

    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });

    async function save() {
        event.preventDefault();

        if(saveOrAdd == "Add") {
            if(base64Image == "") {
                alert("Add slider image first")
                return;
            }
            order = sliderList.length;
            const res = await fetch("./saveSlide", {
                method: "POST",
                body: JSON.stringify({
                    text: text,
                    image: base64Image, 
                    order
                }),
                headers: {"content-type": "application/json"}
            });
            let result = await res.json();
            if (result.type != "success") {
                alert(result.message);
                return;
            }else {
                id = result.message
            }
            sliderList = [...sliderList, [text, base64Image, order, id]];
            text = "";
            base64Image = "";
            id = "";
            image = "";
            order = -1;
            saveOrAdd = "Add";
        }else {
            const res = await fetch("./updateSlide", {
                method: "POST",
                body: JSON.stringify({
                    text: text,
                    image: base64Image,
                    id: id
                }),
                headers: {"content-type": "application/json"}
            });
            let result = await res.json();
            if (result.type != "success") alert(result.message);
        }    
    }

    async function deleteSlide() {
        const res = await fetch('./deleteSlide', {
			method: 'POST',
            body: id
        })

        let result = await res.json()
        if (result.type != "success") return;
        thisSlide.style.display = 'none';
    }

    async function loadedImage() {
        base64Image = await toBase64(image[0]);
    }

    async function previousOrder() {
        if(order == 0) return
        let lastId = sliderList[order-1][3]
        const res = await fetch("./previousOrder", {
            method: "POST",
            body: JSON.stringify({
                id: id,
                lastId: lastId,
                order: order
            }),
            headers: {"content-type": "application/json"}
        });
        let result = await res.json();
        if (result.type != "success") {
            alert(result.message);
            return;
        }else {
            sliderList[order][2] -= 1;
            sliderList[order-1][2] += 1;
            order -= 1;
            sortSlider();
            selectedSetting = ""
            setTimeout(function(){selectedSetting=Slider},1)
        }
    }

    async function nextOrder() {
        if(order == sliderList.length-1) return
        let lastId = sliderList[order+1][3]
        const res = await fetch("./nextOrder", {
            method: "POST",
            body: JSON.stringify({
                id: id,
                lastId: lastId,
                order: order
            }),
            headers: {"content-type": "application/json"}
        });
        let result = await res.json();
        if (result.type != "success") {
            alert(result.message);
            return;
        }else {
            sliderList[order][2] += 1;
            sliderList[order+1][2] -= 1;
            order += 1;
            sortSlider();
            selectedSetting = ""
            setTimeout(function(){selectedSetting=Slider},1)
        }
    }
</script>

<div bind:this={thisSlide} class="news">
    <form class="newsContent" on:submit={save} method="post" >
        <input bind:value={text} type="text" name="text" placeholder="Slide Text" required>
        
        <div class='galleryBox'>
            {#if base64Image != ""}
                <img class="img" src={base64Image} alt="Slide photo">
                <input bind:this={fileInput} bind:files={image} on:change={loadedImage} type="file" name="img" accept="image/*" style="display: none;">
                <input class="fileInput" type="button" value="Change image" on:click={()=>fileInput.click()} style="margin-bottom: 5px;"/>
            {:else}
                <p style="margin:0;height:100px;display:flex;flex-direction:column;align-items:center;justify-content:center;">Slide image is not added (preffered resolution: 1920x500)</p>
                <input bind:this={fileInput} bind:files={image} on:change={loadedImage} type="file" name="img" accept="image/*" style="display: none;">
                <input class="fileInput" type="button" value="Add image" on:click={()=>fileInput.click()} style="margin-bottom: 5px;" />
            {/if}
                 
            
        </div>

        <div class="newsContent2" style="justify-content: center;">
            <input type="submit" class="saveButton" value={saveOrAdd} />
            {#if saveOrAdd == "Save"}
                <button on:click={deleteSlide} class="saveButton delete">Delete</button>
            {/if}
        </div>  
        <div class="newsContent2 orderControl">
            {#if saveOrAdd == "Save"}
                <button type="button" on:click={previousOrder}>Previous</button> <p>order: {order+1}</p> <button type="button" on:click={nextOrder}>Next</button>
            {/if}
        </div>  
    </form> 
</div>

<style>
    input {
        margin: 0;
    }
    .news:first-child {
        border-top: none !important;
    }

    .news {
        height: 400px;
        width: 100%;
        border-top: 2px solid #ff4b2b;
    }

    .newsContent {
        height: 100%;
        margin: 20px;
        display: flex;
        flex-direction: column;
        justify-content: left;
    }

    .newsContent2 {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    .orderControl {
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }

    .orderControl button {
        height: 30px;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0px 5px;
        font-size: 0.9em;
        margin: 0;
    }

    .orderControl p {
        height: 40px;
        line-height: 40px;
        margin: 0 10px;
    }

    .img {
       max-height: 100px;
       max-width: 100%;
       margin-top: 5px;
    }

    .fileInput {
        width: 100%;
    }

    .galleryBox {
        height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .saveButton {
        width: 100px;
        height: 43px;
        padding: 10px 0;
        margin-top: 30px;
        color: white;
        background-color: #FF4B2B;
        border: 1px solid #FF4B2B; 
        border-radius: 20px;
        cursor: pointer;
        transition: transform 80ms ease-in;
        display: flex;
        justify-content: center;
        text-align: center;
    }

    .saveButton:active {
        transform: scale(0.95);
    }

    .saveButton:focus {
        outline: none;
        background-color: #FF4B2B;
    }

    .delete {
        margin-left: 10px;
        background-color: #000000;
        border-color:  #000000;
    }

    .delete:focus {
        outline: none;
        background-color: #000000;
    }
    
</style>
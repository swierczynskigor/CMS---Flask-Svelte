<script>
    let title, description, base64Image, fileInput, image;

    title = "";
    description = "";
    base64Image = "";

    loadContent();

    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });

    async function loadContent() {
        const res = await fetch('./getContent', {
			method: 'POST'
        })

        let content = await res.json()
        content = content[0]
        title = content[0];
        description = content[1];
        base64Image = content[2];
    }

    async function save() {
        event.preventDefault();
        if(base64Image == "") {
            alert("Add image first")
            return;
        };

        const res = await fetch("./saveContent", {
            method: "POST",
            body: JSON.stringify({
                title: title,
                description: description, 
                image: base64Image
            }),
            headers: {"content-type": "application/json"}
        });
        let result = await res.json();
        if (result.type != "success") alert(result.message);
    }


    async function loadedImage() {
        base64Image = await toBase64(image[0]);
    }

</script>

<div class="news">
    <form class="newsContent" on:submit={save} method="post" >
        <input bind:value={title} type="text" name="text" placeholder="Content Title" required style="margin-bottom: 20px;">
        <textarea bind:value={description} type="text" name="text" placeholder="Content Description" required></textarea>
        
        {#if base64Image != ""}
            <img class="img" src={base64Image} alt="Slide photo">
            <input bind:this={fileInput} bind:files={image} on:change={loadedImage} type="file" name="img" accept="image/*" style="display: none;">
            <input class="fileInput" type="button" value="Change image" on:click={()=>fileInput.click()} style="margin-bottom: 5px;"/>
        {:else}
            <p>Image is not added (preffered resolution: 500x500)</p>
            <input bind:this={fileInput} bind:files={image} on:change={loadedImage} type="file" name="img" accept="image/*" style="display: none;">
            <input class="fileInput" type="button" value="Add image" on:click={()=>fileInput.click()} style="margin-bottom: 5px;"/>
        {/if}
                 
            
        <input type="submit" class="saveButton" value="Save" />
    </form> 
</div>

<style>
    .news {
        height: 550px;
        width: 100%;
    }

    .newsContent {
        height: 100%;
        margin: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .img {
       width: 150px;
       height: 150px;
       margin-top: 5px;
       margin-bottom: 10px;
    }

    input {
        width: 50%;
        margin: 0;
        margin-bottom: 10px;
    }

    textarea {
        width: 50%;
        resize: none;
        height: 200px;
    }

    p {
        width: 150px;
        height: 150px;
        margin:0;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
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

    
</style>
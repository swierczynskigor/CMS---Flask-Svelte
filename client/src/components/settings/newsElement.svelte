<script>
    export let news;
    export let newsList;
    let title, description, category, images, fileInput, imagesString, saveOrAdd, thisNews, originalTitle, imagesBase64Array, imageIndex;

    title = "";
    description = "";
    category = "";
    images = "";
    saveOrAdd = "Add"
    imagesBase64Array = [];
    imageIndex = 0;

    if(news != undefined) {
        title = news[0];
        description = news[1]
        category = news[2]
        if(news[3] != '') {
            imagesBase64Array = news[3].split('.');      
        }
        saveOrAdd = "Save";
        originalTitle = title;
    }

    const toBase64 = file => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });

    async function save() {
        event.preventDefault();

        imagesString = "";
        if(imagesBase64Array.length > 0) {
            imagesString = imagesBase64Array.join('.');
        }   
        if(saveOrAdd == "Add") {
            const res = await fetch("./saveNews", {
                method: "POST",
                body: JSON.stringify({
                    title: title,
                    description: description,
                    category: category,
                    images: imagesString
                }),
                headers: {"content-type": "application/json"}
            });
            let result = await res.json();
            if (result.type != "success") {
                alert(result.message);
                return;
            }
            newsList = [...newsList, [title, description, category, imagesString]];
            title = "";
            description = "";
            category = "";
            images = "";
            saveOrAdd = "Add";
            imagesBase64Array = [];
            imageIndex = 0;
        }else {
            const res = await fetch("./updateNews", {
                method: "POST",
                body: JSON.stringify({
                    originalTitle: originalTitle,
                    title: title,
                    description: description,
                    category: category,
                    images: imagesString
                }),
                headers: {"content-type": "application/json"}
            });
            let result = await res.json();
            if (result.type != "success") alert(result.message);
        }    
    }

    async function deleteNews() {
        const res = await fetch('./deleteNews', {
			method: 'POST',
            body: title
        })

        let result = await res.json()
        if (result.type != "success") return;
        thisNews.style.display = 'none';
    }

    async function loadedImage() {
        for(const img of images) {
            let imageSrc = await toBase64(img);
            imagesBase64Array.push(imageSrc);
        }

        imagesBase64Array = imagesBase64Array;
        imageIndex = imagesBase64Array.length - 1;
    }

    function deleteImage() {
        if(imagesBase64Array.length == 0) return;   
        imagesBase64Array.splice(imageIndex, 1);
        imagesBase64Array = imagesBase64Array;
    }

    function previousImage() {
        if (imageIndex > 0) {
            imageIndex -= 1; 
        }else {
            imageIndex = imagesBase64Array.length - 1;
        }
    }

    function nextImage() {
        if ((imageIndex + 1) < imagesBase64Array.length) {
            imageIndex += 1;
        }else {
            imageIndex = 0;
        }
    }
</script>

<div bind:this={thisNews} class="news">
    <form class="newsContent" on:submit={save} method="post" >
        <div class="newsContent2">
            <div class="newsValues">
                <input bind:value={title} type="text" name="title" placeholder="News Title" required>
                <textarea bind:value={description} cols="30" rows="10" placeholder="News Description" required></textarea>
            </div>
            <div class="newsValues">
                <input bind:value={category} type="text" placeholder="News Category" required>

                <div class='galleryBox'>
                    {#if imagesBase64Array.length > 0}
                        gallery:
                        <img class="img" src={imagesBase64Array[imageIndex]} alt="News photo">
                    {:else}
                        gallery is empty
                    {/if}
                    <div style="display: flex; width: 100%; margin-top: 5px;">
                        <button type="button" on:click={previousImage} >Previous</button>
                        <button type="button" on:click={nextImage} style="margin-left: 5px">Next</button>
                    </div>                 
                    <button type="button" on:click={deleteImage}>Delete selected from gallery</button>
                    <input bind:this={fileInput} bind:files={images} on:change={loadedImage} type="file" name="img" accept="image/*" multiple style="display: none;">
                    <input class="fileInput" type="button" value="Add image to gallery" on:click={()=>fileInput.click()} style="margin-bottom: 5px;" />
                </div>
            </div>
        </div>
        
        <div class="newsContent2" style="justify-content: center;">
            <input type="submit" class="saveButton" value={saveOrAdd} />
            {#if saveOrAdd == "Save"}
                <button on:click={deleteNews} class="saveButton delete">Delete</button>
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

    .newsValues {
        width: 40%;
        height: 290px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    textarea {
        resize: none;
        margin: 0;
    }

    .img {
       max-height: 90px;
       max-width: 100%;
       margin-top: 5px;
    }

    .fileInput {
        width: 100%;
    }

    .galleryBox {
        display: flex;
        flex-direction: column;
        align-items: center;
    }


    .galleryBox button {
        width: 100%;
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
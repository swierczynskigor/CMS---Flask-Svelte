<script>
    import FooterElement from "./footerElement.svelte";
    
    let footerList = [];   

    loadFooter();

    async function loadFooter() {
        const res = await fetch('./getFooter', {
			method: 'POST'
        })

        footerList = await res.json()    
    }
</script>

<div class="footerContainer">
    <div class="footerList">
        <p>Footer Items:</p>
        {#each footerList as footer}
            <FooterElement {footer} bind:footerList={footerList}/>
	    {/each}
        <FooterElement footer={['','']} bind:footerList={footerList} />
    </div>
</div>

<style>
    .footerContainer {
        position: absolute;
        top: 0;
        width: 100%;
        height: 100%;
        
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-evenly;
    }

    .footerList {
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
    }
</style>
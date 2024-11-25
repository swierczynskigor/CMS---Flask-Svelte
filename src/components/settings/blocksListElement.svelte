<script>
	export let item;
	export let index;
    export let changeActive;
</script>

<h1>
	<div>{index+1}</div>
    <span style="{item.active == 'false' ? 'color: rgba(0, 0, 0, 0.4);' : undefined}">{item.name}</span>
    {#if item.locked == 'true'}
        <i class="fa fa-solid fa-lock"></i>
    {:else}
        {#if item.active == 'true'}
            <i on:click={changeActive(index)} class="fa fa-solid fa-eye"></i>
        {:else}
            <i on:click={changeActive(index)} class="fa fa-solid fa-eye-slash"></i>
        {/if}
        
    {/if}
</h1>

<style>
    h1 {
        display: flex;
        align-items: center;
    }
	div {
		width: 30px;
        height: 30px; 
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: .5em;
        color: white;
		background-color: #FF4B2B;
		border-radius: 50%;
        margin-right: 10px;
	}
    span {
        text-transform: capitalize;
    }
    i {
        margin-top: 8px;
        margin-left: 5px;
        font-size: 0.75em;
    }
</style>


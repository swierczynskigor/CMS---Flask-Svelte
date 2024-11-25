<script>
    import NewsElement from './newsElement.svelte';
    let newsList = [];
    let newsListLoaded;
    loadNews();

    async function loadNews() {
        const res = await fetch('./getNews', {
			method: 'POST'
        })

        newsList = await res.json()
        newsListLoaded = [];
    }
</script>

<div class='newsContainer'>
    {#each newsList as news}
        <NewsElement {news} bind:newsList={newsList}/>
	{/each}
    {#if newsListLoaded}
        <NewsElement bind:newsList={newsList} />
    {/if}
</div>

<style>
    .newsContainer {
        position: absolute;
        top: 0;

        width: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;
    }

</style>
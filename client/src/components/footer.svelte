<script>
    export let copyrights;
    export let footerItems;
</script>

<footer>
    <div class="contatiner">
        <div class="links">
            {#each footerItems as item}
                <a href={item.link}>{item.text}</a>
            {/each}
        </div>
        <div class="copyrights">©{copyrights}</div>
    </div>
</footer>

<style>
    footer {
        margin-top: 50px;
        width: 100%;
        display: flex;
        justify-content: center;
    }
    .contatiner {
        width: 80%;
        border-top: 1px solid gray;
    }
    .links {
        height: 100px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
    }
    .links a {
        margin: 5px;
    }
    .copyrights {
        text-align: center;
        border-top: 1px solid lightgray;
    }
</style>

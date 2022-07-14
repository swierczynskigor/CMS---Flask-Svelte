<script>
    import Carousel from "svelte-carousel";

    let carousel; // for calling methods of the carousel instance
    export let data;

    const delay = data.sliderDuration;
</script>

{#if data.sliderItems.length > 0}
    <div class="sliderMain" style="color:{data.sliderColor};">
        <Carousel
            bind:this={carousel}
            let:showPrevPage
            let:showNextPage
            autoplay={true}
            autoplayDuration={delay}
            duration={800}
        >
            <div
                slot="prev"
                on:click={showPrevPage}
                class="custom-arrow custom-arrow-prev"
            >
                <i class="fa fa-angle-left" style="font-size:60px" />
            </div>
            {#each data.sliderItems as item}
                <div
                    class="slider"
                    style="background-image: url({item.sliderPhoto});"
                >
                    <p>{item.sliderText}</p>
                </div>
            {/each}
            <div
                slot="next"
                on:click={showNextPage}
                class="custom-arrow custom-arrow-next"
            >
                <i class="fa fa-angle-right" style="font-size:60px" />
            </div>
        </Carousel>
    </div>
{/if}

<style>
    .sliderMain {
        height: 500px;
        -webkit-touch-callout: none; /* iOS Safari */
        -webkit-user-select: none; /* Safari */
        -khtml-user-select: none; /* Konqueror HTML */
        -moz-user-select: none; /* Old versions of Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
        user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
        margin-bottom: 30px;
    }
    .slider {
        width: 100%;
        height: 500px;
        background-color: grey;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all ease 1s;
        background-color: rgba(0, 0, 0, 0.749);
        background-size: cover;
        background-position: center;
    }
    .slider p {
        font-size: 100px;
        margin: 0;
        padding: 0;
    }
    .custom-arrow {
        width: 40px;
        position: absolute;
        top: 0;
        bottom: 0;
        z-index: 1;
        transition: opacity 150ms ease;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
    }
    .custom-arrow-next {
        right: 0;
    }
</style>

<script>
    import SliderElement from "./sliderElement.svelte";
    export let selectedSetting;
    let sliderList = [];
    let sliderListLoaded, sliderDuration;

    loadSlider();
    getSliderDuration();

    async function loadSlider() {
        const res = await fetch("./getSlider", {
            method: "POST",
        });

        sliderList = await res.json();
        sortSlider();
        sliderListLoaded = [];
    }

    function sortSlider() {
        sliderList.sort((a, b) => a[2] - b[2]);
        let lastIndex = 0;
        for (let slide of sliderList) {
            if (slide[2] > lastIndex) slide[2] = lastIndex;
            slide[2] = parseInt(slide[2]);
            lastIndex += 1;
        }
        sliderList = sliderList;
    }

    async function getSliderDuration() {
        const res = await fetch("./getSliderDuration", {
            method: "POST",
        });

        sliderDuration = await res.text();
    }

    async function changeSliderDuration() {
        const res = await fetch("./changeSliderDuration", {
            method: "POST",
            body: sliderDuration,
            headers: { "content-type": "application/json" },
        });
        let result = await res.json();
        if (result.type != "success") alert(result.message);
    }
</script>

<div class="sliderContainer">
    <div class="durationContainer">
        <label for="sliderDuration">Duration: {sliderDuration}ms</label>
        <input
            type="range"
            name="duration"
            id="sliderDuration"
            bind:value={sliderDuration}
            on:change={changeSliderDuration}
            min="1000"
            max="20000"
            step="100"
        />
    </div>

    {#each sliderList as slide}
        <SliderElement
            {slide}
            bind:selectedSetting
            sortSlider={() => sortSlider()}
            bind:sliderList
        />
    {/each}
    {#if sliderListLoaded}
        <SliderElement bind:sliderList />
    {/if}
</div>

<style>
    .sliderContainer {
        position: absolute;
        top: 0;

        width: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .durationContainer {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    #sliderDuration {
        width: 200px;
    }
</style>

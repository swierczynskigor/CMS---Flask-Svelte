<script>
  import Header from "../components/header.svelte";
  import NewsContainer from "../components/NewsContainer.svelte";
  import Footer from "../components/footer.svelte";
  import Slider from "../components/slider.svelte";
  import Progress from "svelte-carousel/src/components/Progress/Progress.svelte";
  import Arrow from "svelte-carousel/src/components/Arrow/Arrow.svelte";
  let logged = false;
  let username = localStorage.getItem("userLoginned");
  if ((username === null || username === "null") === false) logged = true;
  let bgColor;
  let color;
  let font;
  let categories = [];
  let newsIndex;
  let currentCategory = "all";
  let newsToPrint = [];
  async function getData() {
    let res = await fetch("./getData", {
      method: "POST",
    });
    res = await res.json();
    bgColor = res.theme.mainBackground;
    color = res.theme.mainColor;
    font = res.theme.font;
    let newsExists = false;
    res.blocks.forEach((el, i) => {
      if (el.type === "news") {
        newsExists = true;
        newsIndex = i;
      }
    });
    if (newsExists) {
      categories = res.blocks[newsIndex].newsItems.map((el) => {
        return el.newsCategory;
      });
    }
    newsToPrint = res.blocks[newsIndex].newsItems;
    categories = [...new Set(categories)];
    return res;
  }

  const filter = (e) => {
    currentCategory = e.target.value;
  };
  let data = getData();
  const sortNews = (e) => {
    if (e.target.value === "a-z") newsToPrint.sort(sortAZ);
    else if (e.target.value === "z-a") newsToPrint.sort(sortZA);
    let h = [...newsToPrint];
    newsToPrint = [...h];
  };
  function sortAZ(a, b) {
    if (a.newsTitle.toLowerCase() < b.newsTitle.toLowerCase()) {
      return -1;
    }
    if (a.newsTitle.toLowerCase() > b.newsTitle.toLowerCase()) {
      return 1;
    }
    return 0;
  }
  function sortZA(a, b) {
    if (a.newsTitle.toLowerCase() < b.newsTitle.toLowerCase()) {
      return 1;
    }
    if (a.newsTitle.toLowerCase() > b.newsTitle.toLowerCase()) {
      return -1;
    }
    return 0;
  }
</script>

{#await data}
  Loading...
{:then data}
  <script>
  </script>
  <div
    class="main-page-container"
    style="background-color: {bgColor};color:{color}; font-family:{font}"
  >
    {#each data.blocks as item}
      {#if item.type === "navbar"}
        <Header
          navbarType={item.navbarType}
          navbarItems={item.navbarItems}
          background={data.theme.secondBackground}
          color={data.theme.secondColor}
          color2={data.theme.mainColor}
          isLogged={logged}
        />
        <div style="padding: 60px;" />
      {/if}

      {#if item.type === "slider"}
        <Slider data={item} />
      {/if}

      {#if item.type === "news"}
        <div class="additional-to-news">
          <div>
            <select name="" id="filter" on:change={filter}>
              <option value="all">All</option>
              {#each categories as category}
                <option value={category}>{category}</option>
              {/each}
            </select>
            <div>Filter</div>
          </div>
          <div>
            <select name="" id="filter" on:change={sortNews}>
              <option value="a-z">A-Z</option>
              <option value="z-a">Z-A</option>
            </select>
            <div>Filter</div>
          </div>
        </div>
        <div class="newsContainer">
          {#if currentCategory === "all"}
            {#each newsToPrint as news}
              <NewsContainer
                category={news.newsCategory}
                border={data.theme.newsBorder}
                title={news.newsTitle}
                content={news.newsText}
                color={data.theme.mainColor}
                index={news.newsIndex}
              />
            {/each}
          {:else}
            {#each newsToPrint as news}
              {#if currentCategory === news.newsCategory}
                <NewsContainer
                  category={news.newsCategory}
                  border={data.theme.newsBorder}
                  title={news.newsTitle}
                  content={news.newsText}
                  color={data.theme.mainColor}
                  index={news.newsIndex}
                />
              {/if}
            {/each}
          {/if}
        </div>
      {/if}

      {#if item.type === "content"}
        <div class="some-sec-container">
          <div class="someSec">
            <div class="left">
              <div>
                <h2>{item.content.contentTitle}</h2>
              </div>
              <div>
                {item.content.contentDesc}
              </div>
            </div>
            <div class="right">
              <img src={item.content.contentPhoto} alt="" />
            </div>
          </div>
        </div>
      {/if}
      {#if item.type === "footer"}
        <Footer footerItems={item.footerItems} copyrights={item.footerText} />
      {/if}
    {/each}
  </div>
{/await}

<style>
  .additional-to-news {
    display: flex;
    justify-content: space-evenly;
    gap: 20px;
    align-items: center;
  }
  .additional-to-news div {
    display: flex;
    justify-content: center;
    gap: 20px;
    align-items: center;
  }
  .newsContainer {
    width: 100%;
    margin: 0 0 30px 0;
    height: auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    flex-direction: row;
  }
  .someSec {
    width: 80%;
    min-width: 320px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 30px;
  }
  .right img {
    max-width: 500px;
    max-height: 500px;
    width: 100%;
    height: 100%;
    margin: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .some-sec-container {
    width: 100%;
    display: flex;
    justify-content: space-around;
  }
</style>

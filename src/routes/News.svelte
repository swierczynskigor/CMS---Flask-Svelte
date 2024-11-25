<script>
  import Header from "../components/header.svelte";
  import Footer from "../components/footer.svelte";
  import Carousel from "svelte-carousel";
  export let params = {};
  let newsIndex = parseInt(params.id);
  let carousel;
  let logged = false;
  let username = localStorage.getItem("userLoginned");
  if ((username === null || username === "null") === false) logged = true;
  let bgColor;
  let color;
  let news;
  let imagesBase64Array = [];
  let authors = [];
  let comments = [];
  let newComment = "";

  async function getData() {
    let res = await fetch("./getData", {
      method: "POST",
    });
    res = await res.json();
    bgColor = res.theme.mainBackground;
    color = res.theme.mainColor;
    res.blocks.forEach((el) => {
      if (el.type === "news") {
        news = el.newsItems;
      }
    });
    console.log(news[newsIndex]);
    let coms = await fetch("./getComments", {
      method: "POST",
      body: JSON.stringify({
        index: news[newsIndex].newsID,
      }),
      headers: {
        "content-type": "application/json",
      },
    });
    coms = await coms.json();

    authors = coms.authors.split(",,,");
    comments = coms.comments.split(",,,");
    if (
      (authors[0] === " " && comments[0] === " ") ||
      (authors[0] === "" && comments[0] === "")
    ) {
      authors.shift();
      comments.shift();
    }

    console.log(authors, comments);

    if (news[newsIndex].newsPhoto !== "") {
      imagesBase64Array = news[newsIndex].newsPhoto.split(".");
    }
    return res;
  }
  let data = getData();

  async function addComment() {
    console.log(newComment);
    await fetch("./setComments", {
      method: "POST",
      body: JSON.stringify({
        author: localStorage.getItem("userLoginned"),
        content: newComment,
        index: news[newsIndex].newsID,
      }),
      headers: {
        "content-type": "application/json",
      },
    });
    authors = [...authors, localStorage.getItem("userLoginned")];
    comments = [...comments, newComment];

    console.log(authors, comments);
    newComment = "";
  }
</script>

{#await data}
  Loading...
{:then data}
  <div
    class="main-page-container"
    style="background-color: {bgColor};color:{color};"
  >
    <Header
      navbarType={data.blocks[0].navbarType}
      navbarItems={data.blocks[0].navbarItems}
      background={data.theme.secondBackground}
      color={data.theme.secondColor}
      color2={data.theme.mainColor}
      isLogged={logged}
    />
    <div style="padding: 30px;" />

    <div class="container">
      <h5>{news[newsIndex].newsCategory}</h5>
      <h2>{news[newsIndex].newsTitle}</h2>
      <article style="margin-bottom: 30px;">
        <p>
          {news[newsIndex].newsText}
        </p>
      </article>
      <Carousel
        bind:this={carousel}
        let:showPrevPage
        let:showNextPage
        autoplay={false}
        duration={300}
      >
        <div
          slot="prev"
          on:click={showPrevPage}
          class="custom-arrow custom-arrow-prev"
        >
          <i class="fa fa-angle-left" style="font-size:60px" />
        </div>
        {#if imagesBase64Array.length > 0}
          {#each imagesBase64Array as item, i}
            <div class="slider">
              <img class="img" src={imagesBase64Array[i]} alt="" />
            </div>
          {/each}
        {:else}
          <div class="noPictures">
            <p>There are no pictures in gallery</p>
          </div>{/if}
        <div
          slot="next"
          on:click={showNextPage}
          class="custom-arrow custom-arrow-next"
        >
          <i class="fa fa-angle-right" style="font-size:60px" />
        </div>
      </Carousel>
    </div>

    <div class="comments">
      <h3>Komentarze</h3>
      {#if logged}
        <div class="add-comments">
          <input
            type="text"
            bind:value={newComment}
            placeholder="Your comment..."
          />
          <button on:click={addComment}>Post</button>
        </div>
      {/if}
      <div class="comments-list">
        {#each authors as author, i}
          <div
            class="comment"
            style="background-color:{data.theme.secondBackground}; color:{data
              .theme.secondColor};"
          >
            <h4 class="author">{author}</h4>
            <div class="comment-content">{comments[i]}</div>
          </div>
        {/each}
      </div>
    </div>

    <Footer
      footerItems={data.blocks[data.blocks.length - 1].footerItems}
      copyrights={data.blocks[data.blocks.length - 1].footerText}
    />
  </div>
{/await}

<style>
  .comments {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .comments-list {
    min-width: 250px;
    width: 60%;
  }
  .comment {
    padding: 10px 20px;
    margin: 5px;
    border-radius: 20px;
  }
  .comment h4 {
    font-size: 1.2em;
  }
  .author {
    margin: 2px;
  }
  .slider {
    width: 100%;
    height: 500px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all ease 1s;
  }
  .img {
    height: 500px;
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
  .noPictures {
    width: 100%;
    height: 500px;
    background-color: rgb(35, 35, 35);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .noPictures p {
    text-align: center;
  }
  .container {
    width: auto;
    padding: 50px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    font-size: 1.5em;
  }
  article {
    width: 90%;
  }
  article p {
    width: 100%;
    text-align: start;
    margin-bottom: 50px;
  }
</style>

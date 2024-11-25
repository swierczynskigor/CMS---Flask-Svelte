<script>
  export let category;
  export let title;
  export let content;
  export let border;
  export let color;
  export let index;
</script>

<div class="newsContainer" style="border-color: {border};">
  <div class="navContainer" style="background-color: {border};">
    {category}
  </div>
  <div class="newsContent">
    <h3>{title}</h3>
    <p>
      {#if content.length > 30}
        {content.slice(0, 30)}...
      {:else}
        {content}
      {/if}
    </p>
    <button
      class="bt"
      style="border-color: {border};color:{color};"
      onclick="window.location.href='/#/news/{index}'"
    >
      Visit Article
    </button>
  </div>
</div>

<style>
  .newsContainer {
    max-width: 500px;
    min-width: 300px;
    width: 25%;
    display: flex;
    flex-direction: column;
    border-radius: 30px;
    overflow: hidden;
    border: 1px solid #c6e4ff;
    margin: 20px;
  }
  .navContainer {
    padding: 10px;
    background-color: #c6e4ff;
    text-align: center;
  }
  .newsContent {
    padding: 0 10px 10px 10px;
  }
  .bt {
    border-radius: 20px;
    background: none;
    padding: 10px;
    cursor: pointer;
  }
</style>

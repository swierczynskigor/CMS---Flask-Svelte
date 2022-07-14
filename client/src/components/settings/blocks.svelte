<script>
    import SortableList from "svelte-sortable-list";
    import ListElement from "./blocksListElement.svelte";

    loadBlocks();

    let list = [
        // {name: "Navbar", active: 'true', locked: 'true'},
        // {name: "Slider", active: 'true', locked: 'false'},
        // {name: "News", active: 'false', locked: 'false'},
        // {name: "Content", active: 'true', locked: 'false'},
        // {name: "Footer", active: 'true', locked: 'true'}
    ];

    const sortList = (ev) => {
        if (ev.detail[0].name != "navbar" || ev.detail[4].name != "footer")
            return;
        list = ev.detail;
        saveBlocks();
    };

    async function loadBlocks() {
        const res = await fetch("./getBlocks", {
            method: "POST",
        });

        let blocks = await res.json();
        blocks.sort((a, b) => a[2] - b[2]);
        for (const block of blocks) {
            let locked = "false";
            if (block[0] == "navbar" || block[0] == "footer") locked = "true";

            list.push({
                name: block[0],
                active: block[1],
                locked: locked,
            });
            list = list;
        }
    }

    function changeActive(index) {
        if (list[index].active == "true") {
            list[index].active = "false";
        } else {
            list[index].active = "true";
        }
        saveBlocks();
    }

    async function saveBlocks() {
        const res = await fetch("./saveBlocks", {
            method: "POST",
            body: JSON.stringify(list),
            headers: {
                "content-type": "application/json",
            },
        });
        let result = await res.text();
        if (result != "success") console.log("Error while saving blocks");
    }
</script>

<div id="blocksMain">
    <SortableList {list} on:sort={sortList} let:item let:index>
        <ListElement {item} {index} {changeActive} />
    </SortableList>

    <h6>Drag and drop to change order</h6>
</div>

<style>
    #blocksMain {
        display: flex;
        flex-direction: column;
    }

    h6 {
        margin-top: -20px;
        opacity: 0.25;
    }
</style>

<script>
    import userListElement from "./userListElement.svelte";

    export let permissionLevel;
    export let username;
    let userList = [];

    getUserList();
    
    async function getUserList() {
        const res = await fetch('./getUserList', {
			method: 'POST',
			body: JSON.stringify({
				permissionLevel: permissionLevel,
                username: username
            }),
            headers: {
                "content-type": "application/json"
            }
        })

        userList = await res.json()
    }
</script>

<table class="fl-table">
    <thead>
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Password</th>
            <th>Permission Level</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {#each userList as user}
            <svelte:component this={userListElement} user={user} mainPermissionLevel={permissionLevel}/>
        {/each}  
    <tbody>
</table>

<style>
.fl-table {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 5px;
    font-size: 12px;
    font-weight: normal;
    border: none;
    border-collapse: collapse;
    width: 100%;
    max-width: 100%;
    white-space: nowrap;
    background-color: white;
}

.fl-table td, .fl-table th {
    text-align: center;
    padding: 8px;
    font-size: 1.3em;
}

.fl-table td {
    border-right: 1px solid #f8f8f8;
    font-size: 12px;
}

.fl-table td button {
    padding: 5px 10px;
    /* background-color: #4fce43; */
    color: white;
    border: none;
}

.fl-table thead th {
    color: #ffffff;
    background: #ff6d53;
}


.fl-table thead th:nth-child(odd) {
    color: #ffffff;
    background: #474747;
}

.fl-table tr:nth-child(even) {
    background: #F8F8F8;
}


/* Responsive */
/* @media (max-width: 1100px) {
    .fl-table {
        display: block;
    }


    .fl-table thead, .fl-table tbody, .fl-table thead th {
        display: block;
    }
    .fl-table thead th:last-child{
        border-bottom: none;
    }
    .fl-table thead {
        float: left;
    }
    .fl-table tbody {
        width: auto;
        position: relative;
        overflow-x: auto;
    }
    .fl-table td, .fl-table th {
        padding: 20px .625em .625em .625em;
        height: 60px;
        vertical-align: middle;
        box-sizing: border-box;
        overflow-x: hidden;
        overflow-y: auto;
        width: 120px;
        font-size: 1em;
        text-overflow: ellipsis;
    }
    .fl-table thead th {
        text-align: left;
        border-bottom: 1px solid #f7f7f9;
    }
    .fl-table tbody tr {
        display: table-cell;
    }
    .fl-table tbody tr:nth-child(odd) {
        background: none;
    }
    .fl-table tr:nth-child(even) {
        background: transparent;
    }
    .fl-table tr td:nth-child(odd) {
        background: #F8F8F8;
        border-right: 1px solid #E6E4E4;
    }
    .fl-table tr td:nth-child(even) {
        border-right: 1px solid #E6E4E4;
    }
    .fl-table tbody td {
        display: block;
        text-align: center;
    }
} */
</style>

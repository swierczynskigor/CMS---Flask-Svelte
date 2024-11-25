<script>
    import { onMount } from 'svelte';

    export let user;
    export let mainPermissionLevel;
    let originalUsername = user[0];
    let originalEmail = user[1];
    let originalPassword = user[2];
    let originalPermissionLevel = user[3];
    let element_username, element_email, element_password, element_permission, element_firstButton, element_secondButton;
    let firstButton_action = edit;
    let secondButton_action = Delete;

    onMount(async () => {
		element_username = document.getElementById(`userList_username_${originalUsername}`);
        element_email = document.getElementById(`userList_email_${originalUsername}`);
        element_password = document.getElementById(`userList_password_${originalUsername}`);
        element_permission = document.getElementById(`userList_permission_${originalUsername}`);
        element_firstButton = document.getElementById(`userList_firstButton_${originalUsername}`);
        element_secondButton = document.getElementById(`userList_secondButton_${originalUsername}`);
	});

    function edit() {
        element_username.contentEditable = true;
        element_username.style.fontStyle = 'italic';

        element_email.contentEditable = true;
        element_email.style.fontStyle = 'italic';

        element_password.contentEditable = true;
        element_password.style.fontStyle = 'italic';

        if(mainPermissionLevel == 2) {
            element_permission.contentEditable = true;
            element_permission.style.fontStyle = 'italic';
        }
        
        element_firstButton.innerHTML = "Save";
        element_firstButton.style.backgroundColor = "#45a13c";
        firstButton_action = save;

        element_secondButton.innerHTML = "Discard";
        element_secondButton.style.backgroundColor = "#ff5353";
        secondButton_action = discard;
    }

    async function save() {
        element_username.contentEditable = false;
        element_username.style.fontStyle = 'normal';

        element_email.contentEditable = false;
        element_email.style.fontStyle = 'normal';

        element_password.contentEditable = false;
        element_password.style.fontStyle = 'normal';

        element_permission.contentEditable = false;
        element_permission.style.fontStyle = 'normal';
        
        element_firstButton.innerHTML = "Edit";
        element_firstButton.style.backgroundColor = "#43b9ce";
        firstButton_action = edit;

        element_secondButton.innerHTML = "Delete";
        element_secondButton.style.backgroundColor = "#ff5353";
        secondButton_action = Delete;

        if(mainPermissionLevel != 2) {
            element_permission.innerHTML = originalPermissionLevel;
        }

        const res = await fetch('./editUser', {
			method: 'POST',
			body: JSON.stringify({
				originalUsername: originalUsername,
                username: element_username.innerText,
                email: element_email.innerText,
                password: element_password.innerText,
                permissionLevel: element_permission.innerText
            }),
            headers: {
                "content-type": "application/json"
            }
        })

        const result = await res.json()
        if(result['type'] != 'success'){
            alert(result['message'])
            element_username.innerHTML = originalUsername;
            element_email.innerHTML = originalEmail;
            element_password.innerHTML = originalPassword;
            element_permission.innerHTML = originalPermissionLevel;
        }else if(result['type'] == 'success') {
            if(localStorage.getItem("userLoginned") == originalUsername) {
                localStorage.setItem("userLoginned", element_username.innerText);
                document.getElementById('dataUsername').innerHTML = element_username.innerText;
            }
            originalUsername = element_username.innerText;
            originalEmail = element_email.innerText;
            originalPassword = element_password.innerText;
            originalPermissionLevel = element_permission.innerText;    
        }
    }

    function discard() {
        element_username.contentEditable = false;
        element_username.style.fontStyle = 'normal';

        element_email.contentEditable = false;
        element_email.style.fontStyle = 'normal';

        element_password.contentEditable = false;
        element_password.style.fontStyle = 'normal';

        element_permission.contentEditable = false;
        element_permission.style.fontStyle = 'normal';

        element_firstButton.innerHTML = "Edit";
        element_firstButton.style.backgroundColor = "#43b9ce";
        firstButton_action = edit;

        element_secondButton.innerHTML = "Delete";
        element_secondButton.style.backgroundColor = "#ff5353";
        secondButton_action = Delete;

        element_username.innerHTML = originalUsername;
        element_email.innerHTML = originalEmail;
        element_password.innerHTML = originalPassword;
        element_permission.innerHTML = originalPermissionLevel;
    }

    async function Delete() {
        console.log(originalUsername)
        if(originalUsername.toLowerCase() == "admin") {
            alert("You can't delete admin account!")
            return;
        }
        
        const res = await fetch('./deleteUser', {
                method: 'POST',
                body: originalUsername
        })
        const result = await res.text()
        if(result != "success") alert("Error while deleting user")

        document.getElementById(`userList_row_${originalUsername}`).style.display = 'none';
    }


</script>

<tr id="userList_row_{originalUsername}">
    <td id="userList_username_{originalUsername}">{user[0]}</td>
    <td id="userList_email_{originalUsername}">{user[1]}</td>
    <td id="userList_password_{originalUsername}">{user[2]}</td>
    <td id="userList_permission_{originalUsername}">{user[3]}</td>
    <td class="userList_td_button" style='display: flex; justify-content: space-evenly;'>
        <button id='userList_firstButton_{originalUsername}' style="background-color: #43b9ce;" on:click={firstButton_action}>Edit</button>
        <button id='userList_secondButton_{originalUsername}' style="background-color: #ff5353;" on:click={secondButton_action}>Delete</button>
    </td>
</tr>

<style>
    
    td {
        text-align: center;
        padding: 8px;
        margin: auto;
        font-size: 1.2em;
        border-right: 1px solid #f8f8f8;
    }

    .userList_td_button {
        display: flex;
        align-items: center;
        padding: 0;
        height: 100%;
    }
    
    td button {
        width: 50px;
        height: 28px;
        margin: 10px 0;
        color: white !important;
        border: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    tr:nth-child(even){
        background: #F8F8F8;
    }


    /* Responsive */  
    /* @media (max-width: 1100px) {
        td {
            padding: 20px .625em .625em .625em;
            height: 60px;
            vertical-align: middle;
            box-sizing: border-box;
            overflow-x: hidden;
            overflow-y: auto;
            width: 120px;
            font-size: 13px;
            text-overflow: ellipsis;
        }

        .userList_td_button {
            height: 60px;
        }
        
        tr {
            display: table-cell;
        }
        tr:nth-child(odd) {
            background: none;
        }
        tr:nth-child(even) {
            background: transparent;
        }
        tr td:nth-child(odd) {
            background: #F8F8F8;
            border-right: 1px solid #E6E4E4;
        }
        tr td:nth-child(even) {
            border-right: 1px solid #E6E4E4;
        }
        td {
            display: block;
            text-align: center;
        }
    } */
</style>
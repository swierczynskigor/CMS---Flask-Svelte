<script>
    export let type;
    let loginError = '';
    let loginErrorColor = 'red';
    let registerError = '';

    if(localStorage.getItem("userCreated") != null && localStorage.getItem("userCreated") != 'null') {
        localStorage.setItem("userCreated", null);
        loginErrorColor = 'green';
        loginError = 'Account created, try to log in';
        console.log(localStorage.getItem("userCreated"))
    }
    
    
    async function validateLogin() {
        let formEl = document.forms.loginForm;
        let formData = new FormData(formEl);

        const res = await fetch('./login', {
			method: 'POST',
			body: JSON.stringify({
				username: formData.get('username'),
                password: formData.get('password'),
            }),
            headers: {
                "content-type": "application/json"
            }
        })

        const result = await res.text()
        if(result == '1') {
            const res = await fetch('./getProperUsername', {
                method: 'POST',
                body: formData.get('username')
            })
            await res.text().then((username) => {
                localStorage.setItem("userLoginned", username);
                document.location.href = "/#/Settings";
            })
            
        }else {
            loginErrorColor = 'red';
            loginError = 'Invalid username or password';
        }
    }

    async function validateRegister() {
        let formEl = document.forms.registerForm;
        let formData = new FormData(formEl);

        const res = await fetch('./register', {
			method: 'POST',
			body: JSON.stringify({
				username: formData.get('username'),
                password: formData.get('password'),
                email: formData.get('email')
            }),
            headers: {
                "content-type": "application/json"
            }
        })

        const result = await res.text()
        if(result == '1') {
            type = "login";
            loginErrorColor = 'green';
            loginError = 'Account created, try to log in';
            setTimeout( function() { 
                localStorage.setItem("userCreated", true);
                document.location.href = "/#/Login";  
            }, 800);
        }else {
            registerError = 'This username is already taken';
        }
    }

    function changeType() {
        let registerForm = document.getElementById("registerForm");
        
        if(type == "login") {
            type = "register";
            
            registerForm.ontransitionend = () => {
                document.location.href = "/#/Register";
            };
        }else {
            type = "login";

            registerForm.ontransitionend = () => {
                document.location.href = "/#/Login";
            };
        }
        
    }
</script>

<div id="loginBox">
    <a href="/#" id="returnButton">✖</a>
    <form id="loginForm" style={type=="register" ? 'cursor:pointer;' : undefined} on:click={type=="register" ? changeType : undefined} on:submit|preventDefault={type=="login" ? validateLogin : undefined}>
        <h2>Log In</h2>

        <div>
            <input
                type="text"
                placeholder="Username"
                name="username"
                required
            />
        </div>

        <div>
            <input
                type="password"
                placeholder="Password"
                name="password"
                required
            />
        </div>

        <button tabindex="-1" id="loginButton" type="submit">Log In</button>

        <span id="loginError" style="color: {loginErrorColor};">{loginError}</span>
    </form>
    <form id="registerForm" class:activeLogin={type=="login"} style={type=="login" ? 'cursor:pointer; transform: translateY(285px);' : undefined} on:click={type=="login" ? changeType : undefined} on:submit|preventDefault={type=="register" ? validateRegister : undefined}>
        <h2>Sign Up</h2>

        <div>
            <input
                type="text"
                placeholder="Username"
                name="username"
                required
            />
        </div>

        <div>
            <input
                type="text"
                placeholder="Email"
                name="email"
                required
            />
        </div>

        <div>
            <input
                type="password"
                placeholder="Password"
                name="password"
                required
            />
        </div>

        <button tabindex="-1" id="registerButton" type="submit">Sign Up</button>

        <span id="registerError">{registerError}</span>
    </form>
</div>

<style>

    #loginBox {
        position: relative;
        width: 300px;
        height: 400px;
    
        margin: auto;
        margin-top: 100px;
    
        background-color: black;
        border: 2px solid black;
        border-radius: 20px;
        box-shadow: 0 0 20px 4px rgba(0, 0, 0, 0.25);
    
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        overflow: hidden;
    }
    
    #loginForm {
        width: 100%;
        height: 100%;
    
        padding: 20px;
    
        background-color: white;
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;
        align-items: center;
    }
    
    h2 {
        user-select: none;
    }

    #loginForm h2 {
        margin-top: -30px;
        
    }
   
    button {
        padding: 10px 40px;

        border-radius: 20px;
        cursor: pointer;

        transition: transform 80ms ease-in;
    }
    
    button:active {
        transform: scale(0.95);
    }

    button:focus {
        outline: none;
    }

    #loginButton {
        margin-bottom: 50px;
    
        color: white;
        background-color: #FF4B2B;
        border: 1px solid #FF4B2B;     
    }

    #registerButton {
        color: black;
        background-color: white;
        border: 1px solid white;   
    }
    
    #registerForm {
        position: absolute;
        width: 700px;
        height: 345px;
        bottom: 0;
    
        background: linear-gradient(to right, #FF4B2B, #FF416C);
        border-radius: 80% 80% 0 0;
        color: white;
    
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-evenly;
    
        transition: .8s ease-in-out;
    }

     
    #registerForm h2 {
        margin-top: 0px;
    }

    input {
        border-radius: 5px;
        height: 50px;
        line-height: normal;
        color: #282828;
        display: block;
        width: 100%;
        box-sizing: border-box;
        user-select: auto;
        font-size: 16px;
        padding: 0 6px;
        padding-left: 12px;     
    }

    #returnButton {
        position: absolute;
        top: 10px;
        right: 15px;

        color: #FF4B2B;
        font-size: 1.5em;
        text-decoration: none;
        transition: .3s ease-in-out;
    }

    #loginError {
        margin-bottom: 22px;
        margin-top: -70px;
    }

    #registerError {
        color: white;
        margin-top: -10px;
    }
</style>
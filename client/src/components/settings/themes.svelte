<script>
    let selectedMainColor, selectedSecondColor, selectedMainBackground, selectedSecondBackground, selectedNewsBorder, selectedFontFamily, selectedPreset;
    let presets = {
        light: [],
        dark: [], 
        custom: []
    }
    loadPresets();

    async function loadPresets() {
        const res = await fetch('./getPresets', {
			method: 'POST'
        })

        let data = await res.json()
        for(const preset of data) { 
            if(preset[0] == 'dark') {
                if(preset[7] == 1) selectedPreset = preset[0]
                preset.shift();
                presets.dark = preset;      
            }else if(preset[0] == 'light') {
                if(preset[7] == 1) selectedPreset = preset[0]
                preset.shift();
                presets.light = preset;
            }else if(preset[0] == 'custom') {
                if(preset[7] == 1) selectedPreset = preset[0]
                preset.shift();
                presets.custom = preset;
            }else {
                console.log("Error while loading presets");
            }     
        }

        refreshSelected();
    }

    function changePreset() {
        refreshSelected();
        savePreset();
    }

    async function savePreset() {
        const res = await fetch('./savePreset', {
			method: 'POST',
			body: JSON.stringify({
				selectedPreset: selectedPreset,
                preset: [selectedMainColor, selectedSecondColor, selectedMainBackground, selectedSecondBackground, selectedNewsBorder, selectedFontFamily]
            }),
            headers: {
                "content-type": "application/json"
            }
        })

        const result = await res.text()
        if(result != 'success') {
            console.log("Error while saving preset")
            return;
        }

        presets[selectedPreset][0] = selectedMainColor;
        presets[selectedPreset][1] = selectedSecondColor;
        presets[selectedPreset][2] = selectedMainBackground;
        presets[selectedPreset][3] = selectedSecondBackground;
        presets[selectedPreset][4] = selectedNewsBorder;
        presets[selectedPreset][5] = selectedFontFamily;
    }

    function resetPreset() {
        if(selectedPreset == 'light') {
            presets[selectedPreset][0] = '#000000';
            presets[selectedPreset][1] = '#000000';
            presets[selectedPreset][2] = '#ffffff';
            presets[selectedPreset][3] = '#cccccc';
            presets[selectedPreset][4] = '#444444';
            presets[selectedPreset][5] = 'Arial';
        }else if(selectedPreset == 'dark') {
            presets[selectedPreset][0] = '#ffffff';
            presets[selectedPreset][1] = '#ffffff';
            presets[selectedPreset][2] = '#222222';
            presets[selectedPreset][3] = '#333333';
            presets[selectedPreset][4] = '#111111';
            presets[selectedPreset][5] = 'Arial';
        }else {
            presets[selectedPreset][0] = '#000000';
            presets[selectedPreset][1] = '#000000';
            presets[selectedPreset][2] = '#ffffff';
            presets[selectedPreset][3] = '#ffffff';
            presets[selectedPreset][4] = '#cccccc';
            presets[selectedPreset][5] = 'Arial';
        }
           
        refreshSelected();
        savePreset();
    }

    function refreshSelected() {
        selectedMainColor = presets[selectedPreset][0];
        selectedSecondColor = presets[selectedPreset][1];
        selectedMainBackground = presets[selectedPreset][2];
        selectedSecondBackground = presets[selectedPreset][3];
        selectedNewsBorder = presets[selectedPreset][4];
        selectedFontFamily = presets[selectedPreset][5];
    }
    
</script>

<div class="themes_container themes_flexColumn">

    <div class="themes_flexColumn category" style="margin-top: -5px;">
        <h1>Preset:</h1>
        <div class="themes_flexRow" style="justify-content: center;">
            <select bind:value={selectedPreset} on:change={changePreset}>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="custom">Custom</option>
            </select>
            <button on:click={resetPreset}>Reset Preset</button>
        </div>
        
    </div>

    <hr/>

    <div class="themes_flexColumn category">
        <h2>Font Colors:</h2>
        <div class="themes_flexRow">
            <div class="themes_flexColumn element">
                <input bind:value={selectedMainColor} type="color" id="mainColor" >
                <label for="mainColor">Main</label>
            </div>
            
            <div class="themes_flexColumn element">
                <input bind:value={selectedSecondColor} type="color" id="secondaryColor" >
                <label for="secondaryColor">Secondary</label>
            </div>
        </div>
    </div>

    <div class="themes_flexColumn category">
        <h2>Background Colors:</h2>
        <div class="themes_flexRow">
            <div class="themes_flexColumn element">
                <input bind:value={selectedSecondBackground} type="color" id="navbarBackground" >
                <label for="navbarBackground">Navbar</label>
            </div>
            <div class="themes_flexColumn element">
                <input bind:value={selectedNewsBorder} type="color" id="newsBackground" >
                <label for="newsBackground">News Header</label>
            </div>
            <div class="themes_flexColumn element">
                <input bind:value={selectedMainBackground} type="color" id="contentBackground" >
                <label for="contentBackground">Content</label>
            </div>
        </div>
    </div>

    <div class="themes_flexColumn category">
        <h2>Font Family:</h2>
        <select bind:value={selectedFontFamily} style="font-family: '{selectedFontFamily}'">
            <option value="Arial" style="font-family: 'Arial';">Arial</option>
            <option value="Calibri" style="font-family: 'Calibri';">Calibri</option>
            <option value="Roboto" style="font-family: 'Roboto';">Roboto</option>
            <option value="Courier" style="font-family: 'Courier';">Courier</option>
            <option value="Verdana" style="font-family: 'Verdana';">Verdana</option>
            <option value="Comic Sans MS" style="font-family: 'Comic Sans MS';">Comic Sans</option>
        </select>
    </div>

    <button id="saveButton" on:click={savePreset}>SAVE</button>
</div>

<style>
    .themes_flexColumn {
        display: flex;
        flex-direction: column;
        align-items: center;   
    }

    .themes_flexRow {
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
        flex-wrap: wrap;
        width: 100%;
    }

    .themes_container {
        position: absolute;
        top: 0;
        width: 100%;
        align-items: center;
        padding-top: 10px;
    }

    .category {
        width: 60%;
        margin-bottom: 10px;
        margin-top: 20px;
    }

    .element {
        min-width: 60px;
        width: 30%;
    }

    hr {
        border: 1px solid rgb(245, 245, 245);
        width: calc(100% - 2px);
        margin: 5px 0 5px 0;
    }

    h1 {
        margin: 0;
        margin-bottom: 10px;
    }

    h2 {
        margin: 0;
        margin-bottom: 10px;
    }

    input[type=color] {
        width: 50%;
        height: 50px;
        margin: 0;
        padding: 0;
        appearance: none;
        border: none;
        background-color: transparent;
    }

    input[type=color]::-webkit-color-swatch {
        border: 1px solid black;
        border-radius: 12px;
    }

    label {
        text-align: center;
    }

    #saveButton {
        padding: 10px 40px;      
        color: white;
        background-color: #FF4B2B;
        border: 1px solid #FF4B2B; 
        border-radius: 20px;
        cursor: pointer;
        transition: transform 80ms ease-in;
        margin-top: 10px;
    }

    #saveButton:active {
        transform: scale(0.95);
    }

    #saveButton:focus {
        outline: none;
        background-color: #FF4B2B;
    }
</style>
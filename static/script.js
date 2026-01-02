window.onload = function () {

    const bvSlider = document.getElementById("B_V");
    const amagSlider = document.getElementById("Amag");
    const plxSlider = document.getElementById("Plx");

    const bvVal = document.getElementById("bvVal");
    const amagVal = document.getElementById("amagVal");
    const plxVal = document.getElementById("plxVal");


    bvVal.innerText = bvSlider.value;
    amagVal.innerText = amagSlider.value;
    plxVal.innerText = plxSlider.value;

    bvSlider.oninput = () => {
        bvVal.innerText = bvSlider.value;
    };

    amagSlider.oninput = () => {
        amagVal.innerText = amagSlider.value;
    };

    plxSlider.oninput = () => {
        plxVal.innerText = plxSlider.value;
    };

};

function predict() {
    const B_V = Number(document.getElementById("B_V").value);
    const Amag = Number(document.getElementById("Amag").value);
    const Plx = Number(document.getElementById("Plx").value);

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            B_V: B_V,
            Amag: Amag,
            Plx: Plx
        })
    })
        .then(response => response.json())
        .then(result => {
            const isGiant = result.class === 1;
            const starType = isGiant ? "Giant Star" : "Dwarf Star";
            const confidence = (result.probability[result.class] * 100).toFixed(2);

            // Emoji size: Bigger for Giant, smaller for Dwarf
            const starSize = isGiant ? "2rem" : "1.5rem";

            document.getElementById("result").innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: ${starSize}; color: #ffd700; line-height: 1;">★</span>
                    <span>${starType}</span>
                </div>
                <div class="confidence-text">Confidence: ${confidence}%</div>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}



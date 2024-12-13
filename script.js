document.addEventListener("DOMContentLoaded", function () {
    const texts = [
        "Data Science Explorer",
        "Maritime Chief Officer",
        "Curious with logical thinking",
        "Dynamic",
        "Judgemental",
        "Argumentative",
        "& Game Enthusiast"
    ];

    const textElement = document.getElementById("dynamic-text");
    let index = 0;

    function updateText() {
        textElement.textContent = texts[index];
        index = (index + 1) % texts.length;
    }

    setInterval(updateText, 3000); // Change text every 3 seconds
});

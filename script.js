// JavaScript to change the dynamic text
const dynamicText = document.getElementById('dynamic-text');
const texts = [
    "Data Science Explorer",
    "Maritime Chief Officer", 
    "Curious with logical thinking",
    "Dynamic",
    "Judgemental",
    "Argumentative",
    "& Game Enthusiast"
];

let textIndex = 0;

function changeText() {
    dynamicText.textContent = texts[textIndex];
    textIndex = (textIndex + 1) % texts.length;
}

setInterval(changeText, 2000); // Change text every 2 seconds

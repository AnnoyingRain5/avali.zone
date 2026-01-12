let score = 0;
let pb = 0;
let practicetype;
let scoretext;
let pbtext;
let correct;
let incorrect;
let milestone_x10;
let iframe;



window.onload = init;
window.document.addEventListener('Incorrect', handleIncorrect, false)
window.document.addEventListener('Correct', handleCorrect, false)

function init() {
    scoretext = document.getElementById("score")
    pbtext = document.getElementById("score-pb")
    correct = document.getElementById("correct")
    incorrect = document.getElementById("incorrect")
    milestone_x10 = document.getElementById("milestone_x10")
    iframe = document.getElementById("practiceframe");
    
    practicetype = document.getElementById("practicetype").innerText.toLowerCase().replace(/'/g, "");
    pb = Number(document.cookie.split("; ").find((row) => row.startsWith(`score-pb-${practicetype}=`))?.split("=")[1]) || 0;

    iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;

    iframe.onload = function () {
        iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;
    }
}

window.onresize = function () {
    iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;
}

function handleIncorrect() {
    pbtext.style.fontWeight = "unset"
    incorrect.currentTime = 0
    incorrect.play()
    score = 0
    scoretext.innerText = "Score: " + score
}

function handleCorrect() {
    correct.currentTime = 0
    correct.play()
    score += 1
    scoretext.innerText = "Score: " + score
    if (score > pb) {
        pb = score
        pbtext.style.fontWeight = "bold"
        pbtext.innerText = "Best: " + score
        document.cookie = `score-pb-${practicetype}=${pb}; Max-Age=31536000; path=/`
    }
    if (score % 10 === 0) {
        milestone_x10.currentTime = 0
        milestone_x10.play(0)
    }
}
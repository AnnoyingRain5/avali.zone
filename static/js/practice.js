var score = 0


window.onload = init;
window.document.addEventListener('Incorrect', handleIncorrect, false)
window.document.addEventListener('Correct', handleCorrect, false)

function init(){
    scoretext = document.getElementById("score")
    correct = document.getElementById("correct")
    incorrect = document.getElementById("incorrect")
    milestone_x10 = document.getElementById("milestone_x10")
    iframe = document.getElementById("practiceframe");
    
    iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;
    
    iframe.onload = function () {
        iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;
    }
}    

window.onresize = function() {
    iframe.height = iframe.contentWindow.document.body.scrollHeight * 1.2;
}

function handleIncorrect() {
    incorrect.fastSeek(0)
    incorrect.play()
    score = 0
    scoretext.innerText = "Score: " + score
}

function handleCorrect() {
    correct.fastSeek(0)
    correct.play()
    score += 1
    scoretext.innerText = "Score: " + score
    if (score % 10 == 0) {
        milestone_x10.fastSeek(0)
        milestone_x10.play(0)
    }
}

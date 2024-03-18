function checkanswer(answer, correctanswer) {
    if (answer.toLowerCase() == correctanswer.toLowerCase()) {
        //alert("Correct!")
    }
    else {
        alert("Incorrect! The correct answer was " + correctanswer)
    }
    location.reload()
}

function init() {
    var input = document.getElementById("answer")
    // if this is an input subpage
    if (input != null) {
        input.value = ""
        input.focus()
        input.addEventListener("keypress", function (event) {
            // If the user presses the "Enter" key on the keyboard
            if (event.key === "Enter") {
                // Cancel the default action, if needed
                event.preventDefault()
                // Trigger the button element with a click
                document.getElementById("submit").click()
            }
        })
    }
    // if this is a multiple-choice subpage
    else {
        document.addEventListener("keypress", function (event) {
            if (event.key === "1") {
                document.getElementById("answer1").click()
            }
            else if (event.key === "2") {
                document.getElementById("answer2").click()
            }
            else if (event.key === "3") {
                document.getElementById("answer3").click()
            }
        })
    }
}

window.onload = init;

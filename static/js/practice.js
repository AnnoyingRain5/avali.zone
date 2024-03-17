function checkanswer(answer, correctanswer) {
    if (answer == correctanswer) {
        alert("Correct!")
    }
    else {
        alert("Incorrect! The correct answer was " + correctanswer)
    }
    location.reload()
}

function init() {
    var input = document.getElementById("answer")
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

window.onload = init;

function check_answer(answer, correct_answer) {
    if (answer.toLowerCase() === correct_answer.toLowerCase()) {
        let event = new CustomEvent('Correct')
        window.parent.document.dispatchEvent(event)
    } else {
        let event = new CustomEvent('Incorrect')
        window.parent.document.dispatchEvent(event)
        alert("Incorrect! The correct answer was " + correct_answer)
    }
    document.cookie = "lastprompt=" + answer
    location.reload()
}

function init() {
    let input = document.getElementById("answer")
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
            } else if (event.key === "2") {
                document.getElementById("answer2").click()
            } else if (event.key === "3") {
                document.getElementById("answer3").click()
            }
        })
    }
}

window.onload = init;

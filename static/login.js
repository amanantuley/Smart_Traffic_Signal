let switchCtn = document.querySelector("#switch-cnt");
let switchC1 = document.querySelector("#switch-c1");
let switchC2 = document.querySelector("#switch-c2");
let switchCircle = document.querySelectorAll(".switch__circle");
let switchBtn = document.querySelectorAll(".switch-btn");
let aContainer = document.querySelector("#a-container");
let bContainer = document.querySelector("#b-container");

// Function to change form
let changeForm = e => {
    switchCtn.classList.add("is-gx");
    setTimeout(function () {
        switchCtn.classList.remove("is-gx");
    }, 1500);

    switchCtn.classList.toggle("is-txr");
    switchCircle[0].classList.toggle("is-txr");
    switchCircle[1].classList.toggle("is-txr");
    switchC1.classList.toggle("is-hidden");
    switchC2.classList.toggle("is-hidden");
    aContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-z200");
};

// Function to show popup
function showPopup(message) {
    const popup = document.getElementById("popup");
    const popupMessage = document.getElementById("popup-message");
    popupMessage.textContent = message;
    popup.classList.remove("hidden");
}

// Function to hide popup
function hidePopup() {
    const popup = document.getElementById("popup");
    popup.classList.add("hidden");
}

// Event listener for close button
document.getElementById("close-popup").addEventListener("click", hidePopup);

// Main function to add event listeners
let mainF = () => {
    const allButtons = document.querySelectorAll(".switch-btn");
    allButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); 
            changeForm(event); 
        });
    });

    // Modify the signup form submission
    document.getElementById("a-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch("/signup", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showPopup("Account created successfully!");
                this.reset(); 
            } else {
                showPopup(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            showPopup("An error occurred. Please try again.");
        });
    });

    // Modify the login form submission
document.getElementById("b-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    const formData = new FormData(this);

    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            sessionStorage.setItem('loggedIn', 'true'); // Set logged-in flag
            history.pushState(null, null, data.redirect); // Use pushState to add to history
            window.location.href = data.redirect; // Redirect to loading.html
        } else {
            showPopup(data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showPopup("An error occurred. Please try again.");
    });
});

};

// Load main function on window load
window.addEventListener("load", mainF);

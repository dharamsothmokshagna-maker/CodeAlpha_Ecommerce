let cart = [];

let buttons = document.querySelectorAll("button");

buttons.forEach((button) => {
    button.addEventListener("click", () => {

        let product = button.parentElement.querySelector("h3").innerText;

        cart.push(product);

        alert(product + " added to cart!");

        document.querySelector(".cart-count").innerText = cart.length;
    });
});
const container = document.querySelector(".container");
const seats = document.querySelectorAll(".row .seat:not(.sold)");
const count = document.getElementById("count");
const total = document.getElementById("total");
const movieSelect = document.getElementById("movie");
const bookTicketBtn = document.getElementById("book-ticket-btn");
const upiPaymentForm = document.getElementById("upi-payment-form");
const upiForm = document.getElementById("upi-form");
const upiPaymentResult = document.getElementById("upi-payment-result");

populateUI();

let ticketPrice = +movieSelect.value;

// Save selected movie index and price
function setMovieData(movieIndex, moviePrice) {
    localStorage.setItem("selectedMovieIndex", movieIndex);
    localStorage.setItem("selectedMoviePrice", moviePrice);
}

// Update total and count
function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll(".row .seat.selected");

    const seatsIndex = [...selectedSeats].map((seat) => [...seats].indexOf(seat));

    localStorage.setItem("selectedSeats", JSON.stringify(seatsIndex));

    const selectedSeatsCount = selectedSeats.length;

    count.innerText = selectedSeatsCount;
    total.innerText = selectedSeatsCount * ticketPrice;

    setMovieData(movieSelect.selectedIndex, movieSelect.value);
}

// Get data from local storage and populate UI
function populateUI() {
    const selectedSeats = JSON.parse(localStorage.getItem("selectedSeats"));
    const soldSeats = JSON.parse(localStorage.getItem("soldSeats"));

    if (selectedSeats !== null && selectedSeats.length > 0) {
        seats.forEach((seat, index) => {
            if (selectedSeats.indexOf(index) > -1) {
                seat.classList.add("selected");
            }
        });
    }

    if (soldSeats !== null && soldSeats.length > 0) {
        seats.forEach((seat, index) => {
            if (soldSeats.indexOf(index) > -1) {
                seat.classList.add("sold");
            }
        });
    }

    const selectedMovieIndex = localStorage.getItem("selectedMovieIndex");
    if (selectedMovieIndex !== null) {
        movieSelect.selectedIndex = selectedMovieIndex;
    }
}

// Movie select event
movieSelect.addEventListener("change", (e) => {
    ticketPrice = +e.target.value;
    setMovieData(e.target.selectedIndex, e.target.value);
    updateSelectedCount();
});

// Seat click event
container.addEventListener("click", (e) => {
    if (e.target.classList.contains("seat") && !e.target.classList.contains("sold")) {
        e.target.classList.toggle("selected");
        updateSelectedCount();
    }
});

// Book Ticket button event
bookTicketBtn.addEventListener("click", () => {
    const selectedSeats = document.querySelectorAll(".row .seat.selected");

    if (selectedSeats.length > 0) {
        upiPaymentForm.style.display = 'block';
        bookTicketBtn.style.display = 'none';
    } else {
        alert("Please select at least one seat to book.");
    }
});

// Handle UPI payment submission
upiForm.addEventListener("submit", (event) => {
    event.preventDefault();
    
    const upiId = document.getElementById('upi-id').value;
    const screenshot = document.getElementById('transaction-screenshot').files[0];

    if (!upiId) {
        alert('Please enter your UPI ID.');
        return;
    }

    if (!screenshot) {
        alert('Please upload a screenshot of your transaction.');
        return;
    }

    // Simulate successful payment processing
    upiPaymentResult.innerText = 'Payment Successful! Thank you for booking your tickets.';
    
    // Proceed with booking
    bookTickets();
});

// Function to mark selected seats as sold and update UI
function bookTickets() {
    const selectedSeats = document.querySelectorAll(".row .seat.selected");

    selectedSeats.forEach((seat) => {
        seat.classList.remove("selected");
        seat.classList.add("sold");
    });

    const soldSeatsIndex = [...document.querySelectorAll(".row .seat.sold")].map(
        (seat) => [...seats].indexOf(seat)
    );
    localStorage.setItem("soldSeats", JSON.stringify(soldSeatsIndex));

    localStorage.removeItem("selectedSeats");

    // Update UI
    updateSelectedCount();
    alert("Tickets booked successfully!");
    upiPaymentForm.style.display = 'none'; // Hide the payment form
}

// Reset all seats to available
function resetSeats() {
    localStorage.removeItem("soldSeats");
    
    seats.forEach(seat => {
        seat.classList.remove("sold");
    });
    
    localStorage.removeItem("selectedSeats");
    updateSelectedCount();
}

// Reset button event
document.getElementById("reset-btn").addEventListener("click", resetSeats);

// Initial count and total set
updateSelectedCount();

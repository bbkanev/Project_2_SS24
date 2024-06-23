document.addEventListener('DOMContentLoaded', (event) => {
    let timeLeft = testDuration * 60; // convert minutes to seconds
    const timerElement = document.getElementById('timer');

    function updateTimer() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            document.getElementById('testForm').submit();
        }

        timeLeft--;
    }

    const timerInterval = setInterval(updateTimer, 1000);
    updateTimer(); // initial call to set the timer immediately
});

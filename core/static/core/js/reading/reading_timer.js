document.addEventListener("DOMContentLoaded", function () {
  var timerEl = document.getElementById("timer");
  var labelEl = document.getElementById("passage-label");
  var totalSeconds = parseInt(timerEl.dataset.seconds, 10);
  var secondsLeft = totalSeconds;

  function formatTime(s) {
    var m = Math.floor(s / 60);
    var sec = s % 60;
    return String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
  }

  function currentPassage(elapsed) {
    if (elapsed < 15 * 60) return "Passage 1";
    if (elapsed < 35 * 60) return "Passage 2";
    return "Passage 3";
  }

  function tick() {
    var elapsed = totalSeconds - secondsLeft;
    timerEl.textContent = formatTime(Math.max(secondsLeft, 0));
    labelEl.textContent = currentPassage(elapsed);

    if (secondsLeft <= 60) {
      timerEl.classList.add("is-low");
    }
    if (secondsLeft <= 0) {
      clearInterval(intervalId);
      timerEl.textContent = "Time's up";
      return;
    }
    secondsLeft -= 1;
  }

  tick();
  var intervalId = setInterval(tick, 1000);
});
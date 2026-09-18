document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("writing-form");
  var timerEl = document.getElementById("timer");
  var secondsLeft = parseInt(timerEl.dataset.seconds, 10);
  var wordCountEl = document.getElementById("word-count");

  var panels = {
    task1: document.querySelector('.panel[data-panel="task1"]'),
    task2: document.querySelector('.panel[data-panel="task2"]'),
  };
  var tabs = document.querySelectorAll(".task-tab");
  var taskType = window.WRITING_TASK_TYPE;

  // --- Which panel(s) are visible ---
  function showPanel(name) {
    if (taskType === "full") {
      panels.task1.hidden = name !== "task1";
      panels.task2.hidden = name !== "task2";
      tabs.forEach(function (tab) {
        tab.classList.toggle("is-active", tab.dataset.tab === name);
      });
    }
    updateWordCount();
  }

  if (taskType === "full") {
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        showPanel(tab.dataset.tab);
      });
    });
    showPanel("task1");
  } else if (taskType === "task1") {
    panels.task2.hidden = true;
  } else if (taskType === "task2") {
    panels.task1.hidden = true;
  }

  // --- Word count for the currently visible textarea ---
  function activeTextarea() {
    var visiblePanel = panels.task1.hidden ? panels.task2 : panels.task1;
    return visiblePanel.querySelector("textarea");
  }

  function updateWordCount() {
    var ta = activeTextarea();
    var words = ta.value.trim().length ? ta.value.trim().split(/\s+/).length : 0;
    wordCountEl.textContent = words + " words";
  }

  form.querySelectorAll("textarea").forEach(function (ta) {
    ta.addEventListener("input", updateWordCount);
  });
  updateWordCount();

  // --- Timer ---
  function formatTime(s) {
    var m = Math.floor(s / 60);
    var sec = s % 60;
    return String(m).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
  }

  function tick() {
    timerEl.textContent = formatTime(Math.max(secondsLeft, 0));
    if (secondsLeft <= 60) {
      timerEl.classList.add("is-low");
    }
    if (secondsLeft <= 0) {
      clearInterval(intervalId);
      form.submit();
      return;
    }
    secondsLeft -= 1;
  }

  tick();
  var intervalId = setInterval(tick, 1000);

  // Warn before an accidental manual finish, but not on auto-submit.
  document.getElementById("finish-btn").addEventListener("click", function (e) {
    if (secondsLeft > 0) {
      var ok = confirm("Finish now and enter your score? Time left: " + formatTime(secondsLeft));
      if (!ok) e.preventDefault();
    }
  });
});
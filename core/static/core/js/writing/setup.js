document.addEventListener("DOMContentLoaded", function () {
  var radios = document.querySelectorAll('input[name="task_type"]');
  var sections = {
    task1: document.querySelector('.task-fields[data-for="task1"]'),
    task2: document.querySelector('.task-fields[data-for="task2"]'),
  };

  function applyVisibility() {
    var checked = document.querySelector('input[name="task_type"]:checked');
    var value = checked ? checked.value : null;

    sections.task1.hidden = !(value === "task1" || value === "full");
    sections.task2.hidden = !(value === "task2" || value === "full");
  }

  radios.forEach(function (radio) {
    radio.addEventListener("change", applyVisibility);
  });

  // Both hidden until a task type is picked.
  sections.task1.hidden = true;
  sections.task2.hidden = true;
  applyVisibility();
});
// Reusable quiz widget: the Check-yourself section of every lesson.
//
// Usage in a lesson:
//   <div class="quiz" id="quiz"></div>
//   <script src="../assets/quiz.js"></script>
//   <script>
//     renderQuiz(document.getElementById("quiz"), [
//       {
//         q: "Question text?",
//         options: ["Answer one", "Answer two", "Answer three"],  // keep equal-ish length; no formatting clues
//         answer: 1,                                              // index into options
//         explain: "Why answer two is correct."
//       },
//     ]);
//   </script>
//
// Immediate feedback: clicking an option marks it right/wrong, reveals the
// explanation, and locks the question. A running score renders at the bottom.

function renderQuiz(root, questions) {
  root.innerHTML = "";
  const title = document.createElement("h3");
  title.textContent = "Check yourself";
  root.appendChild(title);

  let answered = 0;
  let correct = 0;

  const score = document.createElement("p");
  score.className = "quiz-score";
  score.textContent = "0 / " + questions.length + " answered";

  questions.forEach((item, qi) => {
    const wrap = document.createElement("div");
    wrap.className = "quiz-q";

    const qText = document.createElement("p");
    qText.className = "q-text";
    qText.textContent = (qi + 1) + ". " + item.q;
    wrap.appendChild(qText);

    const explain = document.createElement("div");
    explain.className = "q-explain";
    explain.textContent = item.explain;

    const buttons = [];
    item.options.forEach((opt, oi) => {
      const btn = document.createElement("button");
      btn.className = "q-opt";
      btn.textContent = opt;
      btn.addEventListener("click", () => {
        buttons.forEach((b) => (b.disabled = true));
        if (oi === item.answer) {
          btn.classList.add("correct");
          correct++;
        } else {
          btn.classList.add("wrong");
          buttons[item.answer].classList.add("correct");
        }
        explain.classList.add("shown");
        answered++;
        score.textContent =
          correct + " / " + answered + " correct" +
          (answered < questions.length
            ? " — " + (questions.length - answered) + " to go"
            : answered === questions.length && correct === questions.length
              ? " — perfect."
              : "");
      });
      buttons.push(btn);
      wrap.appendChild(btn);
    });

    wrap.appendChild(explain);
    root.appendChild(wrap);
  });

  root.appendChild(score);
}

const country = document.querySelector('#country');
const options = document.querySelector('#options');
const feedback = document.querySelector('#feedback');
const next = document.querySelector('#next');
let current;
let score = 0;
let count = 0;
let countries = [];

async function startRound() {
  score = count = 0;
  document.querySelector('#score').textContent = '0';
  document.querySelector('#count').textContent = '0 / 16';
  next.hidden = true;
  options.replaceChildren();
  country.textContent = 'Loading…';
  feedback.textContent = '';
  document.querySelector('#prompt').textContent = 'WHAT IS THE CAPITAL OF';
  try {
    const response = await fetch('/api/countries');
    if (!response.ok) throw new Error('Could not load countries');
    countries = (await response.json()).countries;
    // Fisher–Yates shuffle: every country appears exactly once per round.
    for (let i = countries.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [countries[i], countries[j]] = [countries[j], countries[i]];
    }
    await loadQuestion();
  } catch {
    country.textContent = 'Connection problem';
    feedback.textContent = 'Please start a new round to try again.';
  }
}

async function loadQuestion() {
  next.hidden = true;
  feedback.textContent = '';
  options.replaceChildren();
  try {
    const response = await fetch('/api/question?country=' + encodeURIComponent(countries[count]));
    if (!response.ok) throw new Error('Could not load the question');
    current = await response.json();
    country.textContent = current.country;
    for (const choice of current.options) {
      const button = document.createElement('button');
      button.textContent = choice;
      button.addEventListener('click', () => submit(choice));
      options.append(button);
    }
  } catch {
    country.textContent = 'Connection problem';
    feedback.textContent = 'Please refresh the page to try again.';
  }
}

async function submit(choice) {
  for (const button of options.children) button.disabled = true;
  try {
    const response = await fetch('/api/answer', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({country: current.country, choice})
    });
    if (!response.ok) throw new Error('Could not check the answer');
    const result = await response.json();
    count += 1;
    if (result.correct) score += 1;
    document.querySelector('#score').textContent = score;
    document.querySelector('#count').textContent = `${count} / ${countries.length}`;
    for (const button of options.children) {
      if (button.textContent === result.capital) button.classList.add('correct');
      else if (button.textContent === choice) button.classList.add('wrong');
    }
    feedback.textContent = `${result.correct ? 'Correct!' : `The answer is ${result.capital}.`} ${result.fact}`;
    if (count === countries.length) {
      document.querySelector('#prompt').textContent = 'ROUND COMPLETE';
      country.textContent = `You scored ${score} out of ${countries.length}!`;
      feedback.textContent = `${result.correct ? 'Correct!' : `The answer is ${result.capital}.`} ${result.fact} Play again to try for a higher score.`;
    } else {
      next.hidden = false;
    }
  } catch {
    feedback.textContent = 'Could not check your answer. Please try again.';
    for (const button of options.children) button.disabled = false;
  }
}

next.addEventListener('click', loadQuestion);
document.querySelector('#reset').addEventListener('click', startRound);
startRound();

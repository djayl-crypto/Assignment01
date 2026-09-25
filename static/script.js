// 화면 전환과 입력만 JavaScript가 담당합니다. 점수 계산과 유형 판정은 Python에서 실행합니다.
const $ = (id) => document.getElementById(id);
let quiz;
let answers = [];
let current = 0;
let busy = false;
const typeSymbols = { green: '♧', transit: '⇄', active: '⌂', quiet: '☾', culture: '▤' };

function showNotice(message) {
  $('notice').textContent = message;
  $('notice').hidden = !message;
}

function showScreen(screen) {
  for (const name of ['home', 'question', 'result']) {
    $(`${name}-screen`).hidden = name !== screen;
  }
  showNotice('');
  window.scrollTo({ top: 0, behavior: 'instant' });
}

function createTypeCards() {
  for (const [key, type] of Object.entries(quiz.types)) {
    const card = document.createElement('article');
    card.className = 'type-card';
    const icon = document.createElement('span');
    icon.className = 'type-icon';
    icon.style.backgroundColor = type.background;
    icon.style.color = type.color;
    icon.textContent = typeSymbols[key];
    icon.setAttribute('aria-hidden', 'true');
    const number = document.createElement('span');
    number.className = 'type-number';
    number.textContent = type.symbol;
    const heading = document.createElement('h3');
    heading.textContent = type.name;
    const description = document.createElement('p');
    description.textContent = type.short;
    card.append(icon, number, heading, description);
    $('type-cards').append(card);
  }
}

function showQuestion() {
  showScreen('question');
  const question = quiz.questions[current];
  $('question-number').textContent = String(current + 1).padStart(2, '0');
  $('question-title').textContent = question.text;
  $('question-hint').textContent = question.hint;
  $('progress-fill').style.width = `${(current + 1) / quiz.questions.length * 100}%`;
  $('progress').setAttribute('aria-valuenow', current + 1);
  $('question-category').textContent = current < 5 ? 'PART 01 · 내가 원하는 동네' : 'PART 02 · 내가 보내고 싶은 하루';
  $('answers').replaceChildren();
  const legend = document.createElement('legend');
  legend.className = 'sr-only';
  legend.textContent = question.text;
  $('answers').append(legend);
  for (const [index, choice] of quiz.choices.entries()) {
    const label = document.createElement('label');
    label.className = 'answer-option';
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'answer';
    radio.value = choice.value;
    radio.checked = answers[current] === choice.value;
    radio.addEventListener('change', () => {
      answers[current] = choice.value;
      $('next').disabled = false;
    });
    const text = document.createElement('span');
    text.textContent = choice.label;
    const number = document.createElement('span');
    number.className = 'choice-index';
    number.textContent = String(index + 1).padStart(2, '0');
    number.setAttribute('aria-hidden', 'true');
    label.append(radio, text, number);
    $('answers').append(label);
  }
  $('previous').textContent = current === 0 ? '← 처음으로' : '← 이전';
  $('next').innerHTML = current === quiz.questions.length - 1 ? '내 결과 보기 <span aria-hidden="true">↗</span>' : '다음 질문 <span aria-hidden="true">→</span>';
  $('next').disabled = answers[current] === undefined;
  $('question-title').focus({ preventScroll: true });
}

function startTest() {
  if (!quiz || busy) return;
  answers = [];
  current = 0;
  showQuestion();
}

function showResult(result) {
  showScreen('result');
  let tags;
  if (result.mode === 'single') {
    const type = quiz.types[result.best_types[0]];
    $('result-card').style.backgroundColor = type.background;
    $('result-english').textContent = type.english;
    $('result-name').textContent = type.name + ' 도시생활자';
    $('result-headline').textContent = type.title;
    $('result-description').textContent = type.description;
    $('result-tip').textContent = type.tip;
    tags = type.tags;
  } else if (result.mode === 'mixed') {
    $('result-card').style.backgroundColor = '#e8ecd9';
    $('result-english').textContent = 'YOUR OWN CITY MIX';
    $('result-name').textContent = '다채로운 도시생활자';
    $('result-headline').textContent = '하나로 정하기엔,\n좋아하는 일상이 많아요.';
    $('result-description').textContent = `${result.best_types.map(key => quiz.types[key].name).join(' · ')}의 점수가 같아요. 여러 취향을 함께 가진 당신만의 도시생활을 그려보세요.`;
    $('result-tip').textContent = '같은 점수를 받은 요소 중 평소 가장 자주 누리는 것은 무엇인가요? 실제 일주일의 생활 동선을 그려보면 우선순위를 찾는 데 도움이 돼요.';
    tags = result.best_types.map(key => quiz.types[key].name);
  } else {
    $('result-card').style.backgroundColor = '#ececde';
    $('result-english').textContent = 'STILL EXPLORING';
    $('result-name').textContent = '나의 도시 취향 탐색 중';
    $('result-headline').textContent = '아직 발견하지 않은,\n나만의 동네가 있을 거예요.';
    $('result-description').textContent = '이번 질문에서는 뚜렷한 선호가 나타나지 않았어요. 다섯 유형에 꼭 맞출 필요는 없어요. 내가 중요하게 생각하는 다른 조건도 찾아보세요.';
    $('result-tip').textContent = '마음에 들었던 장소를 세 곳 적어보세요. 그곳의 어떤 점이 편안했는지 떠올리면 질문에 담기지 않은 나만의 기준을 발견할 수 있어요.';
    tags = ['취향 탐색', '나만의 기준'];
  }
  $('result-tags').replaceChildren();
  for (const tag of tags) {
    const element = document.createElement('span');
    element.textContent = tag;
    $('result-tags').append(element);
  }
  $('score-bars').replaceChildren();
  for (const [key, type] of Object.entries(quiz.types)) {
    const row = document.createElement('div');
    row.className = 'score-row';
    const label = document.createElement('div');
    label.className = 'score-row-label';
    const name = document.createElement('span');
    name.textContent = type.name;
    const value = document.createElement('span');
    value.textContent = `${result.scores[key]} / ${result.maximums[key]}점 · `;
    const percent = document.createElement('strong');
    percent.textContent = `${result.percentages[key]}%`;
    value.append(percent);
    label.append(name, value);
    const track = document.createElement('div');
    track.className = 'score-track';
    track.setAttribute('aria-hidden', 'true');
    const fill = document.createElement('div');
    fill.style.width = `${result.percentages[key]}%`;
    fill.style.backgroundColor = type.color;
    track.append(fill);
    row.append(label, track);
    $('score-bars').append(row);
  }
  $('result-title').focus({ preventScroll: true });
}

async function goNext() {
  if (busy || answers[current] === undefined) return;
  if (current < quiz.questions.length - 1) {
    current += 1;
    showQuestion();
    return;
  }
  busy = true;
  $('next').disabled = true;
  $('previous').disabled = true;
  $('browse-types').disabled = true;
  $('next').textContent = '취향을 살펴보는 중…';
  showNotice('');
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch('/api/result', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers }), signal: controller.signal,
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '결과를 계산할 수 없어요. 다시 시도해주세요.');
    showResult(result);
  } catch (error) {
    showNotice(error.name === 'AbortError' ? '연결이 지연되고 있어요. 잠시 뒤 다시 시도해주세요.' : '결과를 불러오지 못했어요. 서버 연결을 확인한 뒤 다시 시도해주세요.');
    $('next').textContent = '결과 다시 불러오기 ↗';
    $('next').disabled = false;
  } finally {
    clearTimeout(timeout);
    busy = false;
    $('previous').disabled = false;
    $('browse-types').disabled = false;
  }
}

$('start').addEventListener('click', startTest);
$('restart').addEventListener('click', startTest);
$('next').addEventListener('click', goNext);
$('previous').addEventListener('click', () => {
  if (busy) return;
  if (current === 0) showScreen('home');
  else { current -= 1; showQuestion(); }
});
$('review').addEventListener('click', () => { current = 0; showQuestion(); });
$('browse-types').addEventListener('click', () => {
  if (busy) return;
  showScreen('home');
  $('types').scrollIntoView({ behavior: 'instant', block: 'start' });
});

async function initialize() {
  try {
    const response = await fetch('/api/quiz');
    if (!response.ok) throw new Error('연결 실패');
    quiz = await response.json();
    createTypeCards();
    $('start').innerHTML = '나의 도시 취향 찾기 <span aria-hidden="true">↗</span>';
    $('start').disabled = false;
  } catch (error) {
    showNotice('테스트를 준비하지 못했어요. Python 서버가 실행 중인지 확인하고 새로고침해주세요.');
    $('start').textContent = '새로고침 후 다시 시도해주세요';
  }
}
initialize();

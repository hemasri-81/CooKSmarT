// static/js/main.js
async function postIngredients(ings) {
    const res = await fetch('/api/suggest', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ available_ingredients: ings })
    });
    return res.json();
  }
  
  function renderResults(list) {
    const container = document.getElementById('results');
    container.innerHTML = '';
  
    if (!list || list.length === 0) {
      container.innerHTML = `
        <div class="col-12">
          <div class="alert alert-warning shadow-sm fade-in">
            ⚠️ No suggestions — try different pantry items.
          </div>
        </div>`;
      return;
    }
  
    list.forEach(s => {
      const col = document.createElement('div');
      col.className = 'col-12 fade-in';
  
      // Card
      const card = document.createElement('div');
      card.className = 'card recipe-card p-4 mb-3';
  
      // Header
      const header = document.createElement('div');
      header.className = 'd-flex justify-content-between align-items-start';
      header.innerHTML = `
        <div>
          <h5 class="card-title mb-1 text-gradient">🍴 ${escapeHtml(s.title)}</h5>
          <div class="small text-muted">⭐ Match Score: <strong>${s.score}</strong></div>
        </div>`;
  
      // Body
      const body = document.createElement('div');
      body.className = 'mt-3';
  
      const ingList = document.createElement('div');
      ingList.innerHTML = `<strong>🛒 Ingredients:</strong> ${s.ingredients.map(escapeHtml).join(', ')}`;
  
      const missing = document.createElement('div');
      missing.innerHTML = `<strong>❌ Missing:</strong> ${
        s.missing.length ? s.missing.map(escapeHtml).join(', ') : '<span class="text-success">None 🎉</span>'
      }`;
  
      const subs = document.createElement('div');
      const subsArr = Object.keys(s.substitutions || {}).map(k => 
        `${escapeHtml(k)} → ${escapeHtml(s.substitutions[k])}`
      );
      subs.innerHTML = `<strong>🔄 Substitutions:</strong> ${
        subsArr.length ? subsArr.join(', ') : '—'
      }`;
  
      // Append
      body.appendChild(ingList);
      body.appendChild(missing);
      body.appendChild(subs);
  
      card.appendChild(header);
      card.appendChild(body);
      col.appendChild(card);
      container.appendChild(col);
    });
  }
  
  function escapeHtml(text) {
    return String(text)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('suggest-btn');
    const exampleBtn = document.getElementById('example-btn');
  
    btn.addEventListener('click', async () => {
      const raw = document.getElementById('ingredients-input').value;
      const list = raw.split(',').map(s => s.trim()).filter(Boolean);
      if (list.length === 0) {
        alert('Please type at least one ingredient (comma-separated).');
        return;
      }
      const resp = await postIngredients(list);
      if (resp.error) { alert(resp.error); return; }
      renderResults(resp.suggestions);
    });
  
    exampleBtn.addEventListener('click', async () => {
      const example = ['egg', 'milk', 'flour', 'butter'];
      document.getElementById('ingredients-input').value = example.join(', ');
      const resp = await postIngredients(example);
      renderResults(resp.suggestions);
    });
  });
  
  /* Extra CSS Animations injected dynamically */
  const style = document.createElement('style');
  style.innerHTML = `
    .fade-in {
      animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .recipe-card {
      transition: transform 0.2s, box-shadow 0.2s;
      border-left: 5px solid #7061faff;
    }
    .recipe-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
  `;
  document.head.appendChild(style);
  
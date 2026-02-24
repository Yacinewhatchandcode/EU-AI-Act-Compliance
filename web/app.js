/* ═══════════════════════════════════════════════════════
   EU AI Act PWA — Authenticated App Logic
   Google OAuth + JWT, URL Scanner, Universal Classifier
   ═══════════════════════════════════════════════════════ */

const API = `${location.origin}/api`;

// ── Auth Token Management ──
function getToken() {
    return localStorage.getItem('auth_token') || '';
}

function getUser() {
    try { return JSON.parse(localStorage.getItem('auth_user') || '{}'); } catch { return {}; }
}

function isAuthenticated() {
    return !!getToken() && getToken() !== '';
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    window.location.href = '/login.html';
}

// ── Auth check + Splash Screen ──
window.addEventListener('load', async () => {
    // Check auth — try auto-login if no token
    if (!isAuthenticated()) {
        // Try auto dev-auth first (zero clicks needed)
        try {
            const devRes = await fetch(API + '/auth/dev');
            const devData = await devRes.json();
            if (devData.token) {
                localStorage.setItem('auth_token', devData.token);
                localStorage.setItem('auth_user', JSON.stringify(devData.user));
                window.location.reload();
                return;
            }
        } catch (e) { /* dev auth not available */ }
        window.location.href = '/login.html';
        return;
    }

    // Verify token with server
    try {
        const res = await fetch(API + '/auth/status', {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        const data = await res.json();
        if (!data.authenticated) {
            // Token invalid — try to get a new dev token
            try {
                const devRes = await fetch(API + '/auth/dev');
                const devData = await devRes.json();
                if (devData.token) {
                    localStorage.setItem('auth_token', devData.token);
                    localStorage.setItem('auth_user', JSON.stringify(devData.user));
                    window.location.reload();
                    return;
                }
            } catch (e) { /* dev auth not available */ }
            logout();
            return;
        }
    } catch (e) {
        // Server unreachable, allow offline use
    }

    // Show user info in header
    const user = getUser();
    const userEl = document.getElementById('userInfo');
    if (userEl && user.name) {
        userEl.innerHTML = `<span class="user-name">${user.name.split(' ')[0]}</span>`;
        userEl.style.display = 'flex';
    }

    // Splash dismiss
    setTimeout(() => {
        const s = document.getElementById('splash');
        if (s) { s.classList.add('hide'); setTimeout(() => s.remove(), 600); }
    }, 1600);
});

// ── Service Worker ──
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => { });
}

// ── PWA Install ──
let deferredPrompt;
window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault(); deferredPrompt = e;
    document.getElementById('installBanner').style.display = 'flex';
});
document.getElementById('installBtn')?.addEventListener('click', () => {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(() => {
            document.getElementById('installBanner').style.display = 'none';
            deferredPrompt = null;
            snack('✅ App installée !');
        });
    }
});
document.getElementById('installClose')?.addEventListener('click', () => {
    document.getElementById('installBanner').style.display = 'none';
});

// ── Snackbar ──
let snackTimer;
function snack(msg, duration = 2500) {
    const el = document.getElementById('snackbar');
    if (!el) return;
    clearTimeout(snackTimer);
    el.textContent = msg; el.style.display = 'flex';
    el.classList.remove('out');
    snackTimer = setTimeout(() => {
        el.classList.add('out');
        setTimeout(() => { el.style.display = 'none'; el.classList.remove('out'); }, 300);
    }, duration);
}

// ── Haptic feedback ──
function haptic() {
    if (navigator.vibrate) navigator.vibrate(12);
}

// ── Navigation ──
let currentScreen = 'home';
const screenOrder = ['home', 'classify', 'scan', 'audit', 'report', 'roadmap', 'kb', 'agents', 'wallet', 'leads', 'mica'];

function go(id) {
    if (id === currentScreen && location.hash === '#' + id) return;
    haptic();

    // Transition logic
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const newEl = document.getElementById(`screen-${id}`);
    if (newEl) {
        newEl.classList.add('active');
        const scroll = newEl.querySelector('.screen-scroll');
        if (scroll) scroll.scrollTop = 0;
    }

    // Update state
    currentScreen = id;
    location.hash = id === 'home' ? '' : id;

    // Update Navigation UI
    document.querySelectorAll('.nav-item').forEach(n => {
        n.classList.toggle('active', n.getAttribute('onclick')?.includes(`'${id}'`));
    });

    // Data lazy-loading
    if (id === 'wallet') loadWallet();
    if (id === 'leads') loadLeads();
}

// ── Countdown ──
function updateCD() {
    const deadline = new Date('2026-08-02T00:00:00');
    const now = new Date();
    const diff = Math.max(0, deadline - now);
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    document.getElementById('cdDays').textContent = String(d).padStart(3, '0');
    document.getElementById('cdHours').textContent = String(h).padStart(2, '0');
    document.getElementById('cdMin').textContent = String(m).padStart(2, '0');
    document.getElementById('cdSec').textContent = String(s).padStart(2, '0');
    const start = new Date('2024-08-01');
    const pct = Math.min(100, Math.max(0, ((now - start) / (deadline - start)) * 100));
    document.getElementById('cdFill').style.width = pct.toFixed(1) + '%';
}
setInterval(updateCD, 1000);
updateCD();

// ── API Helper (with auth) ──
async function api(path, body) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + getToken(),
    };
    const opts = body
        ? { method: 'POST', headers, body: JSON.stringify(body) }
        : { headers };
    const res = await fetch(`${API}${path}`, opts);
    if (res.status === 401) {
        logout();
        throw new Error('Session expired');
    }
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

// ════════════════════════════════════════
//  CLASSIFIER
// ════════════════════════════════════════
function fillClassify(text) {
    document.getElementById('classifyInput').value = text;
    haptic();
}

async function doClassify() {
    const desc = document.getElementById('classifyInput').value.trim();
    if (!desc) return snack('⚠️ Décrivez votre système IA');
    const btn = document.getElementById('classifyBtn');
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>Analyse en cours...';

    let result;
    try {
        result = await api('/classify', { description: desc });
    } catch (e) {
        result = classifyLocal(desc);
    }
    btn.disabled = false; btn.textContent = '🔍 Classifier le système';
    showClassifyResult(result);
    haptic();
}

function classifyLocal(desc) {
    const d = desc.toLowerCase();
    const prohibited = [
        { name: 'Social scoring', kw: ['social scoring', 'social credit', 'citizen score'] },
        { name: 'Manipulation subliminale', kw: ['manipulative', 'subliminal', 'deceptive'] },
        { name: 'Émotions au travail', kw: ['emotion recognition', 'workplace emotion'] },
        { name: 'Catégorisation biométrique', kw: ['biometric categorization', 'race detection'] },
        { name: 'Scraping facial', kw: ['facial scraping', 'face database'] },
        { name: 'Police prédictive', kw: ['predictive policing', 'criminal prediction'] },
    ];
    const highRisk = [
        { name: 'Emploi & RH', kw: ['hiring', 'recruitment', 'cv', 'employee', 'worker', 'performance review', 'recrutement'] },
        { name: 'Éducation', kw: ['education', 'school', 'university', 'exam', 'grading', 'student'] },
        { name: 'Crédit & assurance', kw: ['credit', 'insurance', 'loan', 'mortgage'] },
        { name: 'Forces de l\'ordre', kw: ['police', 'law enforcement', 'crime'] },
        { name: 'Infrastructure critique', kw: ['energy', 'transport', 'water supply', 'grid'] },
        { name: 'Migration', kw: ['migration', 'asylum', 'border', 'visa'] },
        { name: 'Biométrie', kw: ['biometric', 'facial recognition'] },
        { name: 'Justice', kw: ['justice', 'court', 'sentencing', 'election'] },
    ];
    for (const p of prohibited) if (p.kw.some(k => d.includes(k))) return { risk_level: 'UNACCEPTABLE (PROHIBITED)', category: p.name, article: 'Article 5', obligations: ['SYSTÈME INTERDIT DANS L\'UE'], penalty: { max_fine_eur: 35000000, max_pct: 7 } };
    for (const h of highRisk) if (h.kw.some(k => d.includes(k))) return { risk_level: 'HIGH', category: h.name, article: 'Article 6(2) + Annexe III', obligations: ['Gestion des risques (Art. 9)', 'Gouvernance des données (Art. 10)', 'Documentation technique (Art. 11)', 'Traçabilité / logging (Art. 12)', 'Transparence (Art. 13)', 'Supervision humaine (Art. 14)', 'Précision & robustesse (Art. 15)', 'Évaluation de conformité (Art. 43)', 'Gestion de la qualité (Art. 17)'] };
    if (['chatbot', 'deepfake', 'synthetic', 'generative', 'bot', 'assistant'].some(k => d.includes(k))) return { risk_level: 'LIMITED', category: 'Obligations de transparence', article: 'Articles 50-52', obligations: ['Divulguer la nature IA', 'Étiqueter le contenu généré'] };
    return { risk_level: 'MINIMAL', category: 'Aucune catégorie spécifique', article: 'N/A', obligations: ['Aucune obligation spécifique', 'Code de conduite volontaire recommandé'] };
}

function showClassifyResult(r) {
    const div = document.getElementById('classifyResult');
    let bClass = 'badge-minimal', bText = '🟢 RISQUE MINIMAL';
    if (r.risk_level.includes('PROHIBITED')) { bClass = 'badge-prohibited'; bText = '🔴 INTERDIT'; }
    else if (r.risk_level === 'HIGH') { bClass = 'badge-high'; bText = '🟠 HAUT RISQUE'; }
    else if (r.risk_level === 'LIMITED') { bClass = 'badge-limited'; bText = '🟡 RISQUE LIMITÉ'; }

    let penaltyHtml = '';
    if (r.penalty) penaltyHtml = `<div class="r-row"><div class="r-label">💰 Sanctions max</div><div class="r-val" style="color:var(--red)">€${(r.penalty.max_fine_eur / 1e6).toFixed(0)}M ou ${r.penalty.max_pct}% CA mondial</div></div>`;

    div.innerHTML = `<div class="result-card">
    <div class="badge ${bClass}">${bText}</div>
    <div class="r-row"><div class="r-label">Catégorie</div><div class="r-val">${r.category}</div></div>
    <div class="r-row"><div class="r-label">Base juridique</div><div class="r-val">${r.article}</div></div>
    ${penaltyHtml}
    <div class="r-row"><div class="r-label">Obligations</div><ul class="r-list">${r.obligations.map(o => `<li>${o}</li>`).join('')}</ul></div>
  </div>`;
    div.scrollIntoView({ behavior: 'smooth' });
}

// ════════════════════════════════════════
//  AUDIT
// ════════════════════════════════════════
const REQS = [
    { id: 'R1', name: 'Gestion des risques', art: 'Art. 9', w: 15 },
    { id: 'R2', name: 'Gouvernance des données', art: 'Art. 10', w: 15 },
    { id: 'R3', name: 'Documentation technique', art: 'Art. 11', w: 12 },
    { id: 'R4', name: 'Traçabilité (Logging)', art: 'Art. 12', w: 10 },
    { id: 'R5', name: 'Transparence', art: 'Art. 13', w: 10 },
    { id: 'R6', name: 'Supervision humaine', art: 'Art. 14', w: 15 },
    { id: 'R7', name: 'Précision & cybersécurité', art: 'Art. 15', w: 13 },
    { id: 'R8', name: 'Évaluation de conformité', art: 'Art. 43', w: 5 },
    { id: 'R9', name: 'Gestion de la qualité', art: 'Art. 17', w: 5 },
];

function buildAuditList() {
    const el = document.getElementById('auditList');
    el.innerHTML = REQS.map(r => `
    <div class="audit-row">
      <div style="flex:1"><div class="audit-name">${r.name}</div><div class="audit-art">${r.art} · Poids ${r.w}%</div></div>
      <select class="audit-sel" id="aud-${r.id}">
        <option value="">—</option>
        <option value="COMPLIANT">✅ Conforme</option>
        <option value="PARTIAL">⚠️ Partiel</option>
        <option value="NON_COMPLIANT">❌ Non conforme</option>
      </select>
    </div>
  `).join('');
}
buildAuditList();

async function doAudit() {
    const name = document.getElementById('auditName').value.trim() || 'Système IA';
    const answers = {};
    REQS.forEach(r => { const v = document.getElementById(`aud-${r.id}`).value; if (v) answers[r.id] = v; });

    let result;
    try {
        result = await api('/audit', { system_name: name, answers });
    } catch (e) {
        result = auditLocal(name, answers);
    }
    showAuditResult(result);
    haptic();
}

function auditLocal(name, answers) {
    let total = 0, max = 0;
    const reqs = REQS.map(r => {
        const st = answers[r.id] || 'NOT_ASSESSED';
        let sc = st === 'COMPLIANT' ? r.w : st === 'PARTIAL' ? r.w * 0.5 : 0;
        total += sc; max += r.w;
        return { ...r, status: st, score: sc };
    });
    const pct = max > 0 ? Math.round((total / max) * 100) : 0;
    return {
        system_name: name, compliance_pct: pct, requirements: reqs,
        rating: pct >= 90 ? '✅ EXCELLENT' : pct >= 70 ? '⚠️ BON' : pct >= 50 ? '🟡 À AMÉLIORER' : '❌ NON CONFORME'
    };
}

function showAuditResult(r) {
    const div = document.getElementById('auditResult');
    let col = 'var(--red)';
    if (r.compliance_pct >= 90) col = 'var(--green)';
    else if (r.compliance_pct >= 70) col = 'var(--yellow)';
    else if (r.compliance_pct >= 50) col = 'var(--orange)';

    const rows = (r.requirements || []).map(q => {
        const ic = { COMPLIANT: '✅', PARTIAL: '⚠️', NON_COMPLIANT: '❌', NOT_ASSESSED: '⬜' }[q.status] || '⬜';
        return `<div class="audit-row"><div class="audit-name">${ic} ${q.name || q.id}</div><div style="font-size:0.75rem;color:var(--t3)">${q.score || 0}/${q.w || q.weight}</div></div>`;
    }).join('');

    div.innerHTML = `<div class="result-card">
    <div class="score-wrap">
      <div class="score-ring" style="border-color:${col};--pct:${r.compliance_pct}"><span class="score-num" style="color:${col}">${r.compliance_pct}%</span></div>
      <div class="score-rating">${r.rating}</div>
    </div>
    ${rows}
  </div>`;
    div.scrollIntoView({ behavior: 'smooth' });
}

// ════════════════════════════════════════
//  REPORT
// ════════════════════════════════════════
let lastReport = '';

async function doReport() {
    const name = document.getElementById('reportName').value.trim() || 'Système IA';
    const desc = document.getElementById('reportDesc').value.trim() || name;
    const div = document.getElementById('reportResult');
    div.innerHTML = '<div class="result-card" style="text-align:center"><span class="spinner"></span> Génération du rapport...</div>';

    let report;
    try {
        const data = await api('/report', { system_name: name, description: desc });
        report = data.report;
    } catch (e) {
        report = `# 🇪🇺 Rapport de Conformité EU AI Act\n## ${name}\n\n**Date**: ${new Date().toLocaleDateString('fr-FR')}\n**Description**: ${desc}\n\n> Connectez le serveur API pour le rapport complet.\n> python eu_ai_act_server.py`;
    }
    lastReport = report;

    div.innerHTML = `<div class="result-card">
    <div class="report-text">${report}</div>
    <button class="btn-secondary ripple" onclick="copyReport()">📋 Copier le rapport</button>
    <button class="btn-secondary ripple" onclick="shareReport()">📤 Partager</button>
    <button class="btn-secondary ripple" onclick="downloadReport()">💾 Télécharger (.txt)</button>
  </div>`;
    div.scrollIntoView({ behavior: 'smooth' });
    haptic();
}

function copyReport() {
    navigator.clipboard.writeText(lastReport).then(() => snack('✅ Rapport copié !'));
}

function downloadReport() {
    const blob = new Blob([lastReport], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'rapport_eu_ai_act.txt';
    a.click();
    snack('💾 Téléchargement lancé');
}

async function shareReport() {
    if (navigator.share && lastReport) {
        try {
            await navigator.share({ title: 'EU AI Act - Rapport', text: lastReport });
        } catch (e) { /* cancelled */ }
    } else {
        copyReport();
    }
}

// ════════════════════════════════════════
//  ROADMAP
// ════════════════════════════════════════
async function doRoadmap() {
    const name = document.getElementById('roadmapName').value.trim() || 'Système IA';
    const div = document.getElementById('roadmapResult');

    const phases = [
        { name: 'Inventaire & Classification', dur: 14, tasks: ['Recenser tous les systèmes IA', 'Classifier par niveau de risque', 'Identifier rôle fournisseur/déployeur', 'Documenter finalité de chaque système'] },
        { name: 'Évaluation des écarts', dur: 30, tasks: ['Auditer documentation (Art. 11)', 'Évaluer gouvernance données (Art. 10)', 'Examiner supervision humaine (Art. 14)', 'Vérifier journalisation (Art. 12)', 'Évaluer cybersécurité (Art. 15)'] },
        { name: 'Gestion des risques', dur: 45, tasks: ['Concevoir cadre Art. 9', 'Documenter tous les risques', 'Implémenter mesures d\'atténuation', 'Mettre en place suivi continu'] },
        { name: 'Implémentation technique', dur: 60, tasks: ['Système de journalisation auto', 'Interfaces supervision humaine', 'Suivi précision/robustesse', 'Contrôles cybersécurité', 'Mécanismes de transparence'] },
        { name: 'Documentation & Évaluation', dur: 30, tasks: ['Documentation technique finale', 'Déclaration UE de Conformité', 'Évaluation de conformité', 'Enregistrement base UE', 'Marquage CE'] },
        { name: 'Surveillance post-marché', dur: 0, tasks: ['Suivi des performances', 'Signalement incidents', 'Revues régulières', 'Formation continue'] },
    ];

    let dt = new Date();
    div.innerHTML = `<div class="result-card">${phases.map((p, i) => {
        const start = dt.toLocaleDateString('fr-FR');
        let endStr = 'En continu';
        if (p.dur > 0) { dt = new Date(dt.getTime() + p.dur * 86400000); endStr = dt.toLocaleDateString('fr-FR'); }
        return `<div class="rm-phase" style="animation-delay:${i * 0.08}s">
      <div class="rm-num">Phase ${i + 1}</div>
      <div class="rm-title">${p.name}</div>
      <div class="rm-dates">${start} → ${endStr}${p.dur ? ` (${p.dur}j)` : ''}</div>
      <ul class="rm-tasks">${p.tasks.map(t => `<li>${t}</li>`).join('')}</ul>
    </div>`;
    }).join('')}</div>`;
    div.scrollIntoView({ behavior: 'smooth' });
    haptic();
}

// ════════════════════════════════════════
//  KNOWLEDGE BASE
// ════════════════════════════════════════
async function loadKB() {
    let data;
    try {
        data = await api('/knowledge');
    } catch (e) {
        data = defaultKB();
    }
    renderKB(data);
}

function defaultKB() {
    return {
        prohibited: [
            { id: 'P1', article: 'Art. 5(1)(a)', name: 'IA manipulatrice / subliminale', description: 'Techniques subliminales modifiant le comportement' },
            { id: 'P2', article: 'Art. 5(1)(b)', name: 'Exploitation des vulnérabilités', description: 'Ciblage âge, handicap, situation sociale' },
            { id: 'P3', article: 'Art. 5(1)(c)', name: 'Scoring social', description: 'Évaluation basée sur le comportement social' },
            { id: 'P4', article: 'Art. 5(1)(d)', name: 'Prédiction criminelle', description: 'Profilage pour prédire le risque criminel' },
            { id: 'P5', article: 'Art. 5(1)(e)', name: 'Scraping facial', description: 'Bases de données faciales par scraping' },
            { id: 'P6', article: 'Art. 5(1)(f)', name: 'Émotions au travail / école', description: 'Reconnaissance d\'émotions en milieu professionnel' },
            { id: 'P7', article: 'Art. 5(1)(g)', name: 'Catégorisation biométrique', description: 'Inférence race, religion par biométrie' },
            { id: 'P8', article: 'Art. 5(1)(h)', name: 'Identification biométrique temps réel', description: 'ID biométrique en espace public' },
        ],
        high_risk: [
            { id: 'HR1', article: 'Art. 6(2)', annex: 'Annexe III §1', name: 'Biométrie', description: 'Identification à distance, émotions' },
            { id: 'HR2', article: 'Art. 6(2)', annex: 'Annexe III §2', name: 'Infrastructure critique', description: 'Trafic routier, eau, gaz, électricité' },
            { id: 'HR3', article: 'Art. 6(2)', annex: 'Annexe III §3', name: 'Éducation', description: 'Accès éducation, évaluation, examens' },
            { id: 'HR4', article: 'Art. 6(2)', annex: 'Annexe III §4', name: 'Emploi', description: 'Tri CV, embauche, évaluation' },
            { id: 'HR5', article: 'Art. 6(2)', annex: 'Annexe III §5', name: 'Services essentiels', description: 'Crédit, assurance, prestations' },
            { id: 'HR6', article: 'Art. 6(2)', annex: 'Annexe III §6', name: 'Forces de l\'ordre', description: 'Preuves, profilage, analyse' },
            { id: 'HR7', article: 'Art. 6(2)', annex: 'Annexe III §7', name: 'Migration & frontières', description: 'Asile, visas, surveillance' },
            { id: 'HR8', article: 'Art. 6(2)', annex: 'Annexe III §8', name: 'Justice & démocratie', description: 'Juridique, sentencing, élections' },
        ],
        requirements: REQS
    };
}

function renderKB(data) {
    document.getElementById('kbP').innerHTML = (data.prohibited || []).map(p => `
    <div class="kb-item"><div class="kb-name">${p.name}</div><div class="kb-desc">${p.description}</div><div class="kb-meta"><span class="kb-tag">${p.article}</span><span class="kb-tag">${p.id}</span></div></div>
  `).join('');
    document.getElementById('kbH').innerHTML = (data.high_risk || []).map(h => `
    <div class="kb-item"><div class="kb-name">${h.name}</div><div class="kb-desc">${h.description}</div><div class="kb-meta"><span class="kb-tag">${h.article}</span><span class="kb-tag">${h.annex || ''}</span></div></div>
  `).join('');
    document.getElementById('kbR').innerHTML = (data.requirements || []).map(r => `
    <div class="kb-item"><div class="kb-name">${r.name}</div><div class="kb-meta"><span class="kb-tag">${r.art || r.article}</span><span class="kb-tag">Poids: ${r.w || r.weight}%</span></div></div>
  `).join('');
}

async function doSearch() {
    const q = document.getElementById('kbSearch').value.trim();
    if (!q) return;
    const resDiv = document.getElementById('kbResults');
    const defDiv = document.getElementById('kbDefault');

    try {
        const data = await api(`/search?q=${encodeURIComponent(q)}`);
        if (data.results.length > 0) {
            defDiv.style.display = 'none';
            resDiv.innerHTML = `<div class="card"><h3>🔍 ${data.count} résultat(s)</h3>
        ${data.results.map(r => `<div class="search-result"><div class="search-type ${r.type}">${r.type === 'prohibited' ? '🔴 INTERDIT' : r.type === 'high_risk' ? '🟠 HAUT RISQUE' : '📋 EXIGENCE'}</div><div class="kb-name">${r.data.name}</div><div class="kb-desc">${r.data.description || ''}</div></div>`).join('')}
        <button class="btn-secondary" onclick="clearSearch()">← Retour</button>
      </div>`;
        } else {
            resDiv.innerHTML = `<div class="card"><p style="color:var(--t3)">Aucun résultat pour "${q}"</p><button class="btn-secondary" onclick="clearSearch()">← Retour</button></div>`;
        }
    } catch (e) {
        resDiv.innerHTML = `<div class="card"><p style="color:var(--t3)">Connectez le serveur API pour la recherche.</p></div>`;
    }
}

function clearSearch() {
    document.getElementById('kbResults').innerHTML = '';
    document.getElementById('kbDefault').style.display = 'block';
    document.getElementById('kbSearch').value = '';
}

// ── Hash Navigation ──
function handleHash() {
    const hash = location.hash.replace('#', '');
    if (hash && document.getElementById(`screen-${hash}`)) {
        go(hash);
    }
}
window.addEventListener('hashchange', handleHash);
if (location.hash) setTimeout(handleHash, 1700); // after splash

// ── PWA standalone ──
if (window.navigator.standalone === true || window.matchMedia('(display-mode: standalone)').matches) {
    document.body.classList.add('pwa-standalone');
}

// ════════════════════════════════════════
//  URL SCANNER — Test Any Website
// ════════════════════════════════════════
async function doScan() {
    const urlInput = document.getElementById('scanUrl');
    let url = (urlInput?.value || '').trim();
    if (!url) return snack('⚠️ Enter a URL to scan');

    // Auto-add https
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
    }

    const div = document.getElementById('scanResult');
    div.innerHTML = `<div class="result-card" style="text-align:center">
        <span class="spinner"></span>
        <div style="margin-top:12px;color:var(--t2)">Scanning <b>${url}</b>...</div>
        <div style="font-size:11px;color:var(--t3);margin-top:6px">Fetching page content and analyzing AI indicators</div>
    </div>`;
    div.scrollIntoView({ behavior: 'smooth' });

    try {
        const result = await api('/scan', { url });
        showScanResult(result);
    } catch (e) {
        div.innerHTML = `<div class="result-card"><div style="color:var(--red)">❌ ${e.message}</div></div>`;
    }
    haptic();
}

function showScanResult(r) {
    const div = document.getElementById('scanResult');
    if (r.status === 'error') {
        div.innerHTML = `<div class="result-card">
            <div class="badge badge-prohibited">❌ SCAN ERROR</div>
            <div style="color:var(--t2);margin-top:8px">${r.summary}</div>
        </div>`;
        return;
    }

    let bClass = 'badge-minimal', bText = '🟢 NO AI DETECTED';
    if (r.risk_level === 'HIGH') { bClass = 'badge-high'; bText = '🟠 HIGH RISK'; }
    else if (r.risk_level === 'LIMITED') { bClass = 'badge-limited'; bText = '🟡 LIMITED RISK'; }
    else if (r.risk_level === 'MINIMAL') { bClass = 'badge-minimal'; bText = '🟢 MINIMAL RISK'; }

    const indicators = (r.ai_indicators || []).map(i => `
        <div class="scan-indicator">
            <div class="si-name">${i.category}</div>
            <div class="si-meta">
                <span class="kb-tag">${i.article}</span>
                <span class="kb-tag">"${i.keyword}" ×${i.count}</span>
                <span class="kb-tag si-weight">W:${i.weight}</span>
            </div>
        </div>
    `).join('');

    const obligations = (r.obligations || []).map(o => `<li>${o}</li>`).join('');

    div.innerHTML = `<div class="result-card">
        <div class="badge ${bClass}">${bText}</div>
        <div class="r-row"><div class="r-label">🌐 URL</div><div class="r-val" style="word-break:break-all;font-size:12px">${r.url}</div></div>
        <div class="r-row"><div class="r-label">📊 Score</div><div class="r-val">${r.score} / ${r.max_score}</div></div>
        <div class="r-row"><div class="r-label">🔍 Indicators</div><div class="r-val">${r.ai_indicators?.length || 0} found</div></div>
        ${indicators ? `<div style="margin-top:12px">${indicators}</div>` : ''}
        <div class="r-row" style="margin-top:12px"><div class="r-label">📋 Obligations</div><ul class="r-list">${obligations}</ul></div>
        <div style="margin-top:16px;font-size:11px;color:var(--t3)">${r.summary}</div>
    </div>`;
    div.scrollIntoView({ behavior: 'smooth' });
}

function fillScanUrl(url) {
    const input = document.getElementById('scanUrl');
    if (input) input.value = url;
    haptic();
}


// ════════════════════════════════════════
//  WALLET & REVENUE
// ════════════════════════════════════════
async function loadWallet() {
    try {
        const data = await api('/wallet');
        updateWalletUI(data);
    } catch (e) {
        snack('❌ Failed to load wallet');
    }
}

function updateWalletUI(w) {
    const balEl = document.getElementById('walletBalance');
    if (balEl) balEl.textContent = Number(w.balance).toLocaleString('en-US', { minimumFractionDigits: 2 });

    const addrEl = document.getElementById('walletAddress');
    if (addrEl) addrEl.textContent = w.address;

    // Agents status
    const oAgent = document.getElementById('agent-openclaw');
    if (oAgent) {
        oAgent.classList.toggle('working', w.agents.openclaw.status === 'working');
        oAgent.querySelector('.amc-status').textContent = w.agents.openclaw.status.toUpperCase();
    }
    const pAgent = document.getElementById('agent-picoclaw');
    if (pAgent) {
        pAgent.classList.toggle('working', w.agents.picoclaw.status === 'working');
        pAgent.querySelector('.amc-status').textContent = w.agents.picoclaw.status.toUpperCase();
    }

    // History
    const histEl = document.getElementById('walletHistory');
    if (histEl) {
        if (!w.history || w.history.length === 0) {
            histEl.innerHTML = '<div class="h-empty">No transactions yet</div>';
        } else {
            histEl.innerHTML = w.history.map(h => `
                <div class="history-item">
                    <div class="h-left">
                        <b>${h.source}</b>
                        <span>${h.date}</span>
                    </div>
                    <div class="h-right">+${h.amount}</div>
                </div>
            `).join('');
        }
    }
}

async function doGenerateRevenue() {
    haptic();
    const btn = document.getElementById('genBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner"></span> Working...';
    }

    // UI feedback: set agents to working
    document.getElementById('agent-openclaw')?.classList.add('working');
    document.getElementById('agent-picoclaw')?.classList.add('working');

    try {
        const res = await api('/wallet/generate');
        if (res.success) {
            snack('💰 Revenue generated successfully!');
            updateWalletUI(res.wallet);
        }
    } catch (e) {
        snack('❌ Generation failed');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = '⚡ Generate';
        }
    }
}

// Update go function to load wallet
function go(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.style.display = 'none');
    document.getElementById(`screen-${screenId}`).style.display = 'block';
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    const navItem = document.querySelector(`.nav-item[onclick*="'${screenId}'"]`);
    if (navItem) navItem.classList.add('active');

    location.hash = screenId;
    if (screenId === 'wallet') loadWallet();
    if (screenId === 'leads') loadLeads();
}

// ── Initialization ──
document.addEventListener('DOMContentLoaded', () => {
    loadKB();
    loadWallet();
    loadLeads();
    if (location.hash) go(location.hash.replace('#', ''));
});

async function unlockKnowledge() {
    haptic();
    const btn = document.querySelector('.pc-btn');
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Unlocking...';
    }

    try {
        const res = await api('/wallet/spend?amount=50&reason=Unlock%20Premium%20Intel');
        if (res.success) {
            snack('✨ Knowledge Unlocked!');
            updateWalletUI(res.wallet);

            // Show insights
            const insightEl = document.getElementById('premiumInsights');
            if (insightEl) {
                insightEl.style.display = 'block';
                insightEl.innerHTML = `
                    <div class="card premium-content fade-in">
                        <h3>💎 2026 AI Niches Unlocked</h3>
                        <ul>
                            <li><b>Real Estate AI Compliance</b>: High demand in Paris/Lyon. 💸</li>
                            <li><b>Deepfake Detection for Hotels</b>: New safety laws coming June 2026.</li>
                            <li><b>Automated HR Screening</b>: Art. 14 audit needed for startups.</li>
                        </ul>
                        <button class="wc-btn ripple" onclick="go('scan')">Scan Prospect Sites</button>
                    </div>
                `;
                const pCard = document.querySelector('.premium-card');
                if (pCard) pCard.style.display = 'none';
            }
        } else {
            snack('❌ Not enough $PRIME. Earn more by scanning!');
        }
    } catch (e) {
        snack('❌ System error during unlock');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Unlock (50 $PRIME)';
        }
    }
}

async function doMicaScan() {
    const txt = document.getElementById('micaInput').value;
    if (!txt) return snack('Paste some text first');

    const btn = document.getElementById('micaBtn');
    if (btn) {
        btn.disabled = true;
        btn.textContent = '🔍 Analyzing Compliance...';
    }

    try {
        const res = await api(`/mica/scan?q=${encodeURIComponent(txt)}`);
        const out = document.getElementById('micaResults');
        if (out) {
            out.innerHTML = `
                <div class="card result-card fade-in">
                    <div class="res-header">
                        <span class="res-badge ${res.status.toLowerCase()}">${res.status}</span>
                        <h3>${res.classification}</h3>
                    </div>
                    <div class="res-score">MiCA Impact Score: <b>${res.score}</b></div>
                    <div class="res-list">
                        ${res.indicators.map(i => `
                            <div class="res-item">
                                <span><b>${i.category}</b> (${i.article})</span>
                                <span class="res-weight">+${i.weight}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="res-advice">💡 ${res.legal_advice}</div>
                    <button class="btn primary ripple" onclick="snack('Report Saved to Wallet History')">📦 Generate PDF Report</button>
                </div>
            `;
        }
    } catch (e) {
        snack('❌ Analysis failed');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Analyze for MiCA';
        }
    }
}

async function doDownloadReport() {
    haptic();
    const btn = document.getElementById('dlBtn');
    if (btn) btn.disabled = true;

    try {
        const name = document.getElementById('mica-input')?.value || 'Compliance-Project';
        // Trigger a real browser download
        const url = `/api/report/download?name=${encodeURIComponent(name)}`;
        const a = document.createElement('a');
        a.href = url;
        a.download = `EU_AUDIT_${name}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        snack('📑 Downloading Premium Report...');
    } catch (e) {
        snack('❌ Download failed');
    } finally {
        if (btn) btn.disabled = false;
    }
}

async function doCheckout(amount, reason) {
    haptic();
    snack('💳 Connecting to Stripe Secure Checkout...');
    try {
        const res = await api('/pay/create-checkout-session', { amount, reason });
        if (res.id) {
            // In real prod: stripe.redirectToCheckout({ sessionId: res.id });
            // For now: Show the "Real" stripe intent link
            setTimeout(() => {
                window.location.href = res.url;
            }, 1000);
        }
    } catch (e) {
        snack('❌ Payment system unavailable');
    }
}

async function doConnectStripe() {
    haptic();
    snack('🔗 Opening Stripe OAuth Gateway...');
    // The official Stripe MCP authorization URL
    const stripeMcpUrl = 'https://mcp.stripe.com/authorize';
    setTimeout(() => {
        window.open(stripeMcpUrl, '_blank');
        snack('ℹ️ Please complete authorization in the new tab.');
    }, 1500);
}
async function doProspecting() {
    haptic();
    snack('🕷️ PicoClaw is scanning French niches...');
    try {
        const res = await api('/leads/prospect?niche=fintech_paris');
        if (res.success) {
            snack(`✅ Found ${res.new_leads.length} new prospects!`);
            updateWalletUI(res.wallet);
            loadLeads();
            // Mock: after prospecting, if they clicked connect, update status
            const ss = document.getElementById('stripe-status');
            if (ss && ss.innerText === 'Not Connected') {
                // We'll leave it for now until they actually connect
            }
        }
    } catch (e) {
        snack('❌ Prospecting failed');
    }
}

async function loadLeads() {
    try {
        const leads = await api('/leads/list');
        const containers = ['leadList', 'leadsDashboard'];
        containers.forEach(id => {
            const el = document.getElementById(id);
            if (!el) return;
            if (leads.length === 0) {
                el.innerHTML = '<div class="h-empty">No leads found yet</div>';
                return;
            }
            el.innerHTML = leads.map(l => `
                <div class="h-item">
                    <div class="h-info">
                        <div class="h-source"><b>${l.company}</b> <span class="chip">${l.niche}</span></div>
                        <div class="h-date">${l.contact} • Trigger: ${l.trigger}</div>
                    </div>
                    <div class="h-amt" style="color:var(--primary)">+${l.value}€</div>
                </div>
            `).join('');
        });
    } catch (e) {
        console.error('Failed to load leads', e);
    }
}
// ── Web3 / Coinbase Wallet ──
let userAddress = null;

async function connectCoinbaseWallet() {
    haptic();
    const btn = document.getElementById('connectWalletBtn');

    // Check if SDK loaded from CDN
    if (!window.CoinbaseWalletSDK || !window.ethers) {
        snack('❌ Web3 Libraries not ready');
        return;
    }

    try {
        if (btn) {
            btn.disabled = true;
            btn.textContent = '🔄 Linking...';
        }

        const coinbaseWallet = new window.CoinbaseWalletSDK({
            appName: 'PRIME-AI Compliance',
            appLogoUrl: '',
            darkMode: true
        });

        // Default to Base Network
        const baseRpcUrl = 'https://mainnet.base.org';
        const chainId = 8453;

        const ethereum = coinbaseWallet.makeWeb3Provider(baseRpcUrl, chainId);

        // Request accounts
        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        userAddress = accounts[0];

        snack('✅ Wallet Linked to Base!');
        updateWalletConnectionUI();

    } catch (e) {
        console.error('Connection failed', e);
        snack('❌ Connection Refused');
    } finally {
        if (btn && !userAddress) {
            btn.disabled = false;
            btn.textContent = 'Connect Coinbase Wallet';
        }
    }
}

function updateWalletConnectionUI() {
    if (!userAddress) return;

    const header = document.getElementById('walletStatusHeader');
    if (header) {
        header.innerHTML = `
            <div class="res-header">
                <span class="res-badge low" style="background:rgba(0,120,255,0.2);color:#0078ff;border-color:#0078ff">BASE MAINNET</span>
                <span class="chip" style="margin:0">${userAddress.slice(0, 6)}...${userAddress.slice(-4)}</span>
            </div>
        `;
    }

    const addrEl = document.getElementById('walletAddress');
    if (addrEl) addrEl.textContent = userAddress;

    // Hide connect button if it exists elsewhere
    const btn = document.getElementById('connectWalletBtn');
    if (btn) btn.style.display = 'none';
}

let ceoInterval = null;

async function toggleCEO() {
    haptic();
    const btn = document.getElementById('ceoBtn');
    const isRunning = btn.innerText.includes('Stop');

    try {
        const action = isRunning ? 'stop' : 'start';
        const res = await api(`/ceo/${action}`);
        if (res.success) {
            btn.innerText = isRunning ? 'Start Auto-Mode' : 'Stop Auto-Mode';
            btn.style.background = isRunning ? '' : '#ff4757';
            document.getElementById('ceo-status').innerText = `System: ${isRunning ? 'Idle' : 'Running'}`;
            snack(`🤖 CEO Agent ${isRunning ? 'Stopped' : 'Started'}`);

            if (!isRunning) {
                if (!ceoInterval) ceoInterval = setInterval(pollCEOLogs, 3000);
            } else {
                if (ceoInterval) {
                    clearInterval(ceoInterval);
                    ceoInterval = null;
                }
            }
        }
    } catch (e) {
        snack('❌ Failed to toggle CEO Agent');
    }
}

async function pollCEOLogs() {
    try {
        const res = await api('/ceo/logs');
        const feed = document.getElementById('ceo-feed');
        if (feed && res.logs) {
            feed.innerHTML = res.logs.map(log => {
                let color = '#ccc';
                if (log.includes('💰')) color = '#2ed573';
                if (log.includes('🕵️')) color = '#1e90ff';
                if (log.includes('📋')) color = '#ffa502';
                return `<div style="color:${color}; margin-bottom:0.25rem;">${log}</div>`;
            }).join('');
        }
        // If we see a sale, refresh the wallet
        if (res.logs && res.logs[0] && res.logs[0].includes('💰')) {
            loadWallet();
        }
    } catch (e) {
        console.error('CEO Log Poll Failed');
    }
}

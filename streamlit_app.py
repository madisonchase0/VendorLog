import streamlit as st
import streamlit.components.v1 as components

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.set_page_config(page_title="Medicare MARx + SunFire Roleplay Simulator", layout="wide")

st.title("Medicare MARx + SunFire Roleplay Simulator")
st.caption("Audio-only mode enabled: click Start listening (it will request mic permission when browser policy allows), then speak; AI replies use a grouchy old-man voice profile.")

with st.expander("Troubleshooting: simulator or voice controls not working"):
    st.markdown(
        """
- Use **Chrome or Edge** for best Web Speech API support.
- **Voice input** requires microphone permission and usually a secure context (HTTPS or localhost).
- In some hosted iframe environments, browser speech APIs may be restricted by policy.
- This build is configured for audio-only flow: microphone input for agent + spoken AI replies.
- Run locally with: `streamlit run streamlit_app.py`.
        """
    )

APP_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Medicare MARx + SunFire Roleplay Simulator</title>
<style>
:root {
  --bg: #eef4f8; --panel: #ffffff; --border: #d9e4ee; --text: #1f2937; --muted: #6b7280;
  --brand: #0f766e; --brand-dark: #115e59; --good: #dcfce7; --warn: #fef3c7; --bad: #fee2e2;
  --neutral: #eef2ff; --shadow: 0 10px 30px rgba(15, 23, 42, 0.08); --radius: 18px;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, Arial, sans-serif; background: linear-gradient(180deg, #edf4f9 0%, #f9fcff 100%); color: var(--text); }
.app { min-height: 100vh; display: grid; grid-template-columns: 320px 1fr 430px; gap: 18px; padding: 18px; }
.panel { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; }
.left-col, .right-col { display: grid; gap: 18px; align-content: start; }
.center-col { display: grid; grid-template-rows: auto auto 1fr auto; min-height: calc(100vh - 36px); }
.panel-header { padding: 16px 18px; border-bottom: 1px solid var(--border); background: #fbfdff; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
.panel-header h2, .panel-header h3 { margin: 0; font-size: 18px; line-height: 1.2; }
.subtle { font-size: 12px; color: var(--muted); margin-top: 4px; }
.toolbar { display: flex; flex-wrap: wrap; gap: 10px; padding: 16px 18px; border-bottom: 1px solid var(--border); background: #fbfdff; }
button, select {
  border: 1px solid #cbd5e1; background: white; color: var(--text); padding: 10px 14px; border-radius: 12px;
  font-weight: 700; cursor: pointer; transition: transform .15s ease, background .15s ease, border-color .15s ease;
}
button:hover { transform: translateY(-1px); }
button.primary { background: var(--brand); border-color: var(--brand); color: white; }
button.primary:hover { background: var(--brand-dark); border-color: var(--brand-dark); }
button.soft { background: #f8fbff; }
select { font-weight: 600; }
.status-row { padding: 12px 18px; border-bottom: 1px solid var(--border); background: #ffffff; display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.pill { display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 800; border: 1px solid transparent; margin-right: 6px; margin-bottom: 6px; }
.pill.good { background: var(--good); color: #166534; border-color: #b7ebc6; }
.pill.warn { background: var(--warn); color: #92400e; border-color: #f0d797; }
.pill.bad { background: var(--bad); color: #991b1b; border-color: #f6b4b4; }
.pill.neutral { background: var(--neutral); color: #3730a3; border-color: #c7d2fe; }
.summary-card { padding: 16px 18px; display: grid; gap: 12px; }
.grid-two { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.stat { border: 1px solid var(--border); border-radius: 14px; padding: 12px; background: #fcfeff; }
.label { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.value { font-size: 15px; font-weight: 700; }
.muted-box { border: 1px dashed #cbd5e1; border-radius: 14px; padding: 12px; background: #fbfdff; font-size: 13px; line-height: 1.45; }
.chat-wrap { padding: 18px; overflow: auto; display: grid; gap: 14px; align-content: start; background: radial-gradient(circle at top right, rgba(15,118,110,.06), transparent 220px), linear-gradient(180deg, #ffffff 0%, #fbfdff 100%); }
.message { max-width: 86%; padding: 14px 16px; border-radius: 16px; line-height: 1.5; white-space: pre-wrap; border: 1px solid var(--border); box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); }
.agent { justify-self: end; background: #e7fff7; border-bottom-right-radius: 6px; }
.client { justify-self: start; background: #ffffff; border-bottom-left-radius: 6px; }
.system { justify-self: center; max-width: 96%; background: #f8fbff; color: #334155; }
.composer { display: grid; grid-template-columns: 1.5fr 1.5fr auto auto auto; gap: 10px; padding: 16px 18px 18px; border-top: 1px solid var(--border); background: #fbfdff; }
textarea { width: 100%; min-height: 92px; max-height: 200px; resize: vertical; padding: 12px 14px; border-radius: 14px; border: 1px solid #cad6e2; font: inherit; color: var(--text); outline: none; }
textarea:focus, input:focus, select:focus { border-color: #60a5fa; box-shadow: 0 0 0 4px rgba(96,165,250,.15); }
.tabs { display: flex; gap: 8px; padding: 14px; border-bottom: 1px solid var(--border); background: #fbfdff; flex-wrap: wrap; }
.tab { border-radius: 999px; padding: 9px 12px; border: 1px solid #cbd5e1; background: white; font-weight: 700; font-size: 13px; cursor: pointer; }
.tab.active { background: var(--brand); color: white; border-color: var(--brand); }
.tab-content { display: none; padding: 16px; max-height: calc(100vh - 150px); overflow: auto; }
.tab-content.active { display: block; }
.mock-screen { border: 1px solid var(--border); border-radius: 16px; overflow: hidden; background: white; }
.screen-head { padding: 12px 14px; background: #e8f0f8; border-bottom: 1px solid var(--border); font-weight: 800; }
.screen-body { padding: 14px; }
.mini-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-bottom: 12px; }
.mini-field { border: 1px solid var(--border); border-radius: 12px; padding: 10px; background: #fcfeff; }
.mini-field .k { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: .05em; margin-bottom: 4px; }
.mini-field .v { font-weight: 700; font-size: 14px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #e5edf5; vertical-align: top; }
th { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); background: #f8fbff; }
.plan-card { border: 1px solid var(--border); border-radius: 16px; padding: 14px; margin-bottom: 12px; background: white; }
.plan-card.recommended { border-color: #86efac; background: linear-gradient(180deg, #f7fff9 0%, #ffffff 100%); box-shadow: 0 8px 20px rgba(34, 197, 94, 0.09); }
.plan-top { display: flex; justify-content: space-between; gap: 16px; align-items: start; }
.plan-name { font-size: 18px; font-weight: 800; margin-bottom: 6px; }
.plan-meta { font-size: 13px; color: var(--muted); }
.plan-price { text-align: right; font-weight: 800; font-size: 20px; }
.score-list { display: grid; gap: 10px; }
.score-item { border: 1px solid var(--border); border-radius: 14px; padding: 12px; background: #fcfeff; }
.score-item.pass { border-color: #86efac; background: #f7fff9; }
.score-item.fail { border-color: #fecaca; background: #fff8f8; }
.small { font-size: 12px; color: var(--muted); }
.checklist { display: grid; gap: 8px; }
.check-row { display: flex; gap: 10px; align-items: start; padding: 10px 0; border-bottom: 1px dashed #e4ebf3; }
.dot { width: 11px; height: 11px; border-radius: 999px; margin-top: 4px; background: #cbd5e1; flex: 0 0 11px; }
.dot.done { background: #16a34a; }
@media (max-width: 1350px) { .app { grid-template-columns: 1fr; } .center-col { min-height: 760px; } .tab-content { max-height: none; } }
</style>
</head>
<body>
<div class="app">
  <div class="left-col">
    <section class="panel"><div class="panel-header"><div><h3>Scenario</h3><div class="subtle">All data is fictitious and generated for training only</div></div></div><div class="summary-card" id="scenarioSummary"></div></section>
    <section class="panel"><div class="panel-header"><div><h3>Agent checklist</h3><div class="subtle">Tracks whether the agent covered the right items</div></div></div><div class="summary-card"><div class="checklist" id="checklist"></div></div></section>
    <section class="panel">
      <div class="panel-header"><div><h3>Voice + difficulty</h3><div class="subtle">Choose call challenge and voice behavior</div></div></div>
      <div class="summary-card">
        <div class="label">Call difficulty</div>
        <select id="difficultySelect"><option value="easy">Easy</option><option value="medium" selected>Medium</option><option value="hard">Hard</option></select>
        <div class="label">AI client voice</div>
        <div style="display:grid;grid-template-columns:1fr auto;gap:8px;">
          <select id="aiVoiceSelect"></select>
          <button id="randomAiVoiceBtn">Random</button>
        </div>
        <div class="label">Agent playback voice</div>
        <select id="agentVoiceSelect"></select>
        <textarea id="coachNotes" placeholder="Type coaching notes here..."></textarea>
      </div>
    </section>
  </div>

  <section class="panel center-col">
    <div class="panel-header"><div><h2>Medicare Agent vs AI Client Roleplay</h2><div class="subtle">Mock MARx check, mock SunFire plan comparison, and live AI-style client responses</div></div><div><span class="pill neutral" id="stagePill">Stage: Introduction</span></div></div>
    <div class="toolbar">
      <button class="primary" id="newScenarioBtn">New scenario</button><button class="soft" id="startCallBtn">Start roleplay</button>
      <button class="soft" id="revealMarxBtn">Reveal MARx check</button><button class="soft" id="openSunfireBtn">Open SunFire view</button>
      <button class="soft" id="scoreBtn">Score call</button><button class="soft" id="speakBtn">Replay AI voice</button>
      <button class="soft" id="voiceBtn">Start listening</button><button class="soft" id="stopVoiceBtn">Stop listening</button>
    </div>
    <div class="status-row"><div id="statusText">Ready. Click Start roleplay to begin.</div><div><span class="pill neutral" id="lookupStatus">MARx hidden</span><span class="pill neutral" id="sunfireStatus">SunFire hidden</span><span class="pill neutral" id="difficultyPill">Difficulty: Medium</span></div></div>
    <div class="chat-wrap" id="chat"></div>
    <div class="composer"><div class="muted-box" id="audioOnlyBanner"><strong>Audio-only mode:</strong> Agent input is voice only. Use Start listening, speak your line, and it will submit automatically.</div><div class="muted-box" id="lastTranscript">Last transcript: (none)</div><button id="hintBtn">Hint</button><button id="objectionBtn">Prompt objection</button><button class="primary" id="sendBtn" disabled>Typing disabled</button></div>
  </section>

  <div class="right-col"><section class="panel"><div class="tabs"><button class="tab active" data-tab="marx">Mock MARx</button><button class="tab" data-tab="sunfire">Mock SunFire</button><button class="tab" data-tab="score">Scorecard</button></div><div class="tab-content active" id="tab-marx"></div><div class="tab-content" id="tab-sunfire"></div><div class="tab-content" id="tab-score"></div></section></div>
</div>
<script>
const NAMES=[{first:'Martha',last:'Caldwell',sex:'F'},{first:'Evelyn',last:'Brooks',sex:'F'},{first:'James',last:'Holloway',sex:'M'},{first:'Robert',last:'Sutton',sex:'M'}];
const LOCATIONS=[{zip:'32114',county:'Volusia',state:'FL',city:'Daytona Beach'},{zip:'30016',county:'Newton',state:'GA',city:'Covington'},{zip:'32822',county:'Orange',state:'FL',city:'Orlando'}];
const PHARMACIES=['CVS','Walmart','Walgreens','Publix Pharmacy'];
const DRUGS=[{name:'Lisinopril 20 mg',type:'generic'},{name:'Rosuvastatin 10 mg',type:'generic'},{name:'Eliquis 5 mg',type:'brand'},{name:'Jardiance 25 mg',type:'brand'},{name:'Amlodipine 5 mg',type:'generic'}];
const DOCTORS=[{name:'Dr. Susan Reed',specialty:'PCP'},{name:'Dr. Michael Bennett',specialty:'Cardiology'},{name:'Dr. Rachel Kim',specialty:'PCP'},{name:'Dr. Nina Alvarez',specialty:'Gastroenterology'}];
const PLAN_TEMPLATES={FL:[{carrier:'Humana',name:'Humana Gold Plus',type:'HMO',contract:'H1036',pbp:'217',premium:0,moop:5400,partB:0},{carrier:'Aetna',name:'Aetna Medicare Value',type:'PPO',contract:'H5521',pbp:'404',premium:0,moop:7900,partB:0},{carrier:'Wellcare',name:'Wellcare Giveback Open',type:'PPO',contract:'H2816',pbp:'017',premium:0,moop:6900,partB:60}],GA:[{carrier:'Aetna',name:'Aetna Medicare Elite',type:'PPO',contract:'H2293',pbp:'031',premium:0,moop:9250,partB:0},{carrier:'Humana',name:'Humana Gold Plus',type:'HMO',contract:'H4141',pbp:'023',premium:0,moop:6750,partB:0},{carrier:'UnitedHealthcare',name:'AARP Medicare Advantage',type:'HMO-POS',contract:'H5322',pbp:'047',premium:0,moop:6700,partB:0}]};
const CHECKLIST_ITEMS=[{id:'greet',label:'Opened professionally and identified as licensed / recorded line style'},{id:'partAB',label:'Confirmed Medicare Part A and Part B'},{id:'medicaid',label:'Asked about Medicaid, Extra Help, LIS, or other coverage'},{id:'zip',label:'Verified ZIP code or county'},{id:'permission',label:'Asked permission to perform the lookup'},{id:'marx',label:'Used the mock MARx screen'},{id:'doctors',label:'Asked about doctors and specialists'},{id:'meds',label:'Asked about medications and pharmacy'},{id:'needs',label:'Asked what matters most to the client'},{id:'sunfire',label:'Opened the mock SunFire view'},{id:'planCompare',label:'Compared more than one plan'},{id:'recommendation',label:'Made a needs-based recommendation'},{id:'lep',label:'Handled uncovered months / LEP carefully'},{id:'close',label:'Moved toward a compliant next step'}];
const OBJECTIONS={
  easy:["That makes sense so far.","I can follow that.","If my doctors are covered, I am open to changing."],
  medium:["I don't want to switch just for a flashy benefit.","Can you show me how this is better than my current plan?","I don't want surprises later, especially with prescriptions."],
  hard:["I have heard agents promise things that were not true.","If this changes my doctors or drug costs, I am not doing it.","I need a clear reason in plain language, and I am still skeptical."]
};
let state={}; let lastAiMessage=''; let voiceRecognizer=null; let allVoices=[]; let selectedAiVoiceName=''; let selectedAgentVoiceName=''; const audioOnlyMode=true;
const AI_VOICE_PROFILE={rate:0.86,pitch:0.68,volume:1};
const rand=(arr)=>arr[Math.floor(Math.random()*arr.length)];
const randInt=(min,max)=>Math.floor(Math.random()*(max-min+1))+min;
const currency=(v)=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(v);
const sample=(arr,count)=>[...arr].sort(()=>Math.random()-0.5).slice(0,count);
function makeMBI(){const chars='ABCDEFGHJKLMNPQRSTUVWXYZ123456789';const pattern=[1,'A',1,'A','A',1,'A',1,'A',1,1];return pattern.map(p=>p==='A'?chars[randInt(0,chars.length-1)]:String(randInt(0,9))).join('');}
function makeDOB(){return `${String(randInt(1,12)).padStart(2,'0')}/${String(randInt(1,28)).padStart(2,'0')}/${randInt(1941,1960)}`;}
function makeAddress(city,state){const streets=['Oak Ridge','Pine Meadow','River Bend'];const suffixes=['Dr','Ct','Ln','Way'];return `${randInt(55,914)} ${rand(streets)} ${rand(suffixes)}, ${city}, ${state}`;}
function buildPlans(location,drugs,docs){const templates=PLAN_TEMPLATES[location.state]||PLAN_TEMPLATES.FL;const current=rand(templates);const brandCount=drugs.filter(d=>d.type==='brand').length;const plans=templates.map((t,i)=>{const docFit=i===1?'partial':'good';const drugFit=i===2?'best':(i===1?'good':'okay');const annualDrugCost=Math.max(90,320+brandCount*randInt(300,950)+i*120-(drugFit==='best'?420:drugFit==='good'?180:0));const annualMedicalEstimate=randInt(250,1400)+(docFit==='partial'?500:0);const annualPremium=Number((t.premium*12).toFixed(2));const annualTotal=Number((annualDrugCost+annualMedicalEstimate+annualPremium).toFixed(2));const plan={...t,id:`${t.contract}-${t.pbp}-000`,annualDrugCost,annualMedicalEstimate,annualPremium,annualTotal,deductible:brandCount>=2?rand([420,590,615]):rand([0,120,250,420]),specialistCopay:rand(['$20','$35','$45','$55']),docFit,drugFit,recommended:false,notes:[]};if(docFit==='good'){plan.notes.push(`${docs.pcp.name} appears in network`);plan.notes.push(`${docs.specialist.name} appears in network`);}else{plan.notes.push(`${docs.specialist.name} needs manual provider confirmation`);}if(drugFit==='best')plan.notes.push('Best prescription estimate of compared options');if(t.partB>0)plan.notes.push(`Includes Part B giveback up to $${t.partB}`);return plan;});plans.sort((a,b)=>a.annualTotal-b.annualTotal);plans[0].recommended=true;return {plans,currentPlan:current};}
function generateScenario(){const person=rand(NAMES);const location=rand(LOCATIONS);const dob=makeDOB();const pharmacy=rand(PHARMACIES);const drugs=sample(DRUGS,3);const docsPool=sample(DOCTORS,4);const pcp=docsPool.find(x=>x.specialty==='PCP')||DOCTORS[0];const specialist=docsPool.find(x=>x.specialty!=='PCP')||DOCTORS[1];const {plans,currentPlan}=buildPlans(location,drugs,{pcp,specialist});const lis=Math.random()>0.78;const medicaid=!lis&&Math.random()>0.82;const uncoveredMonths=Math.random()>0.58?rand([0,0,0,4,7,9]):0;const otherCoverage=Math.random()>0.84;const priorities=['keeping my doctors and lowering total costs','lower prescription costs and staying at my pharmacy','lower specialist copays and predictable coverage'];return {person,location,dob,mbi:makeMBI(),address:makeAddress(location.city,location.state),pharmacy,drugs,pcp,specialist,plans,currentPlan,lis,medicaid,uncoveredMonths,otherCoverage,priority:rand(priorities),stage:'Introduction',started:false,marxRevealed:false,sunfireOpened:false,planChosen:null,lastHint:'',score:null,difficulty:document.getElementById('difficultySelect').value,checklist:Object.fromEntries(CHECKLIST_ITEMS.map(i=>[i.id,false]))};}
function renderScenarioSummary(){const s=state;document.getElementById('scenarioSummary').innerHTML=`<div class="grid-two"><div class="stat"><div class="label">Client</div><div class="value">${s.person.first} ${s.person.last}</div></div><div class="stat"><div class="label">DOB</div><div class="value">${s.dob}</div></div><div class="stat"><div class="label">ZIP / County</div><div class="value">${s.location.zip} / ${s.location.county}</div></div><div class="stat"><div class="label">Priority</div><div class="value">${s.priority}</div></div></div><div class="muted-box"><div><strong>Current coverage:</strong> ${s.currentPlan.carrier} ${s.currentPlan.name} (${s.currentPlan.type})</div><div style="margin-top:8px;"><strong>Pharmacy:</strong> ${s.pharmacy}</div><div><strong>Doctors:</strong> ${s.pcp.name} and ${s.specialist.name}</div><div><strong>Meds:</strong> ${s.drugs.map(d=>d.name).join(', ')}</div></div>`;}
function renderChecklist(){document.getElementById('checklist').innerHTML=CHECKLIST_ITEMS.map(item=>`<div class="check-row"><span class="dot ${state.checklist[item.id]?'done':''}"></span><div style="font-weight:700;">${item.label}</div></div>`).join('');}
function renderMarx(){const s=state;document.getElementById('tab-marx').innerHTML=`<div class="mock-screen"><div class="screen-head">Beneficiary Lookup</div><div class="screen-body"><div class="mini-grid"><div class="mini-field"><div class="k">MBI Number</div><div class="v">${s.mbi}</div></div><div class="mini-field"><div class="k">Name</div><div class="v">${s.person.last.toUpperCase()}, ${s.person.first.toUpperCase()}</div></div><div class="mini-field"><div class="k">Birth Date</div><div class="v">${s.dob}</div></div><div class="mini-field"><div class="k">Address</div><div class="v">${s.address}</div></div></div><div><span class="pill ${s.uncoveredMonths>0?'warn':'good'}">Uncovered months: ${s.uncoveredMonths}</span><span class="pill ${s.lis?'good':'neutral'}">LIS: ${s.lis?'Yes':'No'}</span><span class="pill ${s.medicaid?'good':'neutral'}">Medicaid: ${s.medicaid?'Yes':'No'}</span></div></div></div>`;}
function renderSunfire(){const s=state;document.getElementById('tab-sunfire').innerHTML=`<div class="mock-screen"><div class="screen-head">Plans for ${s.location.zip} (${s.plans.length} results)</div><div class="screen-body">${s.plans.map((plan,index)=>`<div class="plan-card ${plan.recommended?'recommended':''}"><div class="plan-top"><div><div class="plan-name">${plan.carrier} ${plan.name} (${plan.type})</div><div class="plan-meta">2026 ${plan.id}</div><div style="margin-top:8px;"><span class="pill ${plan.docFit==='good'?'good':'warn'}">Doctor fit: ${plan.docFit}</span><span class="pill ${plan.drugFit==='best'?'good':plan.drugFit==='good'?'neutral':'warn'}">Drug fit: ${plan.drugFit}</span></div></div><div class="plan-price">${currency(plan.premium)}<div class="small">monthly premium</div></div></div><table><thead><tr><th>MOOP</th><th>Specialist Copay</th><th>Drug Deductible</th><th>Annual Drug Cost</th><th>Estimated Annual Total</th></tr></thead><tbody><tr><td>${currency(plan.moop)}</td><td>${plan.specialistCopay}</td><td>${currency(plan.deductible)}</td><td>${currency(plan.annualDrugCost)}</td><td><strong>${currency(plan.annualTotal)}</strong></td></tr></tbody></table><div style="margin-top:10px;">${plan.notes.map(n=>`<span class="pill neutral">${n}</span>`).join('')}</div><div style="margin-top:12px;"><button class="${state.planChosen===index?'primary':''}" onclick="selectPlan(${index})">${state.planChosen===index?'Selected as recommendation':'Select as recommendation'}</button></div></div>`).join('')}</div></div>`;}
function renderScorecard(score){let html='<div class="muted-box"><strong>Scoring</strong><div style="margin-top:8px;">This simulator grades whether the agent covered discovery, used the tools, handled uncovered months, and made a needs-based recommendation.</div></div>';if(!score){html+='<div style="margin-top:12px;" class="small">No score yet. Click Score call after the roleplay.</div>';}else{html+=`<div class="stat" style="margin-top:12px;"><div class="label">Overall score</div><div class="value">${score.points}/100</div></div><div class="score-list" style="margin-top:12px;">${score.items.map(item=>`<div class="score-item ${item.pass?'pass':'fail'}"><div style="font-weight:800;">${item.pass?'Pass':'Needs work'} · ${item.label}</div><div class="small" style="margin-top:6px;">${item.detail}</div></div>`).join('')}</div><div class="muted-box" style="margin-top:12px;"><strong>Coach summary</strong><div style="margin-top:8px;">${score.summary}</div></div>`;}document.getElementById('tab-score').innerHTML=html;}
function setStage(stage){state.stage=stage;document.getElementById('stagePill').textContent=`Stage: ${stage}`;}
function setStatus(message){document.getElementById('statusText').textContent=message;}
function addMessage(type,text){const chat=document.getElementById('chat');const div=document.createElement('div');div.className=`message ${type}`;div.textContent=text;chat.appendChild(div);chat.scrollTop=chat.scrollHeight;if(type==='client'){lastAiMessage=text;if(audioOnlyMode)speakLastMessage();}}
function resetChat(){document.getElementById('chat').innerHTML='';}
function updateChecklistFromText(text){const t=text.toLowerCase();const mark=(id)=>state.checklist[id]=true;if(/(licensed|recorded line|my name is|this is)/.test(t))mark('greet');if(/part a|part b/.test(t))mark('partAB');if(/medicaid|extra help|lis|other coverage|va|tricare|employer/.test(t))mark('medicaid');if(/zip|county/.test(t))mark('zip');if(/permission|may i proceed|look you up|look up your medicare/.test(t))mark('permission');if(/doctor|pcp|specialist|hospital/.test(t))mark('doctors');if(/medication|prescription|pharmacy|drug/.test(t))mark('meds');if(/important to you|priority|what matters most|dental|vision|cost/.test(t))mark('needs');if(/compare|hmo|ppo|premium|moop|annual cost|deductible|option/.test(t))mark('planCompare');if(/recommend|best fit|based on what you told me|i would suggest/.test(t))mark('recommendation');if(/lep|late enrollment|uncovered months|creditable coverage|63 days|penalty/.test(t))mark('lep');if(/enroll|move forward|next step|go through that plan|how does that sound/.test(t))mark('close');renderChecklist();}
function switchTab(name){document.querySelectorAll('.tab').forEach(tab=>tab.classList.toggle('active',tab.dataset.tab===name));document.querySelectorAll('.tab-content').forEach(c=>c.classList.toggle('active',c.id===`tab-${name}`));}
function updateDifficultyPill(){const d=state.difficulty||document.getElementById('difficultySelect').value;document.getElementById('difficultyPill').textContent=`Difficulty: ${d[0].toUpperCase()}${d.slice(1)}`;document.getElementById('difficultyPill').className=`pill ${d==='easy'?'good':d==='medium'?'warn':'bad'}`;}
function startScenario(){state=generateScenario();renderScenarioSummary();renderChecklist();renderMarx();renderSunfire();renderScorecard(null);resetChat();setStage('Introduction');document.getElementById('lookupStatus').textContent='MARx hidden';document.getElementById('lookupStatus').className='pill neutral';document.getElementById('sunfireStatus').textContent='SunFire hidden';document.getElementById('sunfireStatus').className='pill neutral';updateDifficultyPill();setStatus('Ready. Click Start roleplay to begin.');addMessage('system','Scenario loaded. Start roleplay when ready. Difficulty controls how objections are presented.');switchTab('marx');}
function startCall(){if(state.started)return;state.started=true;setStatus('Roleplay started. Begin with your greeting and fact find.');addMessage('client',`Hello, this is ${state.person.first} ${state.person.last}.`);}
function revealMarx(){state.marxRevealed=true;state.checklist.marx=true;renderChecklist();document.getElementById('lookupStatus').textContent='MARx shown';document.getElementById('lookupStatus').className='pill good';setStage('Lookup');setStatus('MARx check is visible.');switchTab('marx');addMessage('system',`Mock MARx check revealed. Fake MBI for training: ${state.mbi}.`);}
function openSunfire(){state.sunfireOpened=true;state.checklist.sunfire=true;renderChecklist();document.getElementById('sunfireStatus').textContent='SunFire shown';document.getElementById('sunfireStatus').className='pill good';setStage('Plan Review');setStatus('SunFire view is visible.');switchTab('sunfire');addMessage('system','Compare at least two plans and explain your recommendation.');}
function selectPlan(index){state.planChosen=index;renderSunfire();}
window.selectPlan=selectPlan;
function hintText(){const hints={Introduction:'Confirm Part A/B, ZIP, and Medicaid/Extra Help, then ask permission for lookup.',Lookup:'Use MARx details: DOB, entitlement, LIS, uncovered months.', 'Needs Assessment':'Ask about PCP, specialists, medications, pharmacy, and priorities.', 'Plan Review':'Compare two plans using premium, MOOP, doctor fit, and total annual estimate.', Close:'Recommend clearly and ask for a compliant next step.'};return hints[state.stage]||'Keep fact-finding.';}
const normalize=(text)=>text.toLowerCase().replace(/[^a-z0-9$ ]/g,' ');
function difficultyObjection(){const arr=OBJECTIONS[state.difficulty]||OBJECTIONS.medium;return rand(arr);}
function aiRespond(input){const t=normalize(input);updateChecklistFromText(input);if(/permission|may i proceed|look you up|look up/.test(t)&&state.stage==='Introduction')setStage('Lookup');if(/priority|important to you|what matters most/.test(t))setStage('Needs Assessment');if(/compare|hmo|ppo|option|premium|annual cost|moop|deductible/.test(t))setStage('Plan Review');if(/recommend|best fit|i would suggest/.test(t))setStage('Close');if(/(hello|hi|good morning|good afternoon)/.test(t)&&state.stage==='Introduction')return `${state.person.first} ${state.person.last} speaking.`;if(/part a|part b/.test(t))return 'Yes, I have both Medicare Part A and Part B.';if(/zip|county/.test(t))return `My ZIP code is ${state.location.zip} and I am in ${state.location.county} County.`;if(/medicaid|extra help|lis/.test(t)){if(state.medicaid)return 'Yes, I do receive Medicaid.';if(state.lis)return 'I do receive Extra Help on prescriptions.';return 'No, I do not receive Medicaid and I do not think I get Extra Help.';}if(/permission|may i proceed|look you up|look up/.test(t))return 'Yes, that is fine. What do you need from me?';if(/date of birth|dob/.test(t))return `My date of birth is ${state.dob}.`;if(/doctor|pcp|primary care/.test(t))return `My main doctor is ${state.pcp.name}.`;if(/specialist|hospital/.test(t))return `I also see ${state.specialist.name}.`;if(/medication|prescription|drug/.test(t))return `I take ${state.drugs.map(d=>d.name).join(', ')}.`;if(/pharmacy/.test(t))return `I usually use ${state.pharmacy}.`;if(/important to you|priority|what matters most/.test(t))return `The biggest thing for me is ${state.priority}.`;if(/hmo|ppo|premium|moop|annual cost|deductible|compare|option/.test(t)||/recommend|best fit|based on what you told me|i would suggest/.test(t))return difficultyObjection();if(/enroll|move forward|next step|review that option|go through that plan|how does that sound/.test(t))return state.difficulty==='hard'?'I am still hesitant. Please summarize risks and benefits one more time.':'I would want to hear it one more time before making a final decision, but that sounds reasonable.';const fallbacks={easy:'I am listening and this feels straightforward.',medium:'I am listening. I want to make sure the details are right.',hard:'I am cautious. Please be specific and do not rush me.'};return fallbacks[state.difficulty]||'Okay.';}
function scoreCall(){const c=state.checklist;const items=[];let points=0;const add=(label,pass,detail,value)=>{items.push({label,pass,detail});if(pass)points+=value;};add('Opening and eligibility',c.greet&&c.partAB,c.greet&&c.partAB?'The agent opened appropriately and confirmed Part A and Part B.':'Open professionally and verify Part A/Part B.',12);add('Lookup setup',c.zip&&c.permission,c.zip&&c.permission?'ZIP/county and permission were covered.':'Verify location and ask permission before lookup.',10);add('MARx usage',c.marx,c.marx?'MARx was used.':'Use the MARx panel.',10);add('Discovery',c.medicaid&&c.doctors&&c.meds&&c.needs,c.medicaid&&c.doctors&&c.meds&&c.needs?'Coverage, doctors, meds, and priorities were gathered.':'Complete full discovery before recommending.',22);add('SunFire usage',c.sunfire&&c.planCompare,c.sunfire&&c.planCompare?'SunFire and comparison used.':'Compare two options in SunFire.',15);add('Recommendation quality',c.recommendation&&state.planChosen!==null,c.recommendation&&state.planChosen!==null?`Recommendation given with selected plan ${state.plans[state.planChosen].carrier} ${state.plans[state.planChosen].name}.`:'Give a needs-based recommendation and select plan.',15);add('Uncovered months / LEP handling',state.uncoveredMonths===0||c.lep,state.uncoveredMonths===0?'No special LEP handling needed.':(c.lep?'LEP handled carefully.':'Address uncovered months and possible LEP carefully.'),8);add('Close / next step',c.close,c.close?'A next step was offered.':'Move to a clear next step.',8);state.score={points,items,summary:points>=90?'Strong roleplay.':points>=75?'Solid structure with room to tighten recommendations.':'Needs more structure and complete discovery.'};renderScorecard(state.score);switchTab('score');addMessage('system',`Score complete: ${points}/100.`);}
function getVoiceByName(name){return allVoices.find(v=>v.name===name)||null;}
function pickGrouchyVoice(options){const preferredNames=['david','fred','george','grandpa','oldman','male','baritone','microsoft mark','microsoft david','google uk english male','en-us-neural2-j','en-us-neural2-d'];const found=options.find(v=>preferredNames.some(k=>v.name.toLowerCase().includes(k)));return found||options[0];}
function populateVoiceSelects(){allVoices=window.speechSynthesis?window.speechSynthesis.getVoices():[];const preferred=allVoices.filter(v=>v.lang.toLowerCase().startsWith('en'));const options=(preferred.length?preferred:allVoices);const aiSel=document.getElementById('aiVoiceSelect');const agSel=document.getElementById('agentVoiceSelect');aiSel.innerHTML='';agSel.innerHTML='';if(!options.length){aiSel.innerHTML='<option>No voices available</option>';agSel.innerHTML='<option>No voices available</option>';return;}
options.forEach(v=>{const label=`${v.name} (${v.lang})`;aiSel.add(new Option(label,v.name));agSel.add(new Option(label,v.name));});if(!selectedAiVoiceName)selectedAiVoiceName=pickGrouchyVoice(options).name;if(!selectedAgentVoiceName)selectedAgentVoiceName=options[0].name;aiSel.value=selectedAiVoiceName;agSel.value=selectedAgentVoiceName;}
function speakText(text,voiceName){if(!('speechSynthesis' in window)){alert('Speech synthesis is not supported in this browser.');return;}if(!text)return;window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(text);const voice=getVoiceByName(voiceName);if(voice)utterance.voice=voice;if(voiceName===selectedAiVoiceName){utterance.rate=AI_VOICE_PROFILE.rate;utterance.pitch=AI_VOICE_PROFILE.pitch;utterance.volume=AI_VOICE_PROFILE.volume;}else{utterance.rate=1;utterance.pitch=1;}window.speechSynthesis.speak(utterance);}
function speakLastMessage(){speakText(lastAiMessage,selectedAiVoiceName);}
function randomizeAiVoice(){if(!allVoices.length)populateVoiceSelects();const options=allVoices.filter(v=>v.lang.toLowerCase().startsWith('en'));const chosen=rand(options.length?options:allVoices);if(!chosen)return;selectedAiVoiceName=chosen.name;document.getElementById('aiVoiceSelect').value=chosen.name;setStatus(`AI client voice set to ${chosen.name}.`);}
async function requestMicPermission(){
  const candidates=[window,window.parent,window.top];
  const tried=[];
  for(const ctx of candidates){
    try{
      if(ctx&&ctx.navigator&&ctx.navigator.mediaDevices&&ctx.navigator.mediaDevices.getUserMedia){
        const stream=await ctx.navigator.mediaDevices.getUserMedia({audio:true});
        stream.getTracks().forEach(t=>t.stop());
        return true;
      }
      tried.push('no-mediaDevices');
    }catch(err){
      const code=(err&&err.name)||'unknown';
      tried.push(code);
      if(code==='NotAllowedError'||code==='SecurityError'){
        setStatus('Microphone blocked. Use the browser lock/site-settings icon to allow microphone, then try again.');
        return false;
      }
    }
  }
  setStatus('Could not directly request mic permission here; trying speech recognition start anyway.');
  return true;
}
function setupVoice(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){alert('Speech recognition is not supported in this browser.');return null;}const rec=new SR();rec.lang='en-US';rec.interimResults=false;rec.continuous=true;rec.onresult=(event)=>{const text=event.results[event.results.length-1][0].transcript.trim();if(!text)return;document.getElementById('lastTranscript').textContent=`Last transcript: ${text}`;handleAgentUtterance(text);};rec.onerror=(event)=>{const code=event&&event.error?event.error:'unknown';if(code==='not-allowed'||code==='service-not-allowed'){setStatus('Microphone blocked. Allow microphone permission and try Start listening again.');}else{setStatus(`Voice input error: ${code}.`);}};rec.onstart=()=>setStatus('Listening for agent speech...');rec.onend=()=>setStatus('Voice input stopped.');return rec;}
function handleAgentUtterance(text){if(!text)return;if(!state.started)startCall();addMessage('agent',text);const reply=aiRespond(text);addMessage('client',reply);setStatus(`Stage: ${state.stage}. Continue the roleplay.`);}
function forceObjection(){addMessage('client',difficultyObjection());}
document.getElementById('newScenarioBtn').addEventListener('click',startScenario);document.getElementById('startCallBtn').addEventListener('click',startCall);document.getElementById('revealMarxBtn').addEventListener('click',revealMarx);document.getElementById('openSunfireBtn').addEventListener('click',openSunfire);document.getElementById('scoreBtn').addEventListener('click',scoreCall);document.getElementById('speakBtn').addEventListener('click',speakLastMessage);document.getElementById('objectionBtn').addEventListener('click',forceObjection);
document.getElementById('hintBtn').addEventListener('click',()=>addMessage('system',`Hint: ${hintText()}`));
document.getElementById('voiceBtn').addEventListener('click',async ()=>{const ok=await requestMicPermission();if(!ok)return;if(!voiceRecognizer)voiceRecognizer=setupVoice();if(voiceRecognizer){try{voiceRecognizer.start();}catch(e){setStatus('Could not start voice recognition. Try Stop listening, then Start listening again.');}}});
document.getElementById('stopVoiceBtn').addEventListener('click',()=>{if(voiceRecognizer)voiceRecognizer.stop();});
document.getElementById('difficultySelect').addEventListener('change',(e)=>{state.difficulty=e.target.value;updateDifficultyPill();});
document.getElementById('aiVoiceSelect').addEventListener('change',(e)=>selectedAiVoiceName=e.target.value);document.getElementById('agentVoiceSelect').addEventListener('change',(e)=>selectedAgentVoiceName=e.target.value);document.getElementById('randomAiVoiceBtn').addEventListener('click',randomizeAiVoice);
document.querySelectorAll('.tab').forEach(tab=>tab.addEventListener('click',()=>switchTab(tab.dataset.tab)));
if('speechSynthesis' in window){populateVoiceSelects();window.speechSynthesis.onvoiceschanged=populateVoiceSelects;}
startScenario();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=1400, scrolling=True)

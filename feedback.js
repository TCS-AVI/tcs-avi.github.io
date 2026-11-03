/* Gentle feedback prompt. Nothing is sent automatically: the person chooses to send by email (or WhatsApp / a form if you fill those in).
   EDIT THE THREE LINES BELOW. */
window.TCS_CONFIG={
  email:"baglajakh@gmail.com",   // where feedback emails go
  whatsapp:"",                   // optional: your number with country code and no +, e.g. 919876543210
  formUrl:""                     // optional: a Google Form link; if filled, the button opens the form instead of email
};
(function(){
  var C=window.TCS_CONFIG,K="fb_state";
  function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}return null}
  var st={};try{st=JSON.parse(ls(K)||"{}")}catch(e){}
  try{if(!sessionStorage.getItem("fb_sess")){sessionStorage.setItem("fb_sess","1");st.visits=(st.visits||0)+1;ls(K,JSON.stringify(st))}}catch(e){}
  var DAY=864e5;
  function css(){if(document.getElementById("fbcss"))return;var s=document.createElement("style");s.id="fbcss";s.textContent=
   "#fbbox{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));max-width:560px;margin:0 auto;z-index:10000;background:var(--card,#fff);color:var(--ink,var(--fg,#1c1b19));border:2px solid var(--acc,var(--ok,#0b3d91));border-radius:16px;padding:16px;box-shadow:0 8px 30px rgba(0,0,0,.3);font:inherit;max-height:90vh;overflow:auto}"+
   "#fbbox h2{font-size:1.05rem;margin:0 0 4px}#fbbox p{margin:4px 0 10px;font-size:.92rem;color:var(--mut,#6b675f)}"+
   "#fbbox .fr{display:flex;gap:8px;margin:8px 0}#fbbox .fr button{flex:1;font-size:1.5rem;padding:8px 0}#fbbox .fr button[aria-pressed=true]{outline:3px solid var(--acc,var(--ok,#0b3d91))}"+
   "#fbbox textarea{width:100%;min-height:70px;font:inherit;padding:8px;border-radius:10px;border:1px solid var(--line,#ccc);background:var(--bg,#fff);color:inherit}"+
   "#fbbox .fb{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}#fbbox button{font:inherit;padding:9px 14px;border-radius:10px;border:1px solid var(--line,#ccc);background:var(--card,#fff);color:inherit;cursor:pointer}"+
   "#fbbox button.go{background:var(--acc,var(--ok,#0b3d91));color:var(--card,#fff);border-color:var(--acc,var(--ok,#0b3d91))}";
   document.head.appendChild(s)}
  function open(app,opts){
    if(document.getElementById("fbbox"))return;css();
    var rating=0,box=document.createElement("div");box.id="fbbox";box.setAttribute("role","dialog");box.setAttribute("aria-modal","false");box.setAttribute("aria-labelledby","fbt");
    function mk(t,a,c){var e=document.createElement(t);if(a)for(var k in a)e.setAttribute(k,a[k]);if(c)e.textContent=c;return e}
    var h=mk("h2",{id:"fbt"},"How is this helping you?");box.appendChild(h);
    box.appendChild(mk("p",null,"You are not alone in this journey. A real person reads every message, and your words help the next student too. One line is enough."));
    var fr=mk("div",{"class":"fr",role:"group","aria-label":"Your rating"}),E=[["😕","Not helpful"],["🙂","Okay"],["😊","Helpful"],["🤩","Loved it"]],bs=[];
    E.forEach(function(x,i){var b=mk("button",{type:"button","aria-label":x[1],"aria-pressed":"false",title:x[1]},x[0]);b.onclick=function(){rating=i+1;bs.forEach(function(q,j){q.setAttribute("aria-pressed",j===i?"true":"false")})};bs.push(b);fr.appendChild(b)});
    box.appendChild(fr);
    var ta=mk("textarea",{placeholder:"What is working? What would make it better? Which exam are you preparing for?","aria-label":"Your feedback"});box.appendChild(ta);
    var row=mk("div",{"class":"fb"});
    function body(){return "Rating: "+(rating?E[rating-1][0]+" ("+rating+"/4, "+E[rating-1][1]+")":"not given")+"\nApp: "+app+"\n\nMessage:\n"+ta.value.trim()+"\n"}
    function done(days){st.snooze=Date.now()+days*DAY;ls(K,JSON.stringify(st));box.remove()}
    function thanks(){box.innerHTML="";box.appendChild(mk("h2",null,"Thank you"));box.appendChild(mk("p",null,"Your message means a lot. Keep going: you are doing better than you think."));var c=mk("button",{type:"button","class":"go"},"Close");c.onclick=function(){box.remove()};box.appendChild(c);c.focus()}
    if(C.formUrl){var f=mk("button",{type:"button","class":"go"},"Open feedback form");f.onclick=function(){window.open(C.formUrl,"_blank","noopener");st.snooze=Date.now()+60*DAY;ls(K,JSON.stringify(st));thanks()};row.appendChild(f)}
    else{var m=mk("button",{type:"button","class":"go"},"Send by email");m.onclick=function(){var l=mk("a",{href:"mailto:"+C.email+"?subject="+encodeURIComponent("App feedback "+(rating?E[rating-1][0]:""))+"&body="+encodeURIComponent(body())});document.body.appendChild(l);l.click();l.remove();st.snooze=Date.now()+60*DAY;ls(K,JSON.stringify(st));thanks()};row.appendChild(m)}
    if(C.whatsapp){var w=mk("button",{type:"button"},"Send on WhatsApp");w.onclick=function(){window.open("https://wa.me/"+C.whatsapp+"?text="+encodeURIComponent(body()),"_blank","noopener");st.snooze=Date.now()+60*DAY;ls(K,JSON.stringify(st));thanks()};row.appendChild(w)}
    var n=mk("button",{type:"button"},"Not now");n.onclick=function(){done(opts&&opts.force?0:14)};row.appendChild(n);
    box.appendChild(row);
    box.appendChild(mk("p",{style:"font-size:.78rem;margin:10px 0 0"},"We use your message only to read it, reply and improve the app. It goes to "+C.email+" through your own email app, and we delete it within 12 months. Nothing is sent unless you press send. See Privacy."));
    box.addEventListener("keydown",function(e){if(e.key==="Escape")n.onclick()});
    document.body.appendChild(box);setTimeout(function(){try{bs[2].focus()}catch(e){}},50)}
  // natural moments only (end of a quiz, test or typing stage), never mid-task; at most every 14 days, after a few visits
  window.askFeedback=function(app,opts){
    try{if(opts&&opts.force){open(app||"app",opts);return}
      if((st.visits||0)<3)return;if(st.snooze&&Date.now()<st.snooze)return;if(Math.random()>.6)return;
      setTimeout(function(){open(app||"app")},2500)}catch(e){}};
})();

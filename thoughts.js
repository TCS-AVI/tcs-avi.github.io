/* Friendly thoughts shown when the app opens. k: m = motivation, g = gratitude, w = wellbeing.
   Edit freely: keep each line short, kind and free of pressure. */
window.CA_THOUGHTS={items:[
{k:"m",t:"Small steps count. Twenty focused minutes today beat a perfect plan you never start."},
{k:"m",t:"You do not need to be the best today. You only need to be a little better than yesterday."},
{k:"m",t:"A wrong answer is not a failure. It is exactly what you needed to find before the exam did."},
{k:"m",t:"Progress is rarely loud. Quiet days of practice add up to results that people call sudden."},
{k:"m",t:"Tired? Rest, then come back. Rest is part of the plan, not a break from it."},
{k:"m",t:"Compare your today with your yesterday, not with someone else's highlight reel."},
{k:"m",t:"Every topic that feels hard right now was once a topic you could not even name."},
{k:"m",t:"Consistency is a gentle kind of courage. Show up again today."},
{k:"m",t:"One more question. Then one more. That is how mountains get climbed."},
{k:"m",t:"Your hard work is not wasted just because the result has not arrived yet."},
{k:"m",t:"Be patient with yourself. You are learning, not performing."},
{k:"m",t:"If yesterday went badly, start today clean. You are always allowed to begin again."},
{k:"m",t:"Dream big, plan small, practise daily."},
{k:"m",t:"The seat you are working towards is being earned a little every day, including today."},
{k:"m",t:"Mistakes are proof that you are attempting something difficult."},
{k:"m",t:"Focus on the next question, not the whole syllabus."},
{k:"m",t:"You have already come further than the person who first decided to try."},
{k:"m",t:"Confidence is built from promises you keep to yourself. Keep one small promise today."},
{k:"m",t:"Do it tired, do it slowly, but do something today."},
{k:"m",t:"Good things take time. Keep going. Your effort is quietly adding up."},
{k:"m",t:"Trust the work you have put in. It will be there for you on exam day."},
{k:"m",t:"Even ten minutes of revision tonight matters."},
{k:"m",t:"Remember why you started, and let that reason carry you through the boring parts."},
{k:"m",t:"A bad mock test today is a free lesson for the real exam."},
{k:"m",t:"A calm mind remembers more. Take one slow breath before you begin."},
{k:"m",t:"Your future self is already grateful for the effort you make today."},
{k:"m",t:"It is okay if your path looks different from your friends'. It is still your path."},
{k:"m",t:"You opened the app today. That is already a step forward."},
{k:"m",t:"People who succeed are often just the ones who did not stop."},
{k:"m",t:"You are allowed to be proud of how far you have come, even while you keep climbing."},
{k:"g",t:"A small reminder: have you thanked your parents lately? A simple \"thank you for everything\" can make their whole day."},
{k:"g",t:"Somebody probably worried about your exam late at night. Say thank you to them today."},
{k:"g",t:"Your brother or sister has likely covered for you while you studied. Send them a thank-you."},
{k:"g",t:"Call someone who believes in you, just to say thanks. It takes two minutes."},
{k:"g",t:"Think of the friend who answers your doubts at odd hours. Tell them you are grateful."},
{k:"g",t:"Your family's small sacrifices are part of this journey. A kind word or a hug says a lot."},
{k:"g",t:"Thank a teacher who helped you, even if it was long ago. Teachers remember the students who say it."},
{k:"g",t:"When you succeed, remember the people who brought you tea, silence and patience at your study table."},
{k:"g",t:"Tell one person today: \"I could not have done this without you.\" And mean it."},
{k:"g",t:"Maybe your mother has not heard a thank-you in a while. Today is a good day for it."},
{k:"g",t:"A message, a call, a note: gratitude is free and always on time."},
{k:"g",t:"Someone's hard work is paying for your books and your time. A kind word to them will matter."},
{k:"g",t:"When you have good news, share it first with the people who supported you."},
{k:"g",t:"Help a friend with a topic today. Passing kindness on is a lovely way of saying thanks."},
{k:"g",t:"Study partners are precious. Thank the one who revises with you."},
{k:"g",t:"If your family is tired of hearing about your exam, thank them for listening anyway."},
{k:"g",t:"If a parent or guardian is nearby, sit with them for five minutes before you study."},
{k:"g",t:"Say thank you to whoever made your last meal. Home-cooked support counts."},
{k:"g",t:"Be someone's encouragement today. Message a friend and tell them you believe in them."},
{k:"g",t:"If your loved ones are far away today, a message across the distance still carries love."},
{k:"g",t:"Remember the cousin, neighbour or friend who shared their notes. Pay it forward."},
{k:"g",t:"Who has looked after you on this journey? Parent, guardian, sibling, teacher or friend: let them know today."},
{k:"w",t:"Drink some water and stretch your shoulders. Your brain works better when your body is looked after."},
{k:"w",t:"Sleep is part of studying. Memory gets stored while you rest."},
{k:"w",t:"Look away from the screen for a minute and focus on something far away. Your eyes will thank you."},
{k:"w",t:"A ten-minute walk can clear a foggy head better than another hour of staring."},
{k:"w",t:"Eat something proper before a long study session."},
{k:"w",t:"If the pressure feels heavy today, talk to someone you trust. You do not have to carry it alone."},
{k:"w",t:"The phone can wait. Put it away for twenty minutes and see how much you finish."},
{k:"w",t:"Take a real break between sessions. Short rests keep long study sustainable."},
{k:"w",t:"Breathe in slowly for four counts, out for six. Do it three times, then begin."},
{k:"w",t:"Your worth is not your rank. Study hard, and be kind to yourself too."},
{k:"w",t:"Step into sunlight for a few minutes today if you can."},
{k:"w",t:"Revise tonight, then sleep on time. Tomorrow's you will remember more."}
]};
window.pickThought=function(extraName){
  var T=(window.CA_THOUGHTS||{}).items||[];if(!T.length)return null;
  var ist=new Date(Date.now()+19800000),h=ist.getUTCHours(),g;
  g=h>=5&&h<12?"Good morning":h<17&&h>=12?"Good afternoon":h>=17&&h<22?"Good evening":"Hello, night owl";
  if(extraName)g+=", "+extraName;
  var seen=[];try{seen=JSON.parse(localStorage.getItem("th_seen")||"[]")}catch(e){}
  function one(){var r=Math.random(),k=r<.55?"m":r<.85?"g":"w",pool=T.filter(function(x){return x.k===k&&seen.indexOf(x.t)<0});
    if(!pool.length)pool=T.filter(function(x){return seen.indexOf(x.t)<0});if(!pool.length){seen=[];pool=T}
    return pool[Math.floor(Math.random()*pool.length)]}
  var x=one();seen.push(x.t);seen=seen.slice(-14);try{localStorage.setItem("th_seen",JSON.stringify(seen))}catch(e){}
  var late=(h>=23||h<4)&&x.k!=="w"?" It is late, so rest soon.":"";
  return {greet:g,text:x.t+(late&&Math.random()<.5?late:""),k:x.k};
};

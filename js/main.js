(function(){
"use strict";
var GD=window.GD||{branches:[]};
var $=function(s,r){return (r||document).querySelector(s)};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var html=document.documentElement;

/* welcome animation: sunrise, then a gold flood into the page (once per session, home only) */
(function(){
  var w=$("#welcome");
  if(!w){return}
  function heroIn(){var h=$(".hero");if(h){h.classList.add("hero-in")}}
  if(!html.classList.contains("wel")){heroIn();w.parentNode.removeChild(w);return}
  var c=$(".w-count",w),t0=performance.now(),raf=0,ended=false,timers=[],DUR=3300;
  function tick(n){
    if(ended){return}
    var p=Math.min(1,(n-t0)/DUR);
    if(c){c.textContent=("00"+Math.round(p*100)).slice(-3)}
    if(p<1){raf=requestAnimationFrame(tick)}
  }
  raf=requestAnimationFrame(tick);
  function done(){
    html.classList.remove("wel");
    try{sessionStorage.setItem("gdw","1")}catch(e){}
    if(w.parentNode){w.parentNode.removeChild(w)}
  }
  function finish(){
    if(ended){return}
    ended=true;timers.forEach(clearTimeout);cancelAnimationFrame(raf);
    if(c){c.textContent="100"}
    w.classList.add("flood");
    timers.push(setTimeout(function(){w.classList.add("out");heroIn()},950));
    timers.push(setTimeout(done,1850));
  }
  timers.push(setTimeout(finish,3400));
  var sk=$(".w-skip",w);
  if(sk){sk.addEventListener("click",finish)}
})();

/* header */
var header=$(".site-header");
var heroEl=$(".hero");
function onScroll(){if(header){header.classList.toggle("stuck",window.scrollY>8)}
  var lim=heroEl?heroEl.offsetHeight*0.7:320;document.body.classList.toggle("mbar-on",window.scrollY>lim)}
window.addEventListener("scroll",onScroll,{passive:true});onScroll();
var mb=$(".menu-btn");
function setNav(o){
  document.body.classList.toggle("nav-open",o);
  if(mb){mb.setAttribute("aria-expanded",o?"true":"false");mb.setAttribute("aria-label",o?"Close menu":"Open menu")}
}
if(mb){mb.addEventListener("click",function(){setNav(!document.body.classList.contains("nav-open"))})}
var sc=$(".scrim");if(sc){sc.addEventListener("click",function(){setNav(false)})}
document.addEventListener("keydown",function(e){if(e.key==="Escape"){setNav(false)}});
$$(".nav a").forEach(function(a){a.addEventListener("click",function(){if(!a.closest(".has-sub")||a.classList.contains("sl")){setNav(false)}})});
$$(".subbtn").forEach(function(b){b.addEventListener("click",function(){
  var li=b.closest(".has-sub");var o=!li.classList.contains("open");
  li.classList.toggle("open",o);b.setAttribute("aria-expanded",o?"true":"false")})});
window.addEventListener("resize",function(){if(window.innerWidth>=1100){setNav(false)}});
$$(".nav-cta,.head-cta").forEach(function(b){b.addEventListener("click",function(){setNav(false)})});

/* reveal */
html.classList.add("js");
var rv=$$(".reveal");
if("IntersectionObserver" in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.12,rootMargin:"0px 0px -40px 0px"});
  rv.forEach(function(el){io.observe(el)});
}else{rv.forEach(function(el){el.classList.add("in")})}

/* hero rotation */
var slides=$$(".hero-slides .s"),hls=$$(".hl-box .hl");
if(slides.length>1||hls.length>1){
  var i=0;
  setInterval(function(){
    if(slides.length){slides[i%slides.length].classList.remove("on")}
    if(hls.length){hls[i%hls.length].classList.remove("on")}
    i++;
    if(slides.length){slides[i%slides.length].classList.add("on")}
    if(hls.length){hls[i%hls.length].classList.add("on")}
  },5200);
}

/* WhatsApp enquiry */
function branchBy(slug){for(var k=0;k<GD.branches.length;k++){if(GD.branches[k].slug===slug){return GD.branches[k]}}return GD.branches[0]}
function fmt(d){if(!d){return ""}var p=d.split("-");return p.length===3?p[2]+"/"+p[1]+"/"+p[0]:d}
function waUrl(d){
  var b=branchBy(d.lodge);
  var num=b&&b.wa?b.wa:GD.main_wa;
  var lines=["Hello Golden Days "+(b?b.name:"")+"!","I would like to enquire about a room."];
  if(d.cin){lines.push("Check-in: "+fmt(d.cin))}
  if(d.cout){lines.push("Check-out: "+fmt(d.cout))}
  if(d.guests){lines.push("Guests: "+d.guests)}
  if(d.name){lines.push("Name: "+d.name)}
  if(b&&!b.wa){lines.push("(Sent to the main line because the "+b.name+" number is not listed.)")}
  return "https://wa.me/"+num+"?text="+encodeURIComponent(lines.join("\n"));
}
var today=new Date().toISOString().slice(0,10);
$$('input[type="date"]').forEach(function(x){x.min=today});
function wireDates(form){
  var a=$('[name="cin"]',form),b=$('[name="cout"]',form);
  if(a&&b){a.addEventListener("change",function(){b.min=a.value||today;if(b.value&&b.value<a.value){b.value=""}})}
}
function readForm(form){
  var d={};$$("input,select",form).forEach(function(el){if(el.name){d[el.name]=el.value}});return d;
}
$$("form.enq,form.hero-bar").forEach(function(f){
  wireDates(f);
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var d=readForm(f);
    window.open(waUrl(d),"_blank","noopener");
    var dl=f.closest("dialog");if(dl&&dl.close){dl.close()}
  });
});
var dlg=$("#enqDlg");
function openEnq(slug){
  if(!dlg){return}
  var s=$('select[name="lodge"]',dlg);if(s&&slug){s.value=slug}
  if(dlg.showModal){dlg.showModal()}else{dlg.setAttribute("open","")}
}
$$("[data-enquire]").forEach(function(b){b.addEventListener("click",function(e){e.preventDefault();setNav(false);openEnq(b.getAttribute("data-enquire"))})});
$$("dialog").forEach(function(d){
  d.addEventListener("click",function(e){if(e.target===d){d.close()}});
  $$("[data-close]",d).forEach(function(c){c.addEventListener("click",function(){d.close()})});
});


/* branch finder */
var tb=$$(".town");
tb.forEach(function(b){b.addEventListener("click",function(){
  var t=b.getAttribute("data-town");
  tb.forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});
  $$(".town-panel").forEach(function(p){p.hidden=p.getAttribute("data-panel")!==t});
  var h=$(".town-hint");if(h){h.hidden=true}
})});

/* room compare */
var pick=$("#cmpPick"),out=$("#cmpOut");
if(pick&&out&&GD.rooms){
  var groups={};GD.rooms.forEach(function(r,i){r.i=i;(groups[r.slug]=groups[r.slug]||[]).push(r)});
  var h="";
  GD.branches.forEach(function(b){
    h+='<div class="cmp-grp"><h3>'+b.name+'</h3>';
    (groups[b.slug]||[]).forEach(function(r){
      h+='<label><input type="checkbox" value="'+r.i+'"><span>'+r.name+'</span><span class="p">'+r.price+'</span></label>';
    });
    h+='</div>';
  });
  pick.innerHTML=h;
  var boxes=$$("input",pick);
  function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;")}
  function render(){
    var sel=boxes.filter(function(x){return x.checked}).map(function(x){return GD.rooms[+x.value]});
    boxes.forEach(function(x){x.disabled=!x.checked&&sel.length>=3});
    if(!sel.length){out.className="cmp-out";out.innerHTML='<p class="note">Select two or three rooms to compare them here.</p>';return}
    out.className="cmp-out n"+sel.length;
    out.innerHTML=sel.map(function(r){
      return '<div class="cmp-card"><div class="lodge">'+esc(r.lodge)+'</div><h3>'+esc(r.name)+'</h3><div class="price">'+esc(r.price)+'</div><ul>'+GD.included.map(function(x){return '<li>'+esc(x)+'</li>'}).join("")+(r.note?'<li>'+esc(r.note)+'</li>':'')+'</ul><button class="btn btn-primary btn-sm" type="button" data-enquire="'+r.slug+'">Enquire</button></div>';
    }).join("");
    $$("[data-enquire]",out).forEach(function(b){b.addEventListener("click",function(){openEnq(b.getAttribute("data-enquire"))})});
  }
  boxes.forEach(function(x){x.addEventListener("change",render)});
}

/* gallery filter + lightbox */
var items=$$(".gal button");
$$(".filters button").forEach(function(b){b.addEventListener("click",function(){
  $$(".filters button").forEach(function(x){x.classList.remove("on");x.setAttribute("aria-pressed","false")});
  b.classList.add("on");b.setAttribute("aria-pressed","true");
  var f=b.getAttribute("data-f");
  items.forEach(function(it){it.hidden=!(f==="all"||it.getAttribute("data-tag")===f)});
})});
var lb=$("#lbDlg"),cur=0,vis=[];
function show(n){
  vis=items.filter(function(x){return !x.hidden});if(!vis.length){return}
  cur=(n+vis.length)%vis.length;
  var it=vis[cur];$("img",lb).src=it.getAttribute("data-full");$("img",lb).alt=it.getAttribute("data-alt");
  $("figcaption",lb).textContent=it.getAttribute("data-cap");
}
items.forEach(function(it){it.addEventListener("click",function(){
  vis=items.filter(function(x){return !x.hidden});show(vis.indexOf(it));
  if(lb.showModal){lb.showModal()}else{lb.setAttribute("open","")}
})});
if(lb){
  $(".nx",lb).addEventListener("click",function(){show(cur+1)});
  $(".pv",lb).addEventListener("click",function(){show(cur-1)});
  lb.addEventListener("keydown",function(e){if(e.key==="ArrowRight"){show(cur+1)}if(e.key==="ArrowLeft"){show(cur-1)}});
}

/* contact form -> mailto */
var cf=$("#contactForm");
if(cf){
  cf.addEventListener("submit",function(e){
    e.preventDefault();
    var ok=true;
    $$(".field",cf).forEach(function(f){
      var i=$("input,textarea",f),er=$(".err",f);if(!i||!er){return}
      er.textContent="";
      if(i.required&&!i.value.trim()){er.textContent="Please fill this in.";ok=false}
      else if(i.type==="email"&&i.value&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value)){er.textContent="Please enter a valid email.";ok=false}
    });
    if($(".hp",cf).value){return}
    if(!ok){return}
    var b=branchBy($("#cb",cf).value);
    var body="Name: "+$("#cn",cf).value+"\nEmail: "+$("#ce",cf).value+"\nPhone: "+$("#cp",cf).value+"\nLodge: "+b.name+"\n\n"+$("#cm",cf).value;
    window.location.href="mailto:"+GD.email+"?subject="+encodeURIComponent("Website enquiry: "+b.name)+"&body="+encodeURIComponent(body);
    $("#cs",cf).textContent="Opening your email app with your message ready to send. For the fastest reply, use WhatsApp.";
  });
  var wa=$("#cwa");
  if(wa){wa.addEventListener("click",function(e){
    e.preventDefault();var b=branchBy($("#cb",cf).value);
    var t="Hello Golden Days "+b.name+"! "+($("#cm",cf).value||"I would like to make an enquiry.");
    window.open("https://wa.me/"+(b.wa||GD.main_wa)+"?text="+encodeURIComponent(t),"_blank","noopener");
  })}
}
})();

const menuBtn=document.getElementById('menuBtn');
const navLinks=document.getElementById('navLinks');
if(menuBtn&&navLinks){menuBtn.addEventListener('click',()=>navLinks.classList.toggle('open'));navLinks.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>navLinks.classList.remove('open')))}
const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');revealObserver.unobserve(entry.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>revealObserver.observe(el));
const form=document.getElementById('bookingForm');
if(form){form.addEventListener('submit',async e=>{e.preventDefault();const message=document.getElementById('formMessage');const data=Object.fromEntries(new FormData(form).entries());const csrf=form.querySelector('[name=csrfmiddlewaretoken]').value;const submit=form.querySelector('[type="submit"]');if(submit){submit.disabled=true;submit.dataset.originalText=submit.innerHTML;submit.innerHTML='Sending request…';}try{const phone=String(data.phone||'').replace(/[\s()+-]/g,'');if(!/^(?:91)?[6-9]\d{9}$/.test(phone))throw new Error('Enter a valid 10-digit Indian mobile number.');if(data.ride_date){const chosen=new Date(data.ride_date+'T00:00:00');const today=new Date();today.setHours(0,0,0,0);if(Number.isNaN(chosen.getTime())||chosen<today)throw new Error('Ride date cannot be in the past.');}const response=await fetch('/book/',{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrf},body:JSON.stringify(data)});const result=await response.json();if(!response.ok||!result.ok)throw new Error(result.message||'Unable to submit right now.');form.reset();if(message)message.textContent='';document.querySelector('#bookingModal .booking-modal-close')?.click();const success=document.getElementById('bookingSuccess');const ref=document.getElementById('successReference');if(ref){const match=result.message.match(/NTTS-\d+/);ref.textContent=match?'Booking reference · '+match[0]:'';}const trackLink=document.getElementById('trackBookingLink');if(trackLink){const match=result.reference || (result.message.match(/NTTS-\\d+/)||[])[0];trackLink.href='/track-booking/'+(match?'?reference='+encodeURIComponent(match):'');}const whatsappLink=document.getElementById('whatsappOwnerLink');if(whatsappLink){if(result.whatsapp_url){whatsappLink.href=result.whatsapp_url;whatsappLink.hidden=false;}else{whatsappLink.hidden=true;}}if(success){success.classList.add('open');success.setAttribute('aria-hidden','false');document.body.classList.add('modal-lock');success.querySelector('.success-done')?.focus();}else if(message){message.textContent=result.message;message.style.color='#10844f';}}catch(error){if(message){message.textContent=error.message||'Unable to submit right now. Please try again.';message.style.color='#b42318';}}finally{if(submit){submit.disabled=false;submit.innerHTML=submit.dataset.originalText||'Book Instantly →';}}})}

// Booking modal: keep the original Django booking form and submit endpoint.
(() => {
  const modal = document.getElementById('bookingModal');
  const slot = modal?.querySelector('.modal-form-slot');
  const originalCard = document.querySelector('#booking');
  if (!modal || !slot || !originalCard) return;
  const form = originalCard.querySelector('form');
  const originalParent = originalCard.parentNode;
  const originalNext = originalCard.nextSibling;
  const openers = document.querySelectorAll('.js-open-booking, .js-book-vehicle');
  const close = () => {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-lock');
    if (originalNext) originalParent.insertBefore(originalCard, originalNext);
    else originalParent.appendChild(originalCard);
  };
  const open = (vehicleName) => {
    slot.appendChild(originalCard);
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-lock');
    if (vehicleName) {
      const select = form.querySelector('[name="vehicle_id"]');
      if (select) {
        const option = [...select.options].find(o => o.text.toLowerCase().includes(vehicleName.toLowerCase()));
        if (option) select.value = option.value;
      }
    }
    modal.querySelector('.booking-modal-close')?.focus();
  };
  openers.forEach(el => el.addEventListener('click', e => {
    e.preventDefault();
    open(el.dataset.vehicle || '');
  }));
  modal.querySelectorAll('[data-close-booking]').forEach(el => el.addEventListener('click', close));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && modal.classList.contains('open')) close(); });
})();


// Interactive CMS-driven fleet carousel: tabs, arrows, dots and keyboard-friendly controls.
(() => {
  const slides=[...document.querySelectorAll('[data-fleet-slide]')];
  if(!slides.length) return;
  const tabs=[...document.querySelectorAll('.fleet-tab')];
  const dots=[...document.querySelectorAll('.fleet-dot')];
  let active=0;
  const show=(index)=>{
    active=(index+slides.length)%slides.length;
    slides.forEach((el,i)=>{el.classList.toggle('active',i===active);el.setAttribute('aria-hidden',i===active?'false':'true')});
    tabs.forEach((el,i)=>{el.classList.toggle('selected',i===active);el.setAttribute('aria-selected',i===active?'true':'false')});
    dots.forEach((el,i)=>el.classList.toggle('active',i===active));
  };
  tabs.forEach((el,i)=>el.addEventListener('click',()=>show(i)));
  dots.forEach((el,i)=>el.addEventListener('click',()=>show(i)));
  document.getElementById('fleetPrev')?.addEventListener('click',()=>show(active-1));
  document.getElementById('fleetNext')?.addEventListener('click',()=>show(active+1));
  const region=document.querySelector('.fleet-carousel');
  region?.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(active-1);if(e.key==='ArrowRight')show(active+1)});
  show(0);
})();

// Subtle sticky header state without layout shifts.
(() => {const header=document.querySelector('.site-nav');if(!header)return;const update=()=>header.classList.toggle('scrolled',window.scrollY>12);window.addEventListener('scroll',update,{passive:true});update()})();


// Figma-style booking confirmation overlay.
(() => {const modal=document.getElementById('bookingSuccess');if(!modal)return;const close=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.classList.remove('modal-lock')};modal.querySelectorAll('[data-close-success]').forEach(el=>el.addEventListener('click',close));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&modal.classList.contains('open'))close()});})();


// Single source of truth for navbar active state: click, direct hash load and manual scroll.
(() => {
  const nav = document.getElementById('navLinks');
  if (!nav) return;
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const pairs = links.map(link => ({link, section: document.querySelector(link.getAttribute('href'))})).filter(x => x.section);
  if (!pairs.length) return;
  const activate = link => links.forEach(a => {
    const active = a === link;
    a.classList.toggle('active', active);
    if (active) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });
  const update = () => {
    const header = document.querySelector('.site-nav');
    const marker = (header?.getBoundingClientRect().bottom || 0) + 28;
    let current = pairs[0];
    for (const item of pairs) {
      if (item.section.getBoundingClientRect().top <= marker) current = item;
    }
    activate(current.link);
  };
  links.forEach(link => link.addEventListener('click', () => {
    activate(link);
    nav.classList.remove('open');
  }));
  window.addEventListener('scroll', update, {passive:true});
  window.addEventListener('resize', update, {passive:true});
  window.addEventListener('hashchange', () => {
    const target = links.find(a => a.getAttribute('href') === location.hash);
    if (target) activate(target);
    requestAnimationFrame(update);
  });
  window.addEventListener('load', update);
  if (location.hash) {
    const target = links.find(a => a.getAttribute('href') === location.hash);
    if (target) activate(target);
  }
  requestAnimationFrame(update);
})();

// Only the pricing card selected by the visitor receives the active highlight.
(() => {
  const cards = [...document.querySelectorAll('.price-card')];
  cards.forEach(card => {
    const action = card.querySelector('a');
    if (!action) return;
    action.addEventListener('click', () => {
      cards.forEach(item => item.classList.toggle('is-selected', item === card));
    });
  });
})();

// Reveal important cards as they enter the viewport.
(() => {
  if (!('IntersectionObserver' in window)) return;
  const items = document.querySelectorAll('.price-card,.step-card,.review-card,.safety-grid article,.dispatch-strip');
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
  }), {threshold:.12});
  items.forEach(item => observer.observe(item));
})();


// Pricing cards: selected card only is persistently highlighted; hover is not selection.
(() => {
 const cards=[...document.querySelectorAll('.price-card')];
 cards.forEach(card=>{const action=card.querySelector('a');if(!action)return;action.addEventListener('click',()=>{cards.forEach(c=>c.classList.toggle('is-selected',c===card));});});
})();

// Premium scroll reveals and staggered entrance for the main content blocks.
(() => {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  const targets = document.querySelectorAll(
    '.hero-content,.booking-card,.fleet-motion,.stats-row article,.section-heading,.vehicle-card,.step-card,.price-card,.safety-grid article,.review-card,.download-section,.builder-block'
  );
  if (!targets.length) return;
  document.documentElement.classList.add('ntts-motion-ready');
  targets.forEach((el, index) => {
    el.classList.add('ntts-reveal');
    const sibling = el.parentElement ? [...el.parentElement.children].filter(child => child.matches('.vehicle-card,.step-card,.price-card,.review-card,.safety-grid article,.stats-row article')) : [];
    const order = sibling.indexOf(el);
    if (order >= 0) el.classList.add(`ntts-delay-${Math.min(order + 1, 3)}`);
  });
  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('ntts-in'));
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('ntts-in');
      observer.unobserve(entry.target);
    });
  }, {threshold:.10, rootMargin:'0px 0px -35px 0px'});
  targets.forEach(el => observer.observe(el));
})();

// Add a restrained pointer tilt to desktop cards only; disabled on touch devices.
(() => {
  if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('.vehicle-card,.price-card,.review-card').forEach(card => {
    card.addEventListener('pointermove', event => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      card.style.setProperty('--ntts-pointer-x', `${(x * 3).toFixed(2)}deg`);
      card.style.setProperty('--ntts-pointer-y', `${(-y * 2).toFixed(2)}deg`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.removeProperty('--ntts-pointer-x');
      card.style.removeProperty('--ntts-pointer-y');
    });
  });
})();

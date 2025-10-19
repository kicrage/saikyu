document.addEventListener('DOMContentLoaded', function(){
    // set year in footer
    const yearSpan = document.getElementById('year');
    if(yearSpan) yearSpan.textContent = new Date().getFullYear();

    // mobile menu toggle (if present)
    (function(){
        const menuToggle = document.getElementById('menuToggle');
        const mainNav = document.getElementById('main-nav');
        if(!menuToggle || !mainNav) return;
        menuToggle.addEventListener('click', function(){
            const expanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', String(!expanded));
            const hidden = mainNav.getAttribute('aria-hidden') === 'true';
            mainNav.setAttribute('aria-hidden', String(!hidden));
        });
        // initialize
        mainNav.setAttribute('aria-hidden', 'true');
    })();

    // mark current nav link as active for UX
    (function(){
        try{
            const nav = document.getElementById('main-nav');
            if(!nav) return;
            const links = nav.querySelectorAll('a');
            const path = location.pathname.split('/').pop() || 'index.html';
            links.forEach(a => {
                // normalize href to filename only
                const href = (a.getAttribute('href') || '').split('/').pop();
                if(href === path || (href === 'index.html' && path === '')){
                    a.classList.add('active');
                    a.setAttribute('aria-current', 'page');
                } else {
                    a.classList.remove('active');
                    if(a.getAttribute('aria-current')) a.removeAttribute('aria-current');
                }
            });
        }catch(e){/* ignore */}
    })();

    // sample timetable data
    const sampleData = {
        '中央駅': [
            {time: '08:05', dest: '北町行き'},
            {time: '08:20', dest: '北町行き'},
            {time: '08:35', dest: '南港行き'}
        ],
        '西町駅': [
            {time: '09:00', dest: '中央駅行き'},
            {time: '09:17', dest: '中央駅行き'}
        ]
    };

    const form = document.getElementById('timetableForm');
    const input = document.getElementById('stationInput');
    const results = document.getElementById('results');
    const searchBtn = document.getElementById('searchBtn');

    function renderResults(station){
        results.innerHTML = '';
        if(!station){
            results.textContent = '駅名を入力してください。';
            return;
        }
        const rows = sampleData[station];
        if(!rows){
            results.textContent = 'データが見つかりません。別の駅名を試してください。';
            return;
        }
        const table = document.createElement('table');
        table.className = 'timetable';
        const thead = document.createElement('thead');
        thead.innerHTML = '<tr><th>発車時刻</th><th>行先</th></tr>';
        table.appendChild(thead);
        const tbody = document.createElement('tbody');
        rows.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${r.time}</td><td>${r.dest}</td>`;
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        results.appendChild(table);
    }

    if(form){
        form.addEventListener('submit', function(e){
            e.preventDefault();
            renderResults(input.value.trim());
        });
    }
    if(searchBtn){
        searchBtn.addEventListener('click', function(e){
            e.preventDefault();
            renderResults(input.value.trim());
        });
    }

    // contact form removed — Discord widget is used instead

    // NEWS: load posts list when on news.html
    (function(){
        try{
            const newsList = document.getElementById('news-list');
            if(!newsList) return;
            fetch('posts/posts.json')
                .then(r => {
                    if(!r.ok) throw new Error('network');
                    return r.json();
                })
                .then(posts => {
                    newsList.innerHTML = '';
                    if(!posts || posts.length === 0){
                        newsList.textContent = 'まだお知らせはありません。';
                        return;
                    }
                    const ul = document.createElement('ul');
                    ul.className = 'news-ul';
                    posts.forEach(p => {
                        const li = document.createElement('li');
                        const a = document.createElement('a');
                        a.href = p.path;
                        a.textContent = `${p.date} — ${p.title}`;
                        a.title = p.summary || p.title;
                        li.appendChild(a);
                        const summary = document.createElement('p');
                        summary.className = 'news-summary';
                        summary.textContent = p.summary || '';
                        li.appendChild(summary);
                        ul.appendChild(li);
                    });
                    newsList.appendChild(ul);
                })
                .catch(err => {
                    newsList.textContent = 'お知らせの読み込みに失敗しました。';
                    console.warn('news load error', err);
                });
        }catch(e){/* ignore */}
    })();

});

/* ============================================================
   典藏 · 图书管理系统 —— 前端交互
   三种身份各自拥有按“业务流程顺序”排列的工作台。
   ============================================================ */
(function () {
  'use strict';

  const API = window.LibraryAPI;

  /* ---------------- 常量与标签映射 ---------------- */
  const READER_TYPES = {
    UNDERGRADUATE: '本科生', JUNIOR_COLLEGE: '专科生', GRADUATE: '研究生',
    DOCTOR: '博士生', TEACHER: '教师',
  };
  const ITEM_TYPES = {
    CHINESE_BOOK: '中文图书', FOREIGN_BOOK: '外文图书', CHINESE_MAGAZINE: '中文杂志',
    FOREIGN_MAGAZINE: '外文杂志', THESIS: '论文',
  };

  /* ---------------- SVG 图标 ---------------- */
  function svg(inner, size) {
    const s = size || 20;
    return `<svg viewBox="0 0 24 24" width="${s}" height="${s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;
  }
  const ICONS = {
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    bookOpen: '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    search: '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
    list: '<path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/>',
    bookmark: '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
    userPlus: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6"/><path d="M22 11h-6"/>',
    swap: '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    rotate: '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    card: '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    settings: '<path d="M4 21v-7"/><path d="M4 10V3"/><path d="M12 21v-9"/><path d="M12 8V3"/><path d="M20 21v-5"/><path d="M20 12V3"/><path d="M1 14h6"/><path d="M9 8h6"/><path d="M17 16h6"/>',
    plus: '<path d="M12 5v14"/><path d="M5 12h14"/>',
    trash: '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M10 11v6"/><path d="M14 11v6"/>',
    check: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
    info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  };
  function icon(name, size) { return svg(ICONS[name] || ICONS.info, size); }

  /* ---------------- 工具函数 ---------------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
  }
  function fmtDate(s) { return s ? String(s).slice(0, 10) : '—'; }
  function fmtDT(s) { return s ? String(s).slice(0, 16).replace('T', ' ') : '—'; }
  function today() { return new Date().toISOString().slice(0, 10); }
  function badge(text, tone) {
    return `<span class="badge b-${tone}"><span class="dot"></span>${esc(text)}</span>`;
  }
  function empty(msg) { return `<div class="empty">${icon('info', 26)}<div>${esc(msg)}</div></div>`; }

  function toast(msg, tone) {
    const root = document.getElementById('toasts');
    const t = document.createElement('div');
    t.className = `toast toast-${tone || 'info'}`;
    t.setAttribute('role', 'status');
    t.innerHTML = `${icon(tone === 'error' ? 'alert' : tone === 'success' ? 'check' : 'info', 18)}<span>${esc(msg)}</span>`;
    root.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 260); }, 3600);
  }

  /* ---------------- 状态 ---------------- */
  const state = {
    role: localStorage.getItem('lib.role') || 'reader',
    uid: 0,   // 内部读者 id（由借阅证号解析而来，不对读者展示）
    cardNo: localStorage.getItem('lib.cardNo') || '',
    readerName: '',
    view: null,
  };

  /* 每个身份的工作流程（顺序即业务顺序） */
  const ROLES = {
    reader: {
      label: '读者', hint: '查询藏书、预约图书、查看我的借阅',
      icon: 'bookOpen', desc: '面向读者的自助服务台',
      views: [
        { id: 'catalog', label: '查询图书', hint: '第一步 · 检索馆藏', icon: 'search' },
        { id: 'loans', label: '我的借阅', hint: '第二步 · 借阅与超期', icon: 'list' },
        { id: 'reservations', label: '我的预约', hint: '第三步 · 预约队列', icon: 'bookmark' },
        { id: 'register', label: '注册账号', hint: '新读者登记', icon: 'userPlus' },
      ],
    },
    librarian: {
      label: '图书管理员', hint: '代办借书、还书与借阅查询',
      icon: 'swap', desc: '借阅台工作台',
      views: [
        { id: 'borrow', label: '办理借书', hint: '第一步 · 读者交证交书', icon: 'swap' },
        { id: 'return', label: '办理还书', hint: '第二步 · 读者还书', icon: 'rotate' },
        { id: 'query', label: '读者借阅查询', hint: '第三步 · 查询任意读者', icon: 'users' },
      ],
    },
    admin: {
      label: '系统管理员', hint: '维护借阅证、图书、人员与规则',
      icon: 'shield', desc: '系统维护控制台',
      views: [
        { id: 'cards', label: '借阅证管理', hint: '办理与注销借阅证', icon: 'card' },
        { id: 'catalog', label: '图书与馆藏', hint: '标题与副本维护', icon: 'book' },
        { id: 'staff', label: '人员管理', hint: '管理员账号维护', icon: 'users' },
        { id: 'rules', label: '规则管理', hint: '借阅与罚款规则', icon: 'settings' },
      ],
    },
  };

  const $ = (id) => document.getElementById(id);

  /* ---------------- 视图骨架与挂载 ---------------- */
  const VIEWS = {
    /* ===== 读者 ===== */
    'reader:catalog': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第一步：检索馆藏，找到想借的书后可直接“预约”。预约图书请在下方填写你的借阅证号。</span></div>
          <div class="card">
            <div class="card-head"><h2>检索馆藏</h2><span class="desc">按书名 / 作者 / ISBN 精确或模糊查询</span></div>
            <form data-form="search" class="form-row">
              <div class="field"><label>书名</label><input id="q-title" type="search" placeholder="如：软件工程"></div>
              <div class="field"><label>作者</label><input id="q-author" type="search" placeholder="如：张海藩"></div>
              <div class="field"><label>ISBN</label><input id="q-isbn" type="search" placeholder="精确匹配"></div>
              <button class="btn btn-primary" type="submit">${icon('search')}查询</button>
              <button class="btn btn-ghost" type="button" data-action="search-reset">重置</button>
            </form>
          </div>
          <div class="card" style="margin-top:18px">
            <div class="card-head"><h2>馆藏列表</h2><span class="desc" id="book-count"></span></div>
            <div id="book-grid" class="book-grid stagger"></div>
          </div>`;
      },
      async mount() {
        const q = {};
        ['q-title', 'q-author', 'q-isbn'].forEach((id) => { const v = $(id)?.value.trim(); if (v) q[id.slice(2)] = v; });
        const grid = $('book-grid');
        grid.innerHTML = `<div class="empty">${icon('clock', 26)}<div>正在加载…</div></div>`;
        try {
          const p = new URLSearchParams();
          if (q.title) p.set('title', q.title);
          if (q.author) p.set('author', q.author);
          if (q.isbn) p.set('isbn', q.isbn);
          const books = await API.get('/api/catalog/books?' + p.toString());
          $('book-count').textContent = `共 ${books.length} 条`;
          if (!books.length) { grid.innerHTML = empty('没有找到匹配的图书，试试放宽条件。'); return; }
          grid.innerHTML = books.map((b) => {
            const stock = b.available_count > 0
              ? `<span class="stock">在库 <span class="n">${b.available_count}</span> / ${b.total_count}</span>`
              : `<span class="stock" style="color:var(--red)">已全部借出</span>`;
            const canReserve = b.available_count > 0 && state.uid > 0;
            return `
              <div class="book-card">
                <div class="bc-type">${esc(ITEM_TYPES[b.item_type] || b.item_type)}</div>
                <div class="bc-title">${esc(b.title)}</div>
                <div class="bc-author">${esc(b.author)}</div>
                <div class="bc-meta">${esc(b.publisher || '')} · ISBN ${esc(b.isbn)}</div>
                <div class="bc-foot">
                  ${stock}
                  <button class="btn btn-sm ${canReserve ? 'btn-primary' : 'btn-ghost'}"
                    data-action="reserve" data-title-id="${b.id}" data-title-name="${esc(b.title)}"
                    ${canReserve ? '' : 'title="请先填写借阅证号或图书已借出"'}>${icon('bookmark', 15)}预约</button>
                </div>
              </div>`;
          }).join('');
        } catch (e) { grid.innerHTML = empty(e.message); }
      },
    },

    'reader:loans': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第二步：查看你的当前借阅与历史记录，超期图书会以红色标注。</span></div>
          <div class="card">
            <div class="card-head"><h2>我的借阅</h2><button class="btn btn-ghost btn-sm" data-action="refresh">${icon('rotate', 15)}刷新</button></div>
            <div id="loans-box"></div>
          </div>`;
      },
      async mount() {
        const box = $('loans-box');
        if (!state.uid) { box.innerHTML = empty('请先在上方填写你的「借阅证号」，再查看借阅信息。'); return; }
        box.innerHTML = `<div class="empty">正在加载…</div>`;
        try {
          const list = await API.get(`/api/readers/${state.uid}/loans`);
          if (!list.length) { box.innerHTML = empty('当前没有任何借阅记录。'); return; }
          const active = list.filter((l) => l.status === 'BORROWED').length;
          box.innerHTML = `
            <div class="stat-row" style="margin-bottom:14px">
              <div class="stat"><div class="s-label">当前借阅</div><div class="s-value">${active}</div></div>
              <div class="stat"><div class="s-label">历史记录</div><div class="s-value">${list.length - active}</div></div>
              <div class="stat"><div class="s-label">已超期</div><div class="s-value">${list.filter(isOverdue).length}</div></div>
            </div>
            <div class="table-wrap"><table>
              <thead><tr><th>书名</th><th>作者</th><th>条码</th><th>借出时间</th><th>应还日期</th><th>状态</th></tr></thead>
              <tbody>${list.map((l) => `
                <tr>
                  <td>${esc(l.title)}</td>
                  <td>${esc(l.author)}</td>
                  <td class="mono">${esc(l.barcode)}</td>
                  <td class="mono">${fmtDT(l.borrowed_at)}</td>
                  <td class="mono">${fmtDate(l.due_date)}</td>
                  <td>${loanBadge(l)}</td>
                </tr>`).join('')}</tbody>
            </table></div>`;
        } catch (e) { box.innerHTML = empty(e.message); }
      },
    },

    'reader:reservations': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第三步：查看你的预约队列，预约按创建时间先后排序。</span></div>
          <div class="card">
            <div class="card-head"><h2>我的预约</h2><button class="btn btn-ghost btn-sm" data-action="refresh">${icon('rotate', 15)}刷新</button></div>
            <div id="resv-box"></div>
          </div>`;
      },
      async mount() {
        const box = $('resv-box');
        if (!state.uid) { box.innerHTML = empty('请先在上方填写你的「借阅证号」，再查看预约信息。'); return; }
        box.innerHTML = `<div class="empty">正在加载…</div>`;
        try {
          const list = await API.get(`/api/readers/${state.uid}/reservations`);
          if (!list.length) { box.innerHTML = empty('你还没有预约任何图书。'); return; }
          box.innerHTML = `<div class="table-wrap"><table>
            <thead><tr><th>书名</th><th>作者</th><th>类型</th><th>状态</th><th>预约时间</th></tr></thead>
            <tbody>${list.map((r) => `
              <tr>
                <td>${esc(r.book_title)}</td>
                <td>${esc(r.author)}</td>
                <td>${esc(ITEM_TYPES[r.item_type] || r.item_type)}</td>
                <td>${resvBadge(r.status)}</td>
                <td class="mono">${fmtDT(r.created_at)}</td>
              </tr>`).join('')}</tbody>
          </table></div>`;
        } catch (e) { box.innerHTML = empty(e.message); }
      },
    },

    'reader:register': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>注册后请到馆员处领取借阅证，之后用借阅证号查询借阅与预约。</span></div>
          <div class="card" style="max-width:620px">
            <div class="card-head"><h2>注册读者账号</h2></div>
            <form data-form="register">
              <div class="form-grid">
                <div class="field"><label>姓名 <span class="req">*</span></label><input id="r-name" required placeholder="张三"></div>
                <div class="field"><label>院系 <span class="req">*</span></label><input id="r-dept" required placeholder="计算机学院"></div>
                <div class="field"><label>读者类型 <span class="req">*</span></label>
                  <select id="r-type">${Object.entries(READER_TYPES).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select>
                </div>
                <div class="field"><label>邮箱</label><input id="r-email" type="email" placeholder="可选"></div>
                <div class="field"><label>电话</label><input id="r-phone" placeholder="可选"></div>
              </div>
              <div id="register-result"></div>
              <button class="btn btn-primary btn-lg" type="submit" style="margin-top:16px">${icon('userPlus')}注册</button>
            </form>
          </div>`;
      },
      async mount() {},
    },

    /* ===== 图书管理员 ===== */
    'librarian:borrow': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第一步：读者把借阅证与图书交给管理员。输入借阅证号与馆藏条码即可办理借出（示例：证号 CARD2026000001，条码 BC-1001）。</span></div>
          <div class="card" style="max-width:620px">
            <div class="card-head"><h2>办理借书</h2></div>
            <form data-form="borrow">
              <div class="field"><label>借阅证号 <span class="req">*</span></label><input id="b-card" required placeholder="如：1"></div>
              <div class="field"><label>馆藏条码 <span class="req">*</span></label><input id="b-barcode" required placeholder="如：BC-1001"></div>
              <div id="borrow-result"></div>
              <button class="btn btn-primary btn-lg" type="submit" style="margin-top:6px">${icon('swap')}确认借出</button>
            </form>
          </div>`;
      },
      async mount() {},
    },

    'librarian:return': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第二步：读者归还图书。输入馆藏条码即可办理还书，超期会自动计算罚款。</span></div>
          <div class="card" style="max-width:620px">
            <div class="card-head"><h2>办理还书</h2></div>
            <form data-form="return">
              <div class="field"><label>馆藏条码 <span class="req">*</span></label><input id="rt-barcode" required placeholder="如：BC-1001"></div>
              <div id="return-result"></div>
              <button class="btn btn-primary btn-lg" type="submit" style="margin-top:6px">${icon('rotate')}确认归还</button>
            </form>
          </div>`;
      },
      async mount() {},
    },

    'librarian:query': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>第三步：查询任意读者的借阅信息（当前借阅、历史与超期）。</span></div>
          <div class="card">
            <div class="card-head"><h2>读者借阅查询</h2></div>
            <form data-form="query-loans" class="form-row">
              <div class="field" style="max-width:320px"><label>选择读者</label><select id="q-reader" required><option value="">加载中…</option></select></div>
              <button class="btn btn-primary" type="submit">${icon('search')}查询</button>
            </form>
            <div id="query-result" style="margin-top:18px"></div>
          </div>`;
      },
      async mount() {
        const sel = $('q-reader');
        try {
          const readers = await API.get('/api/readers');
          if (!readers.length) { sel.innerHTML = '<option value="">暂无读者</option>'; return; }
          sel.innerHTML = '<option value="">— 请选择 —</option>' + readers.map((r) =>
            `<option value="${r.id}">#${r.id} ${esc(r.name)} · ${esc(r.department)}（${READER_TYPES[r.reader_type] || r.reader_type}）</option>`).join('');
        } catch (e) { sel.innerHTML = '<option value="">加载失败</option>'; toast(e.message, 'error'); }
      },
    },

    /* ===== 系统管理员 ===== */
    'admin:cards': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>为读者办理借阅证，或注销已有借阅证。同一读者只能持有一张有效借阅证。</span></div>
          <div class="card">
            <div class="card-head"><h2>读者列表 · 办理借阅证</h2><button class="btn btn-ghost btn-sm" data-action="refresh">${icon('rotate', 15)}刷新</button></div>
            <div id="readers-box"></div>
          </div>
          <div class="card">
            <div class="card-head"><h2>已发放借阅证</h2></div>
            <div id="cards-box"></div>
          </div>`;
      },
      async mount() {
        await Promise.all([loadReaders(), loadCards()]);
      },
    },

    'admin:catalog': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>维护图书标题与馆藏副本：新增标题 → 为标题添加副本 → 必要时移除副本或删除标题。</span></div>
          <div class="card">
            <div class="card-head"><h2>新增图书标题</h2></div>
            <form data-form="add-title">
              <div class="form-grid">
                <div class="field"><label>书名 <span class="req">*</span></label><input id="t-title" required></div>
                <div class="field"><label>作者 <span class="req">*</span></label><input id="t-author" required></div>
                <div class="field"><label>ISBN <span class="req">*</span></label><input id="t-isbn" required></div>
                <div class="field"><label>出版社</label><input id="t-publisher"></div>
                <div class="field"><label>类型 <span class="req">*</span></label><select id="t-type">${Object.entries(ITEM_TYPES).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select></div>
              </div>
              <div id="add-title-result"></div>
              <button class="btn btn-primary" type="submit" style="margin-top:14px">${icon('plus')}添加标题</button>
            </form>
          </div>
          <div class="card">
            <div class="card-head"><h2>馆藏副本</h2></div>
            <div class="form-row">
              <form data-form="add-item" class="form-row" style="flex:1">
                <div class="field" style="max-width:360px"><label>所属标题</label><select id="i-title"><option value="">加载中…</option></select></div>
                <div class="field"><label>条码 <span class="req">*</span></label><input id="i-barcode" required placeholder="BC-1001"></div>
                <button class="btn btn-primary" type="submit">${icon('plus')}添加副本</button>
              </form>
              <form data-form="remove-item" class="form-row" style="flex:1">
                <div class="field"><label>移除副本（条码）</label><input id="di-barcode" required placeholder="BC-1001"></div>
                <button class="btn btn-danger-ghost" type="submit">${icon('trash')}移除</button>
              </form>
            </div>
            <div id="add-item-result"></div>
          </div>
          <div class="card">
            <div class="card-head"><h2>全部图书</h2><button class="btn btn-ghost btn-sm" data-action="refresh">${icon('rotate', 15)}刷新</button></div>
            <div id="books-box"></div>
          </div>`;
      },
      async mount() {
        await Promise.all([loadTitleOptions(), loadBooksAdmin()]);
      },
    },

    'admin:staff': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>维护图书管理员与系统管理员账号。</span></div>
          <div class="card">
            <div class="card-head"><h2>图书管理员</h2></div>
            <form data-form="add-librarian" class="form-row">
              <div class="field"><label>姓名 <span class="req">*</span></label><input id="l-name" required></div>
              <button class="btn btn-primary" type="submit">${icon('plus')}添加</button>
            </form>
            <div id="librarians-box" style="margin-top:14px"></div>
          </div>
          <div class="card">
            <div class="card-head"><h2>系统管理员</h2></div>
            <form data-form="add-sysadmin" class="form-row">
              <div class="field"><label>姓名 <span class="req">*</span></label><input id="sa-name" required></div>
              <button class="btn btn-primary" type="submit">${icon('plus')}添加</button>
            </form>
            <div id="sysadmins-box" style="margin-top:14px"></div>
          </div>`;
      },
      async mount() {
        await Promise.all([loadStaff('librarians'), loadStaff('sysadmins')]);
      },
    },

    'admin:rules': {
      skeleton() {
        return `
          <div class="flow-note">${icon('info')}<span>维护各类读者的借阅上限与期限，以及各类借出物的每日罚款额（数据驱动，即时生效）。</span></div>
          <div class="card">
            <div class="card-head"><h2>借阅规则</h2></div>
            <div id="policies-box"></div>
          </div>
          <div class="card">
            <div class="card-head"><h2>罚款规则</h2></div>
            <div id="fines-box"></div>
          </div>`;
      },
      async mount() {
        await Promise.all([loadPolicies(), loadFines()]);
      },
    },
  };

  /* ---------------- 徽章与判定 ---------------- */
  function isOverdue(l) { return l.status === 'BORROWED' && l.due_date < today(); }
  function loanBadge(l) {
    if (l.status === 'RETURNED') return badge('已归还', 'mute');
    if (isOverdue(l)) return badge('已超期', 'red');
    return badge('借出中', 'brass');
  }
  function resvBadge(s) {
    return ({ ACTIVE: badge('预约中', 'green'), FULFILLED: badge('已满足', 'blue'), CANCELLED: badge('已取消', 'mute') })[s] || badge(s, 'mute');
  }
  function cardBadge(s) { return s === 'ACTIVE' ? badge('有效', 'green') : badge('已注销', 'mute'); }

  /* ---------------- 列表加载器（供挂载与局部刷新复用） ---------------- */
  async function loadReaders() {
    const box = $('readers-box'); box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const readers = await API.get('/api/readers');
      if (!readers.length) { box.innerHTML = empty('暂无读者，可先在「读者」身份下注册。'); return; }
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>姓名</th><th>院系</th><th>类型</th><th></th></tr></thead>
        <tbody>${readers.map((r) => `
          <tr><td class="mono">${r.id}</td><td>${esc(r.name)}</td><td>${esc(r.department)}</td>
          <td>${esc(READER_TYPES[r.reader_type] || r.reader_type)}</td>
          <td class="t-actions"><button class="btn btn-sm btn-primary" data-action="issue-card" data-reader-id="${r.id}" data-reader-name="${esc(r.name)}">${icon('card', 15)}办证</button></td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }
  async function loadCards() {
    const box = $('cards-box'); box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const cards = await API.get('/api/admin/borrow-cards');
      if (!cards.length) { box.innerHTML = empty('尚未发放任何借阅证。'); return; }
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>证号</th><th>读者</th><th>院系</th><th>状态</th><th>发放时间</th><th></th></tr></thead>
        <tbody>${cards.map((c) => `
          <tr><td class="mono">${esc(c.card_no)}</td><td>${esc(c.reader_name)}</td><td>${esc(c.department)}</td>
          <td>${cardBadge(c.status)}</td><td class="mono">${fmtDT(c.issued_at)}</td>
          <td class="t-actions">${c.status === 'ACTIVE' ? `<button class="btn btn-sm btn-danger-ghost" data-action="revoke-card" data-card-no="${esc(c.card_no)}">${icon('trash', 15)}注销</button>` : ''}</td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }
  async function loadTitleOptions() {
    const sel = $('i-title');
    try {
      const books = await API.get('/api/catalog/books');
      sel.innerHTML = '<option value="">— 请选择 —</option>' + books.map((b) =>
        `<option value="${b.id}">#${b.id} ${esc(b.title)}（${esc(b.author)}）</option>`).join('');
    } catch (e) { sel.innerHTML = '<option value="">加载失败</option>'; }
  }
  async function loadBooksAdmin() {
    const box = $('books-box'); box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const books = await API.get('/api/catalog/books');
      if (!books.length) { box.innerHTML = empty('暂无图书。'); return; }
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>书名</th><th>作者</th><th>类型</th><th>馆藏</th><th></th></tr></thead>
        <tbody>${books.map((b) => `
          <tr><td class="mono">${b.id}</td><td>${esc(b.title)}</td><td>${esc(b.author)}</td>
          <td>${esc(ITEM_TYPES[b.item_type] || b.item_type)}</td><td class="mono">${b.available_count} / ${b.total_count}</td>
          <td class="t-actions"><button class="btn btn-sm btn-danger-ghost" data-action="delete-title" data-title-id="${b.id}" data-title-name="${esc(b.title)}">${icon('trash', 15)}删除</button></td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }
  async function loadStaff(kind) {
    const box = $((kind === 'librarians' ? 'librarians' : 'sysadmins') + '-box');
    box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const list = await API.get('/api/admin/' + kind);
      if (!list.length) { box.innerHTML = empty('暂无人员。'); return; }
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>姓名</th><th></th></tr></thead>
        <tbody>${list.map((s) => `<tr><td class="mono">${s.id}</td><td>${esc(s.name)}</td>
          <td class="t-actions"><button class="btn btn-sm btn-danger-ghost" data-action="delete-staff" data-kind="${kind}" data-id="${s.id}" data-name="${esc(s.name)}">${icon('trash', 15)}删除</button></td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }
  async function loadPolicies() {
    const box = $('policies-box'); box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const list = await API.get('/api/admin/borrow-policies');
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>读者类型</th><th>借阅上限（本）</th><th>借阅期限（天）</th><th></th></tr></thead>
        <tbody>${list.map((p) => `
          <tr><td>${esc(READER_TYPES[p.reader_type] || p.reader_type)}</td>
          <td><input data-policy-count data-type="${p.reader_type}" type="number" min="0" value="${p.max_borrow_count}" style="width:90px"></td>
          <td><input data-policy-days data-type="${p.reader_type}" type="number" min="0" value="${p.borrow_days}" style="width:90px"></td>
          <td class="t-actions"><button class="btn btn-sm btn-primary" data-action="save-policy" data-type="${p.reader_type}">${icon('check', 15)}保存</button></td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }
  async function loadFines() {
    const box = $('fines-box'); box.innerHTML = `<div class="empty">正在加载…</div>`;
    try {
      const list = await API.get('/api/admin/fine-rules');
      box.innerHTML = `<div class="table-wrap"><table>
        <thead><tr><th>借出物类型</th><th>罚款（元/天）</th><th></th></tr></thead>
        <tbody>${list.map((f) => `
          <tr><td>${esc(ITEM_TYPES[f.item_type] || f.item_type)}</td>
          <td><input data-fine-amt data-type="${f.item_type}" type="number" min="0" step="0.01" value="${f.fine_per_day}" style="width:110px"></td>
          <td class="t-actions"><button class="btn btn-sm btn-primary" data-action="save-fine" data-type="${f.item_type}">${icon('check', 15)}保存</button></td></tr>`).join('')}</tbody>
      </table></div>`;
    } catch (e) { box.innerHTML = empty(e.message); }
  }

  /* ---------------- 结果卡渲染 ---------------- */
  function setResult(id, ok, title, detail) {
    const el = $(id); if (!el) return;
    if (detail == null) { el.innerHTML = ''; return; }
    el.innerHTML = `<div class="result-card ${ok ? 'result-ok' : 'result-err'}" style="margin:14px 0 0">
      ${icon(ok ? 'check' : 'alert')}<div><div class="rk">${esc(title)}</div><div class="rd">${esc(detail)}</div></div></div>`;
  }

  /* ---------------- 动作处理 ---------------- */
  async function handleAction(action, el) {
    switch (action) {
      case 'refresh': await mountView(); break;
      case 'search-reset':
        ['q-title', 'q-author', 'q-isbn'].forEach((id) => { if ($(id)) $(id).value = ''; });
        await mountView(); break;
      case 'reserve': {
        if (state.uid <= 0) { toast('请先在上方填写你的「借阅证号」再预约', 'error'); break; }
        const titleId = el.dataset.titleId, titleName = el.dataset.titleName;
        try {
          await API.post('/api/reservations', { reader_id: state.uid, title_id: Number(titleId) });
          toast(`预约成功：《${titleName}》`, 'success');
        } catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'issue-card': {
        try {
          const card = await API.post('/api/admin/borrow-cards', { reader_id: Number(el.dataset.readerId) });
          toast(`办证成功：证号 ${card.card_no} · ${el.dataset.readerName}`, 'success');
          await loadCards();
        } catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'revoke-card': {
        const no = el.dataset.cardNo;
        if (!confirm(`确定注销借阅证 ${no} 吗？`)) break;
        try { await API.del(`/api/admin/borrow-cards/${encodeURIComponent(no)}`); toast(`已注销借阅证 ${no}`, 'success'); await loadCards(); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'delete-title': {
        const id = el.dataset.titleId;
        if (!confirm(`确定删除图书《${el.dataset.titleName}》吗？`)) break;
        try { await API.del(`/api/admin/book-titles/${id}`); toast('已删除标题', 'success'); await loadBooksAdmin(); await loadTitleOptions(); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'delete-staff': {
        const kind = el.dataset.kind, id = el.dataset.id;
        if (!confirm(`确定删除 ${el.dataset.name} 吗？`)) break;
        try { await API.del(`/api/admin/${kind}/${id}`); toast('已删除', 'success'); await loadStaff(kind); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'save-policy': {
        const type = el.dataset.type;
        const count = document.querySelector(`[data-policy-count][data-type="${type}"]`).value;
        const days = document.querySelector(`[data-policy-days][data-type="${type}"]`).value;
        try { await API.post('/api/admin/borrow-policies', { reader_type: type, max_borrow_count: Number(count), borrow_days: Number(days) }); toast('借阅规则已保存', 'success'); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'save-fine': {
        const type = el.dataset.type;
        const amt = document.querySelector(`[data-fine-amt][data-type="${type}"]`).value;
        try { await API.post('/api/admin/fine-rules', { item_type: type, fine_per_day: parseFloat(amt) }); toast('罚款规则已保存', 'success'); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
    }
  }

  /* ---------------- 表单提交 ---------------- */
  async function handleSubmit(formName) {
    switch (formName) {
      case 'search': { await mountView(); break; }
      case 'register': {
        const body = { name: $('r-name').value.trim(), department: $('r-dept').value.trim(), reader_type: $('r-type').value };
        if ($('r-email').value.trim()) body.email = $('r-email').value.trim();
        if ($('r-phone').value.trim()) body.phone = $('r-phone').value.trim();
        try {
          const r = await API.post('/api/readers', body);
          setResult('register-result', true, '注册成功', `已为 ${r.name} 注册。请到馆员处领取借阅证，之后用借阅证号查询借阅与预约。`);
          toast('注册成功，请到馆员处领取借阅证', 'success');
        } catch (e) { setResult('register-result', false, '注册失败', e.message); }
        break;
      }
      case 'borrow': {
        try {
          const loan = await API.post('/api/circulation/borrow', { card_no: $('b-card').value.trim(), barcode: $('b-barcode').value.trim() });
          setResult('borrow-result', true, '借出成功', `《${loan.title}》（${loan.author}）· 应还日期 ${loan.due_date}`);
          toast(`借出成功：《${loan.title}》`, 'success');
          $('b-barcode').value = '';
        } catch (e) { setResult('borrow-result', false, '借书失败', e.message); }
        break;
      }
      case 'return': {
        try {
          const r = await API.post('/api/circulation/return', { barcode: $('rt-barcode').value.trim() });
          const fine = r.fine ? `，产生罚款 ¥${r.fine.amount.toFixed(2)}（超期 ${r.fine.overdue_days} 天）` : '，无超期';
          setResult('return-result', true, '归还成功', `借阅 #${r.loan_id}${fine}`);
          toast(r.fine ? `还书成功，罚款 ¥${r.fine.amount.toFixed(2)}` : '还书成功', 'success');
          $('rt-barcode').value = '';
        } catch (e) { setResult('return-result', false, '还书失败', e.message); }
        break;
      }
      case 'query-loans': {
        const readerId = $('q-reader').value;
        const box = $('query-result');
        if (!readerId) { box.innerHTML = ''; return; }
        box.innerHTML = `<div class="empty">正在加载…</div>`;
        try {
          const list = await API.get(`/api/readers/${readerId}/loans`);
          if (!list.length) { box.innerHTML = empty('该读者当前没有借阅记录。'); return; }
          box.innerHTML = `<div class="table-wrap"><table>
            <thead><tr><th>书名</th><th>条码</th><th>借出时间</th><th>应还日期</th><th>状态</th></tr></thead>
            <tbody>${list.map((l) => `<tr><td>${esc(l.title)}</td><td class="mono">${esc(l.barcode)}</td>
              <td class="mono">${fmtDT(l.borrowed_at)}</td><td class="mono">${fmtDate(l.due_date)}</td><td>${loanBadge(l)}</td></tr>`).join('')}</tbody>
          </table></div>`;
        } catch (e) { box.innerHTML = empty(e.message); }
        break;
      }
      case 'add-title': {
        const body = { title: $('t-title').value.trim(), author: $('t-author').value.trim(), isbn: $('t-isbn').value.trim(), item_type: $('t-type').value };
        if ($('t-publisher').value.trim()) body.publisher = $('t-publisher').value.trim();
        try {
          await API.post('/api/admin/book-titles', body);
          setResult('add-title-result', true, '添加成功', `《${body.title}》已入库`);
          toast('标题已添加', 'success');
          ['t-title', 't-author', 't-isbn', 't-publisher'].forEach((id) => $(id).value = '');
          await Promise.all([loadBooksAdmin(), loadTitleOptions()]);
        } catch (e) { setResult('add-title-result', false, '添加失败', e.message); }
        break;
      }
      case 'add-item': {
        const titleId = $('i-title').value, barcode = $('i-barcode').value.trim();
        if (!titleId) { setResult('add-item-result', false, '添加失败', '请先选择所属标题'); break; }
        try {
          await API.post('/api/admin/library-items', { title_id: Number(titleId), barcode });
          setResult('add-item-result', true, '添加成功', `条码 ${barcode} 已加入馆藏`);
          toast('副本已添加', 'success');
          $('i-barcode').value = '';
          await loadBooksAdmin();
        } catch (e) { setResult('add-item-result', false, '添加失败', e.message); }
        break;
      }
      case 'remove-item': {
        const barcode = $('di-barcode').value.trim();
        if (!confirm(`确定移除馆藏副本 ${barcode} 吗？`)) break;
        try {
          await API.del(`/api/admin/library-items/${encodeURIComponent(barcode)}`);
          setResult('add-item-result', true, '移除成功', `条码 ${barcode} 已移除`);
          toast('副本已移除', 'success');
          $('di-barcode').value = '';
          await loadBooksAdmin();
        } catch (e) { setResult('add-item-result', false, '移除失败', e.message); }
        break;
      }
      case 'add-librarian': {
        try { const s = await API.post('/api/admin/librarians', { name: $('l-name').value.trim() }); toast(`已添加图书管理员 ${s.name}`, 'success'); $('l-name').value = ''; await loadStaff('librarians'); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
      case 'add-sysadmin': {
        try { const s = await API.post('/api/admin/system-admins', { name: $('sa-name').value.trim() }); toast(`已添加系统管理员 ${s.name}`, 'success'); $('sa-name').value = ''; await loadStaff('sysadmins'); }
        catch (e) { toast(e.message, 'error'); }
        break;
      }
    }
  }

  /* ---------------- 导航与渲染 ---------------- */
  function refreshIdentity() {
    API.setIdentity(state.role, state.uid);
    renderRoleSwitch();
    renderIdentityBar();
  }

  function renderRoleSwitch() {
    $('roleSwitch').innerHTML = Object.entries(ROLES).map(([key, r]) => `
      <button class="role-btn ${state.role === key ? 'active' : ''}" data-action="switch-role" data-role="${key}">
        ${icon(r.icon, 20)}<span><span class="rt">${r.label}</span><span class="rd">${r.hint}</span></span>
      </button>`).join('');
  }

  function renderFlowNav() {
    const role = ROLES[state.role];
    $('flowNav').innerHTML = role.views.map((v, i) => `
      <div class="flow-item ${state.view === v.id ? 'active' : ''}" data-action="switch-view" data-view="${v.id}">
        <span class="num">${i + 1}</span>${icon(v.icon, 18)}<span><span class="fi-label">${v.label}</span><span class="fi-hint">${v.hint}</span></span>
      </div>`).join('');
  }

  function renderIdentityBar() {
    if (state.role === 'reader') {
      $('identityBar').innerHTML = `
        <span class="identity-label">借阅证号</span>
        <div class="uid-field"><input id="cardInput" type="text" value="${esc(state.cardNo)}" placeholder="如 CARD2026000001" style="width:160px"></div>
        <span class="identity-chip">${icon('bookOpen', 14)}${state.readerName ? esc(state.readerName) : '读者'}</span>`;
      $('cardInput').addEventListener('change', (e) => loginByCard(e.target.value));
      $('cardInput').addEventListener('keydown', (e) => { if (e.key === 'Enter') e.target.blur(); });
    } else {
      const r = ROLES[state.role];
      $('identityBar').innerHTML = `<span class="identity-chip">${icon(r.icon, 14)}${r.label}</span>`;
    }
  }

  function renderTopbar() {
    const role = ROLES[state.role];
    const v = role.views.find((x) => x.id === state.view);
    $('topTitle').textContent = v ? v.label : role.label;
    $('topSub').textContent = role.desc;
  }

  async function mountView() {
    const view = VIEWS[`${state.role}:${state.view}`];
    if (!view) return;
    renderTopbar();
    const content = $('content');
    content.innerHTML = `<div class="reveal">${view.skeleton()}</div>`;
    try { await view.mount(); } catch (e) { /* mount 内部自行处理 */ }
  }

  function persistCard() { localStorage.setItem('lib.cardNo', state.cardNo); }

  async function loginByCard(cardNo) {
    cardNo = String(cardNo || '').trim();
    if (!cardNo) {
      state.uid = 0; state.cardNo = ''; state.readerName = '';
      API.setIdentity(state.role, 0); persistCard(); renderIdentityBar();
      return;
    }
    try {
      const reader = await API.get('/api/readers/by-card/' + encodeURIComponent(cardNo));
      state.uid = reader.id;
      state.cardNo = cardNo;
      state.readerName = reader.name;
      API.setIdentity(state.role, state.uid);
      persistCard();
      toast(`欢迎，${reader.name}（${READER_TYPES[reader.reader_type] || reader.reader_type}）`, 'success');
    } catch (e) {
      state.uid = 0; state.cardNo = ''; state.readerName = '';
      API.setIdentity(state.role, 0); persistCard();
      toast(e.message, 'error');
    }
    renderIdentityBar();
    if (['loans', 'reservations', 'catalog'].includes(state.view)) mountView();
  }

  function navigate(role, viewId) {
    state.role = role;
    state.view = viewId;
    localStorage.setItem('lib.role', role);
    renderRoleSwitch();
    renderFlowNav();
    refreshIdentity();
    mountView();
  }

  /* ---------------- 事件委托 ---------------- */
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    const action = el.dataset.action;
    if (action === 'switch-role') { navigate(el.dataset.role, ROLES[el.dataset.role].views[0].id); return; }
    if (action === 'switch-view') { navigate(state.role, el.dataset.view); return; }
    handleAction(action, el);
  });

  document.addEventListener('submit', (e) => {
    const form = e.target.closest('form[data-form]');
    if (!form) return;
    e.preventDefault();
    handleSubmit(form.dataset.form);
  });

  /* ---------------- 启动 ---------------- */
  function init() {
    const role = ROLES[state.role] || ROLES.reader;
    state.view = role.views[0].id;
    API.setIdentity(state.role, state.uid);
    renderRoleSwitch();
    renderFlowNav();
    renderIdentityBar();
    renderTopbar();
    mountView();
    if (state.role === 'reader' && state.cardNo) loginByCard(state.cardNo);
  }

  init();
})();

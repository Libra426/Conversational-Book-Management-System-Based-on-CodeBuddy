/* ============================================================
   api.js —— 与后端交互的唯一入口（前后端拆分点）
   ------------------------------------------------------------
   把 API_BASE 改为后端地址（例如 'http://localhost:8000'），
   即可把整个 static/ 目录当作独立前端，托管到任意静态服务器，
   而无需改动其它任何代码。
   ============================================================ */
window.LibraryAPI = (function () {
  const API_BASE = '';

  // 身份（角色 + 用户 id），由 app.js 通过 setIdentity 维护
  const identity = { role: 'reader', uid: 0 };

  function setIdentity(role, uid) {
    identity.role = role;
    identity.uid = Number(uid) || 0;
  }

  function getIdentity() {
    return { ...identity };
  }

  function headers() {
    return {
      'Content-Type': 'application/json',
      'X-Role': identity.role,
      'X-User-Id': String(identity.uid),
    };
  }

  async function request(method, path, body) {
    const opts = { method, headers: headers() };
    if (body !== undefined) opts.body = JSON.stringify(body);

    let res;
    try {
      res = await fetch(API_BASE + path, opts);
    } catch (e) {
      const err = new Error('无法连接后端（请确认已运行 uvicorn app.main:app）');
      err.network = true;
      throw err;
    }

    let data = null;
    try { data = await res.json(); } catch (e) { /* 204 等无响应体 */ }

    if (!res.ok) {
      let msg = 'HTTP ' + res.status;
      if (data && data.detail) {
        msg = Array.isArray(data.detail)
          ? data.detail.map((d) => d.msg || JSON.stringify(d)).join('；')
          : String(data.detail);
      }
      const err = new Error(msg);
      err.code = data && data.code;
      err.status = res.status;
      throw err;
    }
    return data;
  }

  return {
    setIdentity,
    getIdentity,
    get: (p) => request('GET', p),
    post: (p, b) => request('POST', p, b),
    del: (p) => request('DELETE', p),
  };
})();

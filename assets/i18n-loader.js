/* ZHANXIN GLOBAL - 多语言切换入口
   有语言副本的页面走 URL 跳转（利于收录），没有副本的页面回落到动态加载语言包。 */
(function () {
  window.translations = window.translations || {};

  var HAVE_COPY = { home: 1, about: 1, contact: 1, products: 1 };
  var LANG_PREFIX = /^\/(zh|de|es|fr|ja|ar)(\/|$)/;

  function pageType() {
    var p = location.pathname;
    var m = p.match(LANG_PREFIX);
    var rest = m ? p.slice(m[0].replace(/\/$/, "").length) : p;
    rest = rest.replace(/^\/+|\/+$/g, "");
    if (rest === "" || rest === "index.html") return "home";
    if (/\.html$/.test(rest) || rest.indexOf("blog/") === 0 || rest.indexOf("product/") === 0) return null;
    return rest;
  }

  function urlFor(lang) {
    var t = pageType();
    if (t === null || !HAVE_COPY[t]) return null;
    if (lang === "en") return t === "home" ? "/" : "/" + t;
    return t === "home" ? "/" + lang + "/" : "/" + lang + "/" + t + "/";
  }

  function apply(lang) {
    var url = urlFor(lang);
    if (url) { location.href = url; return; }
    if (window.translations[lang]) { window.setLang && window.setLang(lang); return; }
    var s = document.createElement("script");
    s.src = "/assets/i18n/" + lang + ".js?v=20261108";
    s.onload = function () { window.setLang && window.setLang(lang); };
    s.onerror = function () { window.setLang && window.setLang("en"); };
    document.head.appendChild(s);
  }

  window.ZX_LANG = { apply: apply, urlFor: urlFor, pageType: pageType };
})();

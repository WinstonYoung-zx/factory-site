// lang.js
const translations = {
  en: {
    home: "Home",
    products: "Products",
    about: "About Us",
    contact: "Contact",
    allCategories: "All Categories",
    ourProducts: "Our Products"
  },
  es: {
    home: "Inicio",
    products: "Productos",
    about: "Sobre Nosotros",
    contact: "Contacto",
    allCategories: "Todas las categorías",
    ourProducts: "Nuestros Productos"
  },
  ar: {
    home: "الرئيسية",
    products: "المنتجات",
    about: "معلومات عنا",
    contact: "اتصل بنا",
    allCategories: "كل الفئات",
    ourProducts: "منتجاتنا"
  },
  fr: {
    home: "Accueil",
    products: "Produits",
    about: "À propos de nous",
    contact: "Contact",
    allCategories: "Toutes les catégories",
    ourProducts: "Nos produits"
  },
  de: {
    home: "Startseite",
    products: "Produkte",
    about: "Über uns",
    contact: "Kontakt",
    allCategories: "Alle Kategorien",
    ourProducts: "Unsere Produkte"
  },
  zh: {
    home: "首页",
    products: "产品",
    about: "关于我们",
    contact: "联系我们",
    allCategories: "全部分类",
    ourProducts: "我们的产品"
  }
};

let currentLang = "en";
function setLang(lang) {
  currentLang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    el.innerText = translations[lang][key];
  });
}
document.querySelector(".lang-select").addEventListener("change", e=>{
  setLang(e.target.value);
});
setLang(currentLang);

window.CF = window.CF || {};

// Atajos para buscar elementos del DOM. Evitan repetir document.querySelector.
CF.$ = (selector) => document.querySelector(selector);
CF.$$ = (selector) => Array.from(document.querySelectorAll(selector));

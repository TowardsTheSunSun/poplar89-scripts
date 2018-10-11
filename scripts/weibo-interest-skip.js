// ==UserScript==
// @name         新浪微博兴趣推荐自动跳转
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  新浪微博兴趣推荐自动跳转微博首页
// @author       poplar89
// @match        https://weibo.com/nguide/interests
// @match        https://www.weibo.com/nguide/interests
// @grant        none
// ==/UserScript==

(function() {
    window.location.href="https://weibo.com";
})();
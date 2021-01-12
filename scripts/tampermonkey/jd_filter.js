// ==UserScript==
// @name         京东自定义过滤器
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://search.jd.com/Search*
// @grant        none
// ==/UserScript==

(function() {
    var parentNode=document.getElementById("J_filter").children[0];
    var beforeNode=parentNode.children[2];

    var loadSpeedText=document.createElement("input")
    loadSpeedText.type="text"
    loadSpeedText.id="loadSpeedText"
    loadSpeedText.value="35"
    loadSpeedText.size=2
    loadSpeedText.style.margin=" 0 8px 0 0"
    parentNode.insertBefore(loadSpeedText, beforeNode)

    var loadButton=document.createElement("button");
    loadButton.innerText="加载"
    loadButton.onclick=loadItems
    loadButton.style.margin=" 0 8px 0 0"
    parentNode.insertBefore(loadButton, beforeNode)

    var ziyingButton=document.createElement("button");
    ziyingButton.innerText="自营"
    ziyingButton.onclick=filterZiying
    ziyingButton.style.margin=" 0 8px 0 0"
    parentNode.insertBefore(ziyingButton, beforeNode)
})();

function loadItems(){
    var speed = document.getElementById("loadSpeedText").value;
    var i = 0;
    //可以加大跳转幅度
    var interval = window.setInterval(function(){
        i++;
        var beforeScrollY = window.scrollY;
        window.scrollTo(0, i*100)
        console.log(new Date().getTime() +" - scrollTo "+i*100)
        if(window.scrollY == beforeScrollY) {
            window.clearInterval(interval)
            window.setTimeout(window.scrollTo(0,0), 200)
            return
        }
    }, speed)
}

function filterZiying(){
    filter("自营")
}

function filter(filterText){
    var parent=document.getElementById("J_goodsList").getElementsByClassName("gl-warp")[0];
    var goodsList=parent.children;
    var toBeRemove=[];
    for(var i=0;i<goodsList.length;i++){
        var item = goodsList[i];
        if(item.textContent.indexOf(filterText)==-1) {
            toBeRemove.push(item)
        }
    }

    for(var j=0;j<toBeRemove.length;j++){
        var itemRemove=toBeRemove[j]
        itemRemove.remove()
    }
}
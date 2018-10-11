// ==UserScript==
// @name         手动DHCP列表排序
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  对华硕路由器AC68U的“手动DHCP列表”按照ip地址最后一位进行排序
// @author       poplar89
// @match        http://router.asus.com/Advanced_DHCP_Content.asp
// @grant        none
// ==/UserScript==

(function() {
    var ccc = document.getElementsByClassName("FormTable_table")[0].getElementsByTagName("th")[1];
    ccc.setAttribute("style","cursor:pointer");
    ccc.addEventListener("click", function(){
        var tbody = document.getElementById("dhcp_staticlist_table").children[0];
        var staticlist = tbody.children;
        var result = [];
        for(var i=0;i<staticlist.length;i++){
            result.push(staticlist[i]);
        }
        for(i=0;i<result.length;i++){
            for(var j=0;j<result.length-i-1;j++){
                var value1 = parseInt(result[j].children[1].innerHTML.split("\.")[3]);
                var value2 = parseInt(result[j+1].children[1].innerHTML.split("\.")[3]);
                if(value1>value2){
                    var temp = result[j];
                    result[j] = result[j+1];
                    result[j+1] = temp;
                }
            }
        }
        tbody.innerHTML = "";
        for(i=0;i<result.length;i++){
            tbody.appendChild(result[i]);
        }
    });
})();
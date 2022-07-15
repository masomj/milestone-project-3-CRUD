document.addEventListener('DOMContentLoaded', function() {
    let nav = document.querySelectorAll('.sidenav');
  M.Sidenav.init(nav);
});

document.addEventListener('DOMContentLoaded', function() {
  let records= document.querySelectorAll('.collapsible');
  M.Collapsible.init(records);
});


function fillTime(evnt){
  const now = new Date()
  ele = evnt.target
  ele.value = ("0" + now.getHours()).slice(-2) + ":" + ("0" + now.getMinutes()).slice(-2);
}


let startTime =document.getElementById("start_time");
let endTime = document.getElementById("end_time");


endTime.addEventListener('click',fillTime);
startTime.addEventListener('click',fillTime);
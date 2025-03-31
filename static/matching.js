let currentSearch = 0;
let name = document.querySelector(".SprofileName");
    let sport = document.querySelector(".SprofileSport");
    let age = document.querySelector(".SprofileAge");
    let place = document.querySelector(".SprofilePlace");
    let personality = document.querySelector(".SprofilePersonality");

    const searchesJSON = document.getElementById('values-data').textContent;
    const searches = JSON.parse(searchesJSON)

document.addEventListener("DOMContentLoaded", function(){
    let name = document.querySelector(".SprofileName");
    let sport = document.querySelector(".SprofileSport");
    let age = document.querySelector(".SprofileAge");
    let place = document.querySelector(".SprofilePlace");
    let personality = document.querySelector(".SprofilePersonality");

    const searchesJSON = document.getElementById('values-data').textContent;
    const searches = JSON.parse(searchesJSON)

    window.onload = function() {

    if (searches.length > 0) {
            search = searches[0]
            name.textContent = search.name;
            sport.textContent = search.sport;
            age.textContent = search.age;
            place.textContent = search.place;
            personality.textContent = search.personality;
            days = search.availableD;
            times = search.availableT;
            let splitTimes = times.split(',')
            let splitDays = days.split(',');
            for(var i = 0; i < splitDays.length; i++){
                day = splitDays[i];
                let dayElement =document.querySelector(`.${day}Time`);
                dayElement.textContent = (`${splitTimes[i*2]} - ${splitTimes[i*2+1]}`);
            }
        }
    }

});
function searchNextPerson(){
    currentSearch +=1;
    if (currentSearch > searches.length){

    }
    else{
    search = searches[currentSearch]
            name.textContent = search.name;
            sport.textContent = search.sport;
            age.textContent = search.age;
            place.textContent = search.place;
            personality.textContent = search.personality;
            days = search.availableD;
            times = search.availableT;
            let splitTimes = times.split(',')
            let splitDays = days.split(',');
            for(var i = 0; i < splitDays.length; i++){
                day = splitDays[i];
                let dayElement =document.querySelector(`.${day}Time`);
                dayElement.textContent = (`${splitTimes[i*2]} - ${splitTimes[i*2+1]}`);
            }
    }
}

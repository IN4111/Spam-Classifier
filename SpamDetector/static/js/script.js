const spamDetect=document.querySelector("#spam-detect");
const spamRecord=document.querySelector("#spam-record");
const aboutAuthor=document.querySelector("#author-detail");
const Scores=document.querySelector("#scores");

active=false;
setActionButtons=()=>{
    document.querySelector(".reset-button").addEventListener("click",()=>document.querySelector('.text-area').value='');
    document.querySelector(".test-button").addEventListener("click",()=>{
        if(document.querySelector('.text-area').value!==""){
            document.querySelector(".loading").style.display="block";
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://127.0.0.1:8000/result?text="+document.querySelector('.text-area').value, true);
            xhr.responseType = 'document'; 
            xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var toast_result=xhr.responseXML.querySelector(".toast-popup");
                document.querySelector("body").appendChild(toast_result);
                if(!active){
                    document.querySelector('.text-area').value="";
                    toast_result.style.display="block";
                    document.querySelector(".loading").style.display="none"
                    active=true;
                    setTimeout(function(){toast_result.style.display="none";active=false;},2000);
        }
                
    }
};
    xhr.send();
}
    
});
};

setActionButtons();

var currentElement='.menu-content';

const Paths=[[spamDetect,"home/",".menu-content"],[spamRecord,"records/",".spam-records"],[aboutAuthor,"author/",".author-content"],[Scores,"scores/",".scores"]];
Paths.forEach((instance)=>{
    instance[0].addEventListener("click",()=>{
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:8000/'+instance[1], true);
    xhr.responseType = 'document';  
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.querySelector(".container").removeChild(document.querySelector(currentElement));
            document.querySelector(".container").appendChild(xhr.responseXML.querySelector(instance[2]));
            currentElement=instance[2];
            if(instance[2]===".menu-content")
            setActionButtons();
        }
    };
    xhr.send();
});
});
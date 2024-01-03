
var divp = document.getElementById("hidden-tweet");
function togglep(){
  //  divp.classList.toggle("hidden_tweet_box");
  //  divp.classList.toggle(".hidden-main-input");
  //  divp.classList.toggle(".hidden-post-btn");
  //  divp.classList.toggle(".hidden-Menu_options");

  if (divp.style.display === "none"){
      divp.style.display= "block";
  }
  else {
    divp.style.display="none";
  }
 
  
}
function inputmeathod(){
 
   document.getElementById("file_input1").click();
  
}

let ht= document.getElementById("heart-icon");

function heart(){
  console.log(1);
  ht.classList.toggle("fa-solid");
  if (ht.style.color == " #19885c"){
     ht.style.color = "white";
  }
  else{
    ht.style.color=" #19885c";
  }
  
}

console.log(1);
var divc = document.getElementById("post-box");
function togglec(){
  //  divp.classList.toggle("hidden_tweet_box");
  //  divp.classList.toggle(".hidden-main-input");
  //  divp.classList.toggle(".hidden-post-btn");
  //  divp.classList.toggle(".hidden-Menu_options");

  if (divc.style.display === "none"){
      divc.style.display= "block";
  }
  else {
    divc.style.display="none";
  }
 
  
}
// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  // hljs.highlightAll();
  let alertWrapper = document.querySelector('.alert')
  let alertClose = document.querySelector('.alert__close')

  if (alertWrapper){
    alertClose.addEventListener('click', function(){
      alertWrapper.style.display = "none"
    })
  }

  // setTimeout(() => {
  //   if (alertWrapper) {
  //     console.log(alertClose)
  //     alertWrapper.style.display = "none"
  //   }
  // }, 9000); // 300


});





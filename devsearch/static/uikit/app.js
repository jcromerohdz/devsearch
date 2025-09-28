// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

setTimeout(() => {
    if (alertWrapper) {
      console.log(alertClose)
      alertWrapper.style.display = "none"
    }
    }, 3000); // 300


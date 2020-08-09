$(document).ready(function() {
  window.elem = "hello";

  $(".glyph").on("click", function() {
    window.elem = this;
    console.log(this.textContent);
  })
});

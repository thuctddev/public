// Remove all body content and make a blank white page
(function clearPage() {
  // Remove all child elements inside body
  document.body.innerHTML = '';

  // Reset body styles to blank white page
  document.body.style.cssText = `
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  `;

  // Also reset html element
  document.documentElement.style.cssText = `
    margin: 0;
    padding: 0;
    background-color: #ffffff;
  `;
})();

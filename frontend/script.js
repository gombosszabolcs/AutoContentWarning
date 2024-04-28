function sendUrl() {
  const url = document.getElementById("urlInput").value; /* URL beolvasása */
  const data = { url }; /* JSON adat az URL-lel */

  /* Betöltési ikon megjelenítése */
  document.getElementById("loading").style.display = "block";
  document.getElementById("result").innerText = ""; /* Eredmény törlése */

  fetch("http://127.0.0.1:5000/api/process_url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json()) /* JSON válasz */
    .then((data) => {
      document.getElementById("loading").style.display =
        "none"; /* Betöltési ikon elrejtése */
      if (data.decision) {
        document.getElementById("result").innerText =
          "Content is appropriate."; /* Pozitív üzenet */
      } else {
        document.getElementById("result").innerText =
          "Content contains inappropriate language."; /* Negatív üzenet */
      }
    })
    .catch((error) => {
      console.error("Error:", error); /* Hiba kezelés */
      document.getElementById("loading").style.display =
        "none"; /* Betöltési ikon elrejtése */
      document.getElementById("result").innerText =
        "An error occurred."; /* Hiba üzenet */
    });
}

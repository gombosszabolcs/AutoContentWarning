function sendUrl() {
  const url = document.getElementById("urlInput").value;
  const data = { url };

  document.getElementById("loading").style.display = "block";
  document.getElementById("checker_button").style.visibility = "hidden";
  document.getElementById("result").innerText = "";

  fetch("http://127.0.0.1:5000/api/process_url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("checker_button").style.visibility = "visible";
      document.getElementById("loading").style.display = "none";
      if (data.decision == "True") {
        document.getElementById("result").innerText = "Content is appropriate.";
      } else {
        document.getElementById("result").innerText =
          "Content contains inappropriate language.";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("loading").style.display = "none";
      document.getElementById("result").innerText = "An error occurred.";
    });
}

function updateVehicleCount() {
  fetch('/vehicle_count')
    .then(res => res.json())
    .then(data => {
      document.getElementById("vehicle-count").textContent = data.total;

      document.getElementById("car-count").textContent = data.details.car || 0;
      document.getElementById("bus-count").textContent = data.details.bus || 0;
      document.getElementById("truck-count").textContent = data.details.truck || 0;
      document.getElementById("motorbike-count").textContent = data.details.motorbike || 0;


    });
}
let isStreaming = false;

const button = document.getElementById("toggle-button");

button.addEventListener("click", () => {
  // const isStreaming = button.src.includes("pause.svg");
  const url = isStreaming ? "/start" : "/stop";

  const newIcon = isStreaming ? "images/play.svg" : "images/pause.svg";

  fetch(url, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      isStreaming = !isStreaming;
      button.src = `/static/${newIcon}`;
      console.log("Stream status:", data.status);
    })
    .catch(err => {
      console.error("Error toggling stream:", err);
    });


});
function changeVideo() {
  const videoSelect = document.getElementById("videoSelect");
  const selectedFile = videoSelect.value;

  fetch("/set_video", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ filename: selectedFile })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Video changed to:", data.file);
      // Force-refresh the video stream by changing the src (cache buster)
      const videoFeed = document.getElementById("video_feed");
      if (videoFeed) {
        videoFeed.src = "/video_feed?" + new Date().getTime();
      }
    })
    .catch(error => {
      console.error("Error changing video:", error);
      document.getElementById("change-video").onclick= document.getElementById("toggle-button").src ="static/images/play.svg";
        console.log("changed");
      
    });
}
// Call every 2 seconds
setInterval(updateVehicleCount, 1000);

// Run once immediately on load
updateVehicleCount();

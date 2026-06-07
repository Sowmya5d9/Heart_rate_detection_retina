// Update dashboard every second
setInterval(() => {

    fetch("/metrics")
        .then(response => response.json())
        .then(data => {

            document.getElementById(
                "eye-status"
            ).innerText = data.eye_status;

            document.getElementById(
                "blink-count"
            ).innerText = data.blink_count;

            document.getElementById(
                "frequency"
            ).innerText = data.frequency;

            document.getElementById(
                "heart-rate"
            ).innerText = data.heart_rate;

        })
        .catch(error => {
            console.log("Metrics Error:", error);
        });

}, 1000);


// Start Camera
function startCamera() {

    fetch("/start_camera")
        .then(response => response.json())
        .then(data => {

            document.getElementById("videoFeed").src =
                "/video_feed?" + new Date().getTime();

        });
}


// Stop Camera
function stopCamera() {

    fetch("/stop_camera")
        .then(response => response.json())
        .then(data => {

            console.log(data);

            document.getElementById(
                "videoFeed"
            ).src = "";

            document.getElementById(
                "eye-status"
            ).innerText = "Not Detected";

            document.getElementById(
                "blink-count"
            ).innerText = "0";

            document.getElementById(
                "frequency"
            ).innerText = "N/A";

            document.getElementById(
                "heart-rate"
            ).innerText = "N/A";

        })
        .catch(error => {
            console.log("Stop Camera Error:", error);
        });

}
const video = document.getElementById("webcam");
const captureButton = document.getElementById("capture");
const resultParagraph = document.getElementById("result");

// Access the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing webcam:", err);
    });

// Capture frame and send to FastAPI backend
captureButton.addEventListener("click", async () => {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);

    const image = canvas.toDataURL("image/jpeg");

    // Send the image to the FastAPI backend
    const response = await fetch("http://localhost:8000/detect-emotion", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ image }),
    });

    const data = await response.json();
    resultParagraph.textContent = `Detected Emotion: ${data.emotion} (Confidence: ${data.confidence.toFixed(2)})`;
});
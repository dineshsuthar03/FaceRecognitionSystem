function uploadImage(event) {
    event.preventDefault();  // Prevent the page from reloading (if it's inside a form)
    console.log("Starting image upload...");

    var input = document.getElementById('imageInput');
    var nameInput = document.getElementById('nameInput');
    var file = input.files[0];
    var name = nameInput.value; // Get the name from the input

    // Check if the file and name are provided
    if (!file) {
        console.log("No file selected!");
        document.getElementById('result').innerHTML = "Please select an image file.";
        return;
    }

    if (name) {
        console.log("Name provided: " + name);
    } else {
        console.log("No name provided.");
    }

    var formData = new FormData();
    formData.append("image", file);
    formData.append("name", name); // Send the name as well

    console.log("Preparing to send the request to the backend...");

    fetch("http://127.0.0.1:5000/recognize", {
        method: "POST",
        body: formData
    })
    .then(response => {
        console.log("Response received from the server.");
        return response.json();
    })
    .then(data => {
        console.log("Data received from server:", data);
        
        if (data.name) {
            console.log("Face recognized with name: " + data.name);
            document.getElementById('result').innerHTML = "Recognized: " + data.name;
        } else {
            console.log("Error from backend:", data.error);
            document.getElementById('result').innerHTML = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.log("An error occurred while processing the request:", error);
        document.getElementById('result').innerHTML = "Error: " + error;
    });
}

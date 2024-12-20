document.getElementById("url-check-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const url = document.getElementById("url-input").value;

    fetch('/check-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'url': url
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display result box
        const resultBox = document.getElementById("result-box");
        resultBox.style.display = 'block';
        
        // Update the URL and result in the box
        document.getElementById("checked-url").innerText = url;
        document.getElementById("result-text").innerText = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Back button functionality
document.getElementById("back-btn").addEventListener("click", function() {
    document.getElementById("result-box").style.display = 'none';  // Hide result box
    document.getElementById("url-input").value = '';  // Clear input field
});

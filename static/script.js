document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('logFileForm');
    form.onsubmit = function(event) {
        event.preventDefault();
        var formData = new FormData(form);
        fetch('/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('analysisResults').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('analysisResults').textContent = 'Error: ' + error;
        });
    };
  });
  
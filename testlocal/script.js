// File upload handling
document.querySelectorAll('.file-input').forEach(input => {
    input.addEventListener('change', function() {
        const file = this.files[0];
        const uploadId = this.id;
        const fileInfoId = uploadId === 'file1' ? 'file1-info' : 'file2-info';
        const fileInfo = document.getElementById(fileInfoId);
        
        if (file) {
            if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
                fileInfo.textContent = 'Please select a CSV file only';
                fileInfo.style.color = '#e74c3c';
                this.value = '';
                return;
            }
            
            fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
            fileInfo.style.color = '#4b6cb7';
        } else {
            fileInfo.textContent = '';
        }
        
        checkUploadButton();
    });
});

// Drag and drop functionality
document.querySelectorAll('.upload-area').forEach(area => {
    area.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#182848';
        this.style.backgroundColor = '#eef2ff';
    });
    
    area.addEventListener('dragleave', function() {
        this.style.borderColor = '#4b6cb7';
        this.style.backgroundColor = '#f8f9ff';
    });
    
    area.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '#4b6cb7';
        this.style.backgroundColor = '#f8f9ff';
        
        const file = e.dataTransfer.files[0];
        const input = this.querySelector('.file-input');
        
        if (file) {
            if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
                const fileInfo = this.querySelector('.file-info');
                fileInfo.textContent = 'Please select a CSV file only';
                fileInfo.style.color = '#e74c3c';
                return;
            }
            
            // Create a new FileList with the dropped file
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            
            // Trigger the change event
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
        }
    });
});

// Check if both files are selected to enable upload button
function checkUploadButton() {
    const file1 = document.getElementById('file1').files[0];
    const file2 = document.getElementById('file2').files[0];
    const uploadBtn = document.getElementById('upload-btn');
    
    uploadBtn.disabled = !(file1 && file2);
}

// Upload files function
function uploadFiles() {
    const file1 = document.getElementById('file1').files[0];
    const file2 = document.getElementById('file2').files[0];
    
    if (!file1 || !file2) {
        alert('Please select both files');
        return;
    }
    
    // In a real application, you would send the files to a server here
    // For this example, we'll just show a success message
    
    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);
    
    // Simulate upload process
    const uploadBtn = document.getElementById('upload-btn');
    uploadBtn.textContent = 'Uploading...';
    uploadBtn.disabled = true;
    
    // Simulate network delay
    setTimeout(() => {
        uploadBtn.textContent = 'Upload Successful!';
        uploadBtn.style.background = 'linear-gradient(90deg, #4CAF50 0%, #2E7D32 100%)';
        
        // Reset button after 2 seconds
        setTimeout(() => {
            uploadBtn.textContent = 'Upload Files';
            uploadBtn.disabled = false;
            uploadBtn.style.background = 'linear-gradient(90deg, #4CAF50 0%, #2E7D32 100%)';
        }, 2000);
        
        // Show results in console
        console.log('File 1:', file1.name);
        console.log('File 2:', file2.name);
    }, 1500);
    
    // Log form data to console (in a real app, you would send this to a server)
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }
}
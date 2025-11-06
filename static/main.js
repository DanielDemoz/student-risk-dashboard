const API_BASE = window.location.origin;

const form = document.getElementById('uploadForm');
const uploadBtn = document.getElementById('uploadBtn');
const loader = document.getElementById('loader');
const messageDiv = document.getElementById('message');
const resultsSection = document.getElementById('resultsSection');
const tableBody = document.getElementById('tableBody');

// Make file input clickable
document.querySelector('.file-input-wrapper').addEventListener('click', function(e) {
    if (e.target.tagName !== 'INPUT') {
        document.getElementById('excelFile').click();
    }
});

// Form submit
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = document.getElementById('excelFile').files[0];
    if (!file) {
        showMessage('error', '❌ Please select an Excel file first!');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    uploadBtn.disabled = true;
    loader.style.display = 'block';
    messageDiv.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE}/upload-excel`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }
        
        showMessage('success', `✅ ${data.message}`);
        setTimeout(loadResults, 1000);
    } catch (error) {
        showMessage('error', `❌ ${error.message}`);
    } finally {
        uploadBtn.disabled = false;
        loader.style.display = 'none';
    }
});

// Load results
async function loadResults() {
    try {
        const response = await fetch(`${API_BASE}/results`);
        if (!response.ok) {
            if (response.status === 404) return;
            throw new Error('Failed to load results');
        }
        
        const students = await response.json();
        if (students.length === 0) return;
        
        displayResults(students);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Display results
function displayResults(students) {
    // Summary
    const total = students.length;
    const highRisk = students.filter(s => s.risk_label === 'High Risk').length;
    const atRisk = students.filter(s => s.risk_label === 'At Risk').length;
    const safe = students.filter(s => s.risk_label === 'Safe').length;
    
    document.getElementById('totalStudents').textContent = total;
    document.getElementById('highRiskCount').textContent = highRisk;
    document.getElementById('mediumRiskCount').textContent = atRisk;
    document.getElementById('lowRiskCount').textContent = safe;
    
    // Table - show top 10
    const top10 = students.slice(0, 10);
    tableBody.innerHTML = '';
    
    top10.forEach(student => {
        const row = document.createElement('tr');
        const riskClass = student.risk_label === 'High Risk' ? 'high' :
                         student.risk_label === 'At Risk' ? 'medium' : 'low';
        
        row.innerHTML = `
            <td><strong>${escapeHtml(student.student_name)}</strong></td>
            <td>${escapeHtml(student.program || 'N/A')}</td>
            <td>${student.grade.toFixed(1)}%</td>
            <td>${student.attendance_rate.toFixed(1)}%</td>
            <td><span class="risk-badge ${riskClass}">${escapeHtml(student.risk_label)}</span></td>
            <td>${escapeHtml(student.recommended_action)}</td>
            <td><a href="mailto:${student.email}" class="email-link">${escapeHtml(student.email || '')}</a></td>
        `;
        tableBody.appendChild(row);
    });
    
    resultsSection.style.display = 'block';
}

function showMessage(type, text) {
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = text;
    messageDiv.style.display = 'block';
    if (type === 'success') {
        setTimeout(() => messageDiv.style.display = 'none', 5000);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load on page load
window.addEventListener('load', loadResults);


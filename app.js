document.addEventListener('DOMContentLoaded', () => {
    const grievanceForm = document.getElementById('grievanceForm');
    const responseMessage = document.getElementById('responseMessage');
    const grievanceTableBody = document.getElementById('grievanceTableBody');

    // Pre-populated initial mock data to look like a live system
    const existingComplaints = [
        {
            id: 'CV-1042',
            citizen_name: 'Aarav Sharma',
            citizen_email: 'aarav@example.com',
            complaint_text: 'Major water pipeline burst outside Sector 14 causing flooding across main road.',
            category: 'Infrastructure',
            department: 'Water & Sanitation',
            priority: 'High',
            status: 'Assigned'
        },
        {
            id: 'CV-1041',
            citizen_name: 'Priya Patel',
            citizen_email: 'priya@example.com',
            complaint_text: 'Streetlights on 5th Avenue non-functional for three consecutive nights.',
            category: 'Public Safety',
            department: 'Electrical Services',
            priority: 'Medium',
            status: 'In Progress'
        },
        {
            id: 'CV-1040',
            citizen_name: 'Rahul Verma',
            citizen_email: 'rahul@example.com',
            complaint_text: 'Garbage dump overflowing near community center causing health hazards.',
            category: 'Sanitation',
            department: 'Waste Management',
            priority: 'High',
            status: 'Pending Dispatch'
        }
    ];

    // Initialize Page Data & Charts
    renderTable(existingComplaints);
    initDepartmentChart();

    // Form Submission Handler
    grievanceForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Standardized field names matching backend specification
        const payload = {
            citizen_name: document.getElementById('citizen_name').value,
            citizen_email: document.getElementById('citizen_email').value,
            complaint_text: document.getElementById('complaint_text').value
        };

        // UI Loading State
        showStatus('Submitting grievance to Flask backend (POST /complaints)...', 'loading');

        try {
            // Prepared API call for Flask backend
            const response = await fetch('http://localhost:5000/complaints', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const data = await response.json();
                showStatus('Grievance processed & registered with backend!', 'success');
                addNewComplaintToTable(data);
                grievanceForm.reset();
            } else {
                // Offline fallback logic
                handleOfflineSubmission(payload);
            }
        } catch (error) {
            console.warn('Backend API currently offline. Running local mock triage.');
            handleOfflineSubmission(payload);
        }
    });

    function handleOfflineSubmission(payload) {
        showStatus('Backend API offline. Simulated AI triage successful!', 'success');

        // AI Field simulation based on exact teammate specs
        const mockResponse = {
            id: `CV-${Math.floor(1000 + Math.random() * 9000)}`,
            citizen_name: payload.citizen_name,
            citizen_email: payload.citizen_email,
            complaint_text: payload.complaint_text,
            category: detectCategory(payload.complaint_text),
            department: detectDepartment(payload.complaint_text),
            priority: payload.complaint_text.toLowerCase().includes('urgent') || payload.complaint_text.toLowerCase().includes('flood') ? 'High' : 'Normal',
            status: 'Triaged (Mock Mode)'
        };

        existingComplaints.unshift(mockResponse);
        renderTable(existingComplaints);
        grievanceForm.reset();
    }

    function showStatus(message, type) {
        responseMessage.classList.remove('hidden', 'bg-indigo-500/10', 'text-indigo-400', 'border-indigo-500/30', 'bg-emerald-500/10', 'text-emerald-400', 'border-emerald-500/30');
        
        if (type === 'loading') {
            responseMessage.classList.add('bg-indigo-500/10', 'text-indigo-400', 'border-indigo-500/30');
            responseMessage.innerHTML = `<i class="fa-solid fa-spinner animate-spin mr-2"></i> ${message}`;
        } else {
            responseMessage.classList.add('bg-emerald-500/10', 'text-emerald-400', 'border-emerald-500/30');
            responseMessage.innerHTML = `<i class="fa-solid fa-circle-check mr-2"></i> ${message}`;
        }
    }

    function renderTable(data) {
        grievanceTableBody.innerHTML = '';
        data.forEach(item => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-slate-800/50 transition-colors';

            const priorityBadge = item.priority === 'High' 
                ? '<span class="bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded text-xs font-semibold">High</span>'
                : '<span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-xs font-semibold">Normal</span>';

            row.innerHTML = `
                <td class="px-4 py-3 font-mono text-xs text-indigo-400">${item.id}</td>
                <td class="px-4 py-3 font-medium text-white">${escapeHtml(item.citizen_name)}</td>
                <td class="px-4 py-3 text-xs text-slate-300 max-w-xs truncate" title="${escapeHtml(item.complaint_text)}">${escapeHtml(item.complaint_text)}</td>
                <td class="px-4 py-3 text-xs">${item.category || 'General'}</td>
                <td class="px-4 py-3 text-xs text-slate-400">${item.department || 'Unassigned'}</td>
                <td class="px-4 py-3">${priorityBadge}</td>
                <td class="px-4 py-3 text-xs font-medium text-amber-400">${item.status}</td>
            `;
            grievanceTableBody.appendChild(row);
        });
    }

    function initDepartmentChart() {
        const ctx = document.getElementById('deptChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Public Works', 'Water & Sanitation', 'Electrical', 'Waste Mgmt'],
                datasets: [{
                    data: [42, 28, 18, 12],
                    backgroundColor: ['#6366f1', '#06b6d4', '#f59e0b', '#10b981'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#94a3b8', font: { size: 11 } }
                    }
                }
            }
        });
    }

    function detectCategory(text) {
        text = text.toLowerCase();
        if (text.includes('water') || text.includes('leak')) return 'Water Supply';
        if (text.includes('light') || text.includes('power')) return 'Electrical';
        if (text.includes('garbage') || text.includes('waste')) return 'Sanitation';
        return 'Infrastructure';
    }

    function detectDepartment(text) {
        text = text.toLowerCase();
        if (text.includes('water') || text.includes('leak')) return 'Water & Sanitation Dept';
        if (text.includes('light') || text.includes('power')) return 'Electrical Services';
        if (text.includes('garbage') || text.includes('waste')) return 'Municipal Waste Mgmt';
        return 'Public Works Department';
    }

    function escapeHtml(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const grievanceForm = document.getElementById('grievanceForm');
    const responseMessage = document.getElementById('responseMessage');
    const grievanceTableBody = document.getElementById('grievanceTableBody');

    loadComplaints();
    loadAnalytics();

    // =========================
    // SUBMIT COMPLAINT
    // =========================

    grievanceForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            citizen_name: document.getElementById('citizen_name').value,
            citizen_email: document.getElementById('citizen_email').value,
            complaint_text: document.getElementById('complaint_text').value
        };

        showStatus(
            'AI is analyzing and routing your grievance...',
            'loading'
        );

        try {
            const response = await fetch('/complaints', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Complaint submission failed');
            }

            showStatus(
                `Grievance registered successfully! Complaint ID: ${data.complaint_id}`,
                'success'
            );

            grievanceForm.reset();

            await loadComplaints();
            await loadAnalytics();

        } catch (error) {
            console.error(error);

            showStatus(
                'Unable to submit grievance. Please try again.',
                'error'
            );
        }
    });


    // =========================
    // LOAD REAL COMPLAINTS
    // =========================

    async function loadComplaints() {
        try {
            const response = await fetch('/complaints');

            if (!response.ok) {
                throw new Error('Failed to load complaints');
            }

            const complaints = await response.json();

            renderTable(complaints);

        } catch (error) {
            console.error('Error loading complaints:', error);
        }
    }


    // =========================
    // RENDER COMPLAINT TABLE
    // =========================

    function renderTable(data) {
        grievanceTableBody.innerHTML = '';

        if (!data || data.length === 0) {
            grievanceTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="px-4 py-6 text-center text-slate-400">
                        No complaints submitted yet.
                    </td>
                </tr>
            `;
            return;
        }

        data.forEach(item => {

            const priorityClass =
                item.priority === 'Urgent'
                    ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                    : item.priority === 'High'
                    ? 'bg-orange-500/10 text-orange-400 border border-orange-500/20'
                    : item.priority === 'Medium'
                    ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'
                    : 'bg-blue-500/10 text-blue-400 border border-blue-500/20';

            const statusClass =
                item.status === 'Resolved'
                    ? 'text-emerald-400'
                    : item.status === 'In Progress'
                    ? 'text-blue-400'
                    : item.status === 'Assigned'
                    ? 'text-purple-400'
                    : 'text-amber-400';

            const complaintId = item.id;

            const row = document.createElement('tr');

            row.className =
                'hover:bg-slate-800/50 transition-colors';

            row.innerHTML = `
                <td class="px-4 py-3 font-mono text-xs text-indigo-400">
                    #${complaintId}
                </td>

                <td class="px-4 py-3 font-medium text-white">
                    ${escapeHtml(item.citizen_name || '')}
                </td>

                <td class="px-4 py-3 text-xs text-slate-300 max-w-xs truncate"
                    title="${escapeHtml(item.complaint_text || '')}">
                    ${escapeHtml(item.complaint_text || '')}
                </td>

                <td class="px-4 py-3 text-xs">
                    ${escapeHtml(item.category || 'Other')}
                </td>

                <td class="px-4 py-3 text-xs text-slate-400">
                    ${escapeHtml(item.department || 'Unassigned')}
                </td>

                <td class="px-4 py-3">
                    <span class="${priorityClass} px-2 py-0.5 rounded text-xs font-semibold">
                        ${escapeHtml(item.priority || 'Low')}
                    </span>
                </td>

                <td class="px-4 py-3 text-xs font-medium ${statusClass}">
                    ${escapeHtml(item.status || 'Pending')}
                </td>
            `;

            grievanceTableBody.appendChild(row);
        });
    }


    // =========================
    // LOAD REAL ANALYTICS
    // =========================

    async function loadAnalytics() {
        try {
            const response = await fetch('/analytics');

            if (!response.ok) {
                throw new Error('Failed to load analytics');
            }

            const data = await response.json();

            updateAnalyticsChart(data);

        } catch (error) {
            console.error('Error loading analytics:', error);
        }
    }


    // =========================
    // ANALYTICS CHART
    // =========================

    function updateAnalyticsChart(data) {

        const canvas = document.getElementById('deptChart');

        if (!canvas || typeof Chart === 'undefined') {
            return;
        }

        const categoryCounts = data.category_counts || {};

        const labels = Object.keys(categoryCounts);
        const values = Object.values(categoryCounts);

        if (window.departmentChart) {
            window.departmentChart.destroy();
        }

        window.departmentChart = new Chart(canvas.getContext('2d'), {
            type: 'doughnut',

            data: {
                labels: labels.length
                    ? labels
                    : ['No complaints yet'],

                datasets: [{
                    data: values.length
                        ? values
                        : [1],

                    borderWidth: 0
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: 'bottom',

                        labels: {
                            color: '#94a3b8',
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        });
    }


    // =========================
    // STATUS MESSAGE
    // =========================

    function showStatus(message, type) {

        responseMessage.classList.remove(
            'hidden',
            'bg-indigo-500/10',
            'text-indigo-400',
            'border-indigo-500/30',
            'bg-emerald-500/10',
            'text-emerald-400',
            'border-emerald-500/30',
            'bg-red-500/10',
            'text-red-400',
            'border-red-500/30'
        );

        if (type === 'loading') {

            responseMessage.classList.add(
                'bg-indigo-500/10',
                'text-indigo-400',
                'border-indigo-500/30'
            );

            responseMessage.innerHTML =
                `<i class="fa-solid fa-spinner animate-spin mr-2"></i> ${message}`;

        } else if (type === 'error') {

            responseMessage.classList.add(
                'bg-red-500/10',
                'text-red-400',
                'border-red-500/30'
            );

            responseMessage.innerHTML =
                `<i class="fa-solid fa-circle-exclamation mr-2"></i> ${message}`;

        } else {

            responseMessage.classList.add(
                'bg-emerald-500/10',
                'text-emerald-400',
                'border-emerald-500/30'
            );

            responseMessage.innerHTML =
                `<i class="fa-solid fa-circle-check mr-2"></i> ${message}`;
        }
    }


    // =========================
    // HTML SAFETY
    // =========================

    function escapeHtml(str) {

        return String(str).replace(
            /[&<>'"]/g,

            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
});

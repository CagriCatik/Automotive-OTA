// --- CLOCK ---
function updateClock() {
    const now = new Date();
    const clockEl = document.getElementById('clock');
    if (clockEl) {
        clockEl.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}
setInterval(updateClock, 1000);
updateClock();

// --- VEHICLE SIMULATOR ---
let simState = {
    battery_soc: 50,
    gear: "P",
    parking_brake: true,
    ignition: "ON"
};

function openSimControls() {
    document.getElementById('sim_app').classList.add('active');
}

function closeSimControls() {
    document.getElementById('sim_app').classList.remove('active');
}

function updateSimVal(key, val) {
    if (key === 'soc') {
        document.getElementById('val_soc').innerText = val + '%';
        simState.battery_soc = parseInt(val);
    }
    pushSimState();
}

function toggleSim(key) {
    if (key === 'brake') {
        simState.parking_brake = !simState.parking_brake;
        const btn = document.getElementById('sim_brake');
        if (simState.parking_brake) {
            btn.classList.add('active');
            btn.innerText = "Engaged";
        } else {
            btn.classList.remove('active');
            btn.innerText = "Released";
        }
    }
    pushSimState();
}

function pushSimState() {
    // Read Selects
    simState.gear = document.getElementById('sim_gear').value;
    simState.ignition = document.getElementById('sim_ign').value;

    // Send to Gateway
    fetch('/api/vehicle/state', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(simState)
    }).catch(console.error);
}

// Initial Push
pushSimState();


// --- OTA LOGIC ---
let otaOpen = false;
let updateAcknowledged = false; // Prevents re-opening success screen

function openOTA() {
    document.getElementById('ota_app').classList.add('active');
    document.getElementById('update_toast').classList.remove('visible');

    // Clear warnings
    const warnBox = document.getElementById('precondition_warn');
    if (warnBox) warnBox.classList.remove('visible');

    otaOpen = true;
}

function closeOTA() {
    document.getElementById('ota_app').classList.remove('active');
    otaOpen = false;
}

function showView(viewId) {
    // Helper to ensure mutual exclusion of views
    const views = ['view_approval', 'view_progress', 'view_success', 'view_failed'];
    views.forEach(id => {
        const el = document.getElementById(id);
        if (id === viewId) el.classList.remove('hidden');
        else el.classList.add('hidden');
    });
}

async function approve() {
    const fail = document.getElementById('fail_check').checked;
    // Don't close approval view yet, wait for response

    try {
        const res = await fetch('/api/approve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ simulate_failure: fail })
        });
        const data = await res.json();

        if (data.ok) {
            showView('view_progress');
        } else {
            // Show Warning
            alert("Cannot install: " + data.error);
        }
    } catch (e) {
        console.error("Approval failed", e);
    }
}

function rebootSystem() {
    // Simulate system refresh without reloading page (which would re-trigger success state)
    closeOTA();
    updateAcknowledged = true;

    // Visual flair: Flicker the screen
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.opacity = '1';
        // Reset to home state appearance
    }, 1000);
}

// --- POLLING LOOP ---
async function pollStatus() {
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        const s = data.state;

        if (s === 'NOTIFIED') {
            if (!otaOpen && !data.approved && !updateAcknowledged) {
                document.getElementById('update_toast').classList.add('visible');
            }
        }
        else if (s === 'WAITING_FOR_APPROVAL') {
            if (otaOpen) showView('view_approval');
        }
        else if (['DOWNLOADING', 'STAGED', 'INSTALLING', 'VALIDATING'].includes(s)) {
            if (!otaOpen) openOTA();
            showView('view_progress');

            const pRes = await fetch('/api/progress');
            const pData = await pRes.json();

            updateBar('engine', pData.progress.engine);
            updateBar('adas', pData.progress.adas);

            if (pData.logs && pData.logs.length) {
                document.getElementById('term_log').innerText = "> " + pData.logs[pData.logs.length - 1];
            }
        }
        else if (s === 'SUCCEEDED') {
            if (!updateAcknowledged) {
                if (!otaOpen) openOTA();
                showView('view_success');
            }
        }
        else if (['FAILED', 'ROLLED_BACK'].includes(s)) {
            if (!updateAcknowledged) {
                if (!otaOpen) openOTA();
                showView('view_failed');
                if (data.details && data.details.reason) {
                    document.getElementById('fail_reason').innerText = data.details.reason;
                }
            }
        }

    } catch (e) { console.error(e); }
    setTimeout(pollStatus, 1000);
}

function updateBar(id, data) {
    const bar = document.getElementById('bar_' + id);
    if (bar && data) {
        bar.style.width = data.percent + '%';
        const label = document.getElementById('label_' + id);
        if (label) label.innerText = data.status;
        if (data.percent === 100) bar.classList.add('success');
    }
}

// Global scope expose for onClick handlers
window.openOTA = openOTA;
window.closeOTA = closeOTA;
window.approve = approve;
window.rebootSystem = rebootSystem;

// Start polling
pollStatus();

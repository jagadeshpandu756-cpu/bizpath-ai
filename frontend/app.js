window.onload = function() {
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chip.classList.toggle('selected');
        });
    });
}

async function generateRoadmap() {
    const selectedInterests = [...document.querySelectorAll('.chip.selected')]
        .map(c => c.dataset.value);

    if (!document.getElementById('name').value) { alert('Please enter your name!'); return; }
    if (!document.getElementById('location').value) { alert('Please enter your location!'); return; }
    if (!document.getElementById('budget').value) { alert('Please enter your budget!'); return; }
    if (selectedInterests.length === 0) { alert('Please select at least one business interest!'); return; }

    const payload = {
        name: document.getElementById('name').value,
        location: document.getElementById('location').value,
        budget: parseFloat(document.getElementById('budget').value),
        currency: document.getElementById('currency').value,
        interests: selectedInterests,
        risk_level: parseInt(document.getElementById('riskLevel').value),
        time_horizon: parseInt(document.getElementById('timeHorizon').value),
        experience: 0,
        goal: document.getElementById('goal').value || 'Build a profitable business'
    };

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('loading').scrollIntoView({ behavior: 'smooth' });

    try {
        const response = await fetch('/generate-roadmap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (data.roadmap) {
            document.getElementById('roadmapContent').innerHTML = formatRoadmap(data.roadmap);
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Something went wrong. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Cannot connect to server. Make sure the backend is running!');
    }

    document.getElementById('loading').style.display = 'none';
    document.getElementById('submitBtn').disabled = false;
}

function formatRoadmap(text) {
    return text
        .replace(/## (.+)/g, '<h2>$1</h2>')
        .replace(/# (.+)/g, '<h2>$1</h2>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/^- (.+)/gm, '<li>$1</li>')
        .replace(/^\d+\. (.+)/gm, '<li>$1</li>')
        .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}
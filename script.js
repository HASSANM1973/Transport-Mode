// static/script.js
function showBaseline() {
    document.getElementById('baseline').style.display = 'block';
}

function showPolicyOptions() {
    document.getElementById('policyOptions').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function calculateImpact() {
    const busTime = document.getElementById('busTime').value;
    const parkingFee = document.getElementById('parkingFee').value;
    const busFrequency = document.getElementById('busFrequency').value;
    const parkRide = document.getElementById('parkRide').checked;

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ busTime, parkingFee, busFrequency, parkRide })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').style.display = 'block';
        document.getElementById('modeShare').innerText = `${data.mode_share.public_transport}%`;
        document.getElementById('carTrips').innerText = data.reduction_in_car_trips;
        document.getElementById('emissions').innerText = data.reduction_in_emissions;

        const ctx = document.getElementById('projectedChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Car', 'Public Transport'],
                datasets: [{
                    data: [data.mode_share.car, data.mode_share.public_transport],
                    backgroundColor: ['#FF6384', '#36A2EB']
                }]
            }
        });
    });
}
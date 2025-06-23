const body = document.body;
const iframe = document.querySelector('iframe');
const desktopApps = document.querySelectorAll('.desktopApp');
desktopApps.forEach(desktopApp => {
    desktopApp.addEventListener('click', openWindow);
});

document.addEventListener('mousedown', (e) => {
    body.classList.add('grabbing');
});

document.addEventListener('mouseup', () => {
    body.classList.remove('grabbing');
});

const windowContainer = document.getElementById('windowContainer');

function openWindow(event) {
    const app = event.currentTarget;
    const label = app.querySelector('label').textContent;

    const headerText = document.getElementById('headerText');
    const icon = document.querySelector('#windowHeader img');

    headerText.textContent = label;

    if (label === "Litter Predictions") {
        iframe.src = "Frontend/dashboard.html";
        icon.src = "Frontend/Art/trashCan.png";
        icon.style.scale = "0.7";
    } else {
        iframe.src = "Frontend/stats.html";
        icon.src = "Frontend/Art/colaCan.png";
        // icon.style.scale = "1.3";
    }

    if (getComputedStyle(windowContainer).display === "none") {
        windowContainer.style.display = "block";
        setTimeout(() => {
            windowContainer.style.transform = "scale(1)";
        }, 10);
    }
}

function closeWindow() {
    windowContainer.style.transform = "scale(0)";
    setTimeout(() => {
        windowContainer.style.display = "none";
    }, 200);
}

function updateDateTime() {
    dateTime = new Date();
    document.getElementById('dateTime').textContent = dateTime.toLocaleString();
}

setInterval(updateDateTime, 1000);
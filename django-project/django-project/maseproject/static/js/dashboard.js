document.addEventListener("DOMContentLoaded", function () {
    // === Toggle Status Coș ===
    const toggleBtn = document.getElementById("toggleStatus");
    const hiddenInput = document.getElementById("status_cos");

    if (toggleBtn && hiddenInput) {
        toggleBtn.addEventListener("click", function () {
            const isFull = toggleBtn.classList.contains("plin");

            if (isFull) {
                toggleBtn.classList.remove("plin");
                toggleBtn.classList.add("gol");
                toggleBtn.textContent = "Container gol";
                hiddenInput.value = "false";
            } else {
                toggleBtn.classList.remove("gol");
                toggleBtn.classList.add("plin");
                toggleBtn.textContent = "Container plin – gata de colectat";
                hiddenInput.value = "true";
            }
        });
    }

    // === Hartă Leaflet ===
    const mapDiv = document.getElementById("harta");
    if (!mapDiv) return;

    // Coordonate din atribut data-* dacă sunt salvate în template
    const latAttr = mapDiv.getAttribute("data-lat");
    const lonAttr = mapDiv.getAttribute("data-lon");

    const hasCoords = latAttr && lonAttr && !isNaN(latAttr) && !isNaN(lonAttr);
    const adresa = document.getElementById("adresa")?.value;

    if (hasCoords) {
        const lat = parseFloat(latAttr);
        const lon = parseFloat(lonAttr);

        const map = L.map('harta').setView([lat, lon], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        L.marker([lat, lon]).addTo(map)
            .bindPopup("Containerul dumneavoastră")
            .openPopup();

    } else if (adresa) {
        // fallback geocodare dacă lat/lon lipsesc
        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(adresa)}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const lat = parseFloat(data[0].lat);
                    const lon = parseFloat(data[0].lon);

                    const map = L.map('harta').setView([lat, lon], 15);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; OpenStreetMap contributors'
                    }).addTo(map);

                    L.marker([lat, lon]).addTo(map)
                        .bindPopup("Locația estimată")
                        .openPopup();
                } else {
                    mapDiv.innerHTML = "<p style='color:red;'>Adresa nu a putut fi localizată.</p>";
                }
            })
            .catch(err => {
                console.error("Eroare la geocodare:", err);
                mapDiv.innerHTML = "<p style='color:red;'>Eroare la afișarea hărții.</p>";
            });
    } else {
        mapDiv.innerHTML = "<p style='color:red;'>Locație indisponibilă.</p>";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const map = L.map("map").setView([-12.121, -77.03], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "© OpenStreetMap contributors"
    }).addTo(map);

    // Datos pasados desde el backend como JSON seguro
    const nodosData = JSON.parse(`{{ nodos_data|escapejs }}`);
    const conexionesData = JSON.parse(`{{ conexiones_data|escapejs }}`);

    // Agregar nodos al mapa
    const nodeLayer = L.geoJSON(nodosData, {
        pointToLayer: function (feature, latlng) {
            const marker = L.circleMarker(latlng, {
                radius: 5,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });

            const tooltipContent = `ID: ${feature.id || "No disponible"}`;
            marker.bindTooltip(tooltipContent, {
                permanent: false,
                direction: "top",
                offset: L.point(0, -5)
            });

            marker.on("mouseover", function () {
                this.setStyle({ radius: 8, fillColor: "#ff0000" });
            });
            marker.on("mouseout", function () {
                this.setStyle({ radius: 5, fillColor: "#ff7800" });
            });
            return marker;
        }
    }).addTo(map);

    // Agregar conexiones al mapa
    const edgeLayer = L.geoJSON(conexionesData, {
        style: {
            color: "#00bfff",
            weight: 2,
            opacity: 0.6
        }
    }).addTo(map);

    map.fitBounds(nodeLayer.getBounds());
});
document.addEventListener("DOMContentLoaded", function () {
    // Inicializa el mapa centrado en Miraflores
    const map = L.map("map").setView([-12.121, -77.03], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);
  
    let nodeLayer;
    let edgeLayer;
  
    // Función para cargar y mostrar nodos y conexiones de un distrito
    function loadDistrictData(district) {
      if (nodeLayer) map.removeLayer(nodeLayer);
      if (edgeLayer) map.removeLayer(edgeLayer);
  
      // Utiliza `{{ static_url }}` como prefijo para las rutas de los archivos
      const nodeFile = `/static/Datos_Lima/${district}_nodos.json`;
      const edgeFile = `/static/Datos_Lima/${district}_conexiones.json`;
  
      fetch(nodeFile)
        .then((response) => response.json())
        .then((nodes) => {
          nodeLayer = L.geoJSON(nodes, {
            pointToLayer: function (feature, latlng) {
              const marker = L.circleMarker(latlng, {
                radius: 5,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8,
              });
  
              const tooltipContent = `ID: ${feature.id || "No disponible"}`;
              marker.bindTooltip(tooltipContent, {
                permanent: false,
                direction: "top",
                offset: L.point(0, -5),
              });
  
              marker.on("mouseover", function () {
                this.setStyle({ radius: 8, fillColor: "#ff0000" });
              });
              marker.on("mouseout", function () {
                this.setStyle({ radius: 5, fillColor: "#ff7800" });
              });
              return marker;
            },
          }).addTo(map);
  
          map.fitBounds(nodeLayer.getBounds());
  
          fetch(edgeFile)
            .then((response) => response.json())
            .then((edges) => {
              edgeLayer = L.geoJSON(edges, {
                style: {
                  color: "#00bfff",
                  weight: 2,
                  opacity: 0.6,
                },
              }).addTo(map);
            })
            .catch((error) => console.error(`Error al cargar las conexiones: ${error}`));
        })
        .catch((error) => console.error(`Error al cargar los nodos: ${error}`));
    }
  
    loadDistrictData("Miraflores");
  
    // Mostrar botón cuando se selecciona un distrito
    const viewGraphButton = document.getElementById("view-graph");
    document.getElementById("district-select").addEventListener("change", function () {
        const selectedDistrict = this.value;
        if (selectedDistrict) {
          viewGraphButton.style.display = "block";
          viewGraphButton.href = `/graph/${selectedDistrict}/`;
          viewGraphButton.target = "_blank"; // Añade esto también
          loadDistrictData(selectedDistrict);
        } else {
          viewGraphButton.style.display = "none";
        }
      });
  });
  
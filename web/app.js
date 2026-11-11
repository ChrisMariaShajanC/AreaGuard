const TYPE_NAMES = { DF: "Debris flow", SS: "Surficial slide", RF: "Rock fall" };

const map = L.map("map").setView([10.85, 76.27], 7);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

const markerLayer = L.layerGroup().addTo(map);

const state = {
  geojson: null,
  selectedDistrict: "all",
  selectedTypes: new Set(["DF", "SS", "RF"]),
};

const els = {
  districtFilter: document.getElementById("district-filter"),
  typeChecks: document.querySelectorAll('.type-filter input[type="checkbox"]'),
  loading: document.getElementById("loading-state"),
  error: document.getElementById("error-state"),
  empty: document.getElementById("empty-state"),
  retry: document.getElementById("retry-btn"),
  status: document.getElementById("data-status"),
  total: document.getElementById("stat-total"),
  districts: document.getElementById("stat-districts"),
  df: document.getElementById("stat-df"),
  ss: document.getElementById("stat-ss"),
  rf: document.getElementById("stat-rf"),
  zeroArea: document.getElementById("stat-zero-area"),
  zeroLw: document.getElementById("stat-zero-lw"),
  terrain: document.getElementById("terrain-info"),
};

function showState(name) {
  els.loading.classList.toggle("hidden", name !== "loading");
  els.error.classList.toggle("hidden", name !== "error");
  els.empty.classList.toggle("hidden", name !== "empty");
}

function formatValue(v) {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") return Number.isInteger(v) ? v.toLocaleString() : v.toFixed(2);
  return String(v);
}

function popupHtml(p) {
  const rows = [
    ["No", p.No],
    ["District", p.District],
    ["Type", `${p.Type_of_sl} — ${TYPE_NAMES[p.Type_of_sl] || ""}`],
    ["NRSC", p.NRSC],
    ["GSI", p.GSI],
    ["Newly mapped", p.New],
    ["Length (m)", p.Length],
    ["Width (m)", p.Width],
    ["Area (m²)", p.Area],
    ["Buildings impacted", p.Building_I],
    ["Road impact", p.Road_impac],
    ["Agriculture impact", p.Impact_Agr],
    ["Land use 2010", p.LU_2010],
    ["Land use 2018", p.LU_2018],
    ["Reason code", p.Specific_r],
    ["Remarks", p.Remarks],
    ["Longitude", p.POINT_X],
    ["Latitude", p.POINT_Y],
    ["Reclassified slope", p.Reclass_Sl],
    ["Slope (°)", p.RASTERVALU],
    ["Elevation (m)", p.elevation_m],
    ["Slope (°, terrain)", p.slope_deg],
    ["Aspect (°)", p.aspect_deg],
    ["Terrain status", p.terrain_status],
  ];
  return rows
    .map(([k, v]) => `<div class="popup-row"><span class="popup-key">${k}</span><span class="popup-val">${formatValue(v)}</span></div>`)
    .join("");
}

function filteredFeatures() {
function showTerrain(p) {
  const rows = [
    ["Elevation (m)", formatValue(p.elevation_m)],
    ["Slope (°)", formatValue(p.slope_deg)],
    ["Aspect (°)", formatValue(p.aspect_deg)],
    ["Status", formatValue(p.terrain_status)],
    ["DEM source", formatValue(p.dem_source)],
  ];
  els.terrain.innerHTML = rows
    .map(([k, v]) => `<div class="t-row"><span class="t-key">${k}</span><span class="t-val">${v}</span></div>`)
    .join("");
}


  if (!state.geojson) return [];
  return state.geojson.features.filter((f) => {
    const p = f.properties;
    if (state.selectedDistrict !== "all" && p.District !== state.selectedDistrict) return false;
    if (!state.selectedTypes.has(p.Type_of_sl)) return false;
    return true;
  });
}

function updateStats(features) {
  els.total.textContent = features.length.toLocaleString();
  els.districts.textContent = new Set(features.map((f) => f.properties.District)).size;
  els.df.textContent = features.filter((f) => f.properties.Type_of_sl === "DF").length.toLocaleString();
  els.ss.textContent = features.filter((f) => f.properties.Type_of_sl === "SS").length.toLocaleString();
  els.rf.textContent = features.filter((f) => f.properties.Type_of_sl === "RF").length.toLocaleString();
  els.zeroArea.textContent = features.filter((f) => f.properties.Area === 0).length.toLocaleString();
  els.zeroLw.textContent = features.filter((f) => f.properties.Length === 0 && f.properties.Width === 0).length.toLocaleString();
}

function renderMarkers(features) {
  markerLayer.clearLayers();
  if (features.length === 0) {
    showState("empty");
    return;
  }
  showState(null);
  features.forEach((f) => {
    const [lon, lat] = f.geometry.coordinates;
    const marker = L.circleMarker([lat, lon], {
      radius: 4,
      color: "#1d4ed8",
      weight: 1,
      fillColor: "#3b82f6",
      fillOpacity: 0.7,
    });
    marker.bindPopup(popupHtml(f.properties), { maxWidth: 320 });
    marker.on("click", () => showTerrain(f.properties));
    marker.addTo(markerLayer);
  });
}

function applyFilters() {
  const features = filteredFeatures();
  updateStats(features);
  renderMarkers(features);
}

function populateDistricts(features) {
  const districts = [...new Set(features.map((f) => f.properties.District))].sort();
  districts.forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = d;
    els.districtFilter.appendChild(opt);
  });
}

async function loadData() {
  showState("loading");
  try {
    const res = await fetch("/api/landslides");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.geojson = await res.json();
    populateDistricts(state.geojson.features);
    els.status.textContent = `${state.geojson.features.length.toLocaleString()} records loaded`;
    applyFilters();
  } catch (err) {
    console.error(err);
    showState("error");
    els.status.textContent = "Failed to load";
  }
}

els.districtFilter.addEventListener("change", (e) => {
  state.selectedDistrict = e.target.value;
  applyFilters();
});

els.typeChecks.forEach((cb) => {
  cb.addEventListener("change", () => {
    state.selectedTypes.clear();
    els.typeChecks.forEach((c) => { if (c.checked) state.selectedTypes.add(c.value); });
    applyFilters();
  });
});

els.retry.addEventListener("click", loadData);

loadData();
"""
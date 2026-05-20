// World map statistics visualization using Chart.js + chartjs-chart-geo
(function () {
  'use strict';

  // UN numeric id → ISO 3166-1 alpha-2 (covers all countries in topojson 110m)
  var N2A = {
    "4":"AF","8":"AL","12":"DZ","24":"AO","32":"AR","36":"AU","40":"AT","50":"BD",
    "56":"BE","68":"BO","76":"BR","100":"BG","104":"MM","116":"KH","120":"CM",
    "124":"CA","140":"CF","144":"LK","152":"CL","156":"CN","170":"CO","180":"CD",
    "188":"CR","191":"HR","192":"CU","196":"CY","203":"CZ","208":"DK","214":"DO",
    "218":"EC","818":"EG","222":"SV","233":"EE","231":"ET","246":"FI","250":"FR",
    "266":"GA","276":"DE","288":"GH","300":"GR","320":"GT","324":"GN","332":"HT",
    "340":"HN","348":"HU","356":"IN","360":"ID","364":"IR","368":"IQ","372":"IE",
    "376":"IL","380":"IT","388":"JM","392":"JP","400":"JO","398":"KZ","404":"KE",
    "408":"KP","410":"KR","414":"KW","418":"LA","422":"LB","430":"LR","434":"LY",
    "440":"LT","442":"LU","450":"MG","454":"MW","458":"MY","484":"MX","504":"MA",
    "508":"MZ","516":"NA","524":"NP","528":"NL","554":"NZ","558":"NI","562":"NE",
    "566":"NG","578":"NO","586":"PK","591":"PA","598":"PG","600":"PY","604":"PE",
    "608":"PH","616":"PL","620":"PT","642":"RO","643":"RU","646":"RW","682":"SA",
    "686":"SN","694":"SL","706":"SO","710":"ZA","724":"ES","729":"SD","752":"SE",
    "756":"CH","760":"SY","764":"TH","792":"TR","800":"UG","804":"UA","784":"AE",
    "826":"GB","840":"US","858":"UY","860":"UZ","862":"VE","704":"VN","887":"YE",
    "894":"ZM","716":"ZW","51":"AM","31":"AZ","112":"BY","70":"BA","795":"TM",
    "762":"TJ","496":"MN","498":"MD","703":"SK","705":"SI","688":"RS","807":"MK"
  };

  // English country name → ISO alpha-2 (for matching against country_distribution names)
  var NAME_TO_A2 = {
    "Afghanistan":"AF","Albania":"AL","Algeria":"DZ","Angola":"AO","Argentina":"AR",
    "Armenia":"AM","Australia":"AU","Austria":"AT","Azerbaijan":"AZ","Bahamas":"BS",
    "Bahrain":"BH","Bangladesh":"BD","Belarus":"BY","Belgium":"BE","Bolivia":"BO",
    "Bosnia and Herzegovina":"BA","Botswana":"BW","Brazil":"BR","Bulgaria":"BG",
    "Burkina Faso":"BF","Cambodia":"KH","Cameroon":"CM","Canada":"CA","Chad":"TD",
    "Chile":"CL","China":"CN","Colombia":"CO","Congo":"CG","Costa Rica":"CR",
    "Croatia":"HR","Cuba":"CU","Czechia":"CZ","DR Congo":"CD","Denmark":"DK",
    "Dominican Republic":"DO","Ecuador":"EC","Egypt":"EG","El Salvador":"SV",
    "Equatorial Guinea":"GQ","Estonia":"EE","Ethiopia":"ET","Finland":"FI","France":"FR",
    "Gabon":"GA","Georgia":"GE","Germany":"DE","Ghana":"GH","Greece":"GR",
    "Guatemala":"GT","Guinea":"GN","Haiti":"HT","Honduras":"HN","Hungary":"HU",
    "Iceland":"IS","India":"IN","Indonesia":"ID","Iran":"IR","Iraq":"IQ","Ireland":"IE",
    "Israel":"IL","Italy":"IT","Jamaica":"JM","Japan":"JP","Jordan":"JO",
    "Kazakhstan":"KZ","Kenya":"KE","Kosovo":"XK","Kyrgyzstan":"KG","Laos":"LA",
    "Latvia":"LV","Lebanon":"LB","Liberia":"LR","Libya":"LY","Lithuania":"LT",
    "Luxembourg":"LU","Madagascar":"MG","Malawi":"MW","Malaysia":"MY","Mali":"ML",
    "Mauritania":"MR","Mexico":"MX","Moldova":"MD","Mongolia":"MN","Morocco":"MA",
    "Mozambique":"MZ","Myanmar":"MM","Namibia":"NA","Nepal":"NP","Netherlands":"NL",
    "New Zealand":"NZ","Nicaragua":"NI","Niger":"NE","Nigeria":"NG","North Korea":"KP",
    "North Macedonia":"MK","Norway":"NO","Oman":"OM","Pakistan":"PK","Panama":"PA",
    "Papua New Guinea":"PG","Paraguay":"PY","Peru":"PE","Philippines":"PH","Poland":"PL",
    "Portugal":"PT","Qatar":"QA","Romania":"RO","Russia":"RU","Rwanda":"RW",
    "Saudi Arabia":"SA","Senegal":"SN","Serbia":"RS","Sierra Leone":"SL","Slovakia":"SK",
    "Slovenia":"SI","Somalia":"SO","South Africa":"ZA","South Korea":"KR","South Sudan":"SS",
    "Spain":"ES","Sri Lanka":"LK","Sudan":"SD","Suriname":"SR","Sweden":"SE",
    "Switzerland":"CH","Syria":"SY","Taiwan":"TW","Tajikistan":"TJ","Tanzania":"TZ",
    "Thailand":"TH","Togo":"TG","Trinidad and Tobago":"TT","Tunisia":"TN","Turkey":"TR",
    "Turkmenistan":"TM","Uganda":"UG","Ukraine":"UA","United Arab Emirates":"AE",
    "United Kingdom":"GB","United States":"US","Uruguay":"UY","Uzbekistan":"UZ",
    "Venezuela":"VE","Vietnam":"VN","Yemen":"YE","Zambia":"ZM","Zimbabwe":"ZW",
    "Cote d'Ivoire":"CI","Ivory Coast":"CI","Eswatini":"SZ"
  };

  var worldCache = null;

  function getWorld() {
    if (worldCache) return Promise.resolve(worldCache);
    return fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
      .then(function(r) { return r.json(); })
      .then(function(d) { worldCache = d; return d; });
  }

  // Track Chart instances so we can destroy before re-creating
  var chartInstances = {};

  function buildChoropleth(container, countryNameData) {
    // countryNameData = { "United States": 5, "Japan": 3, ... }

    // Convert name-keyed data → alpha-2 keyed
    var alpha2Data = {};
    Object.keys(countryNameData).forEach(function(name) {
      var code = NAME_TO_A2[name];
      if (code) alpha2Data[code] = countryNameData[name];
    });

    if (!Object.keys(alpha2Data).length) {
      container.innerHTML = '<p class="text-gray-400 text-center py-8">No geographic data available for this media type yet.</p>';
      return;
    }

    // Create canvas
    container.innerHTML = '<canvas style="width:100%;max-height:480px;"></canvas>';
    var canvas = container.querySelector('canvas');
    var canvasId = container.id + '-canvas';
    canvas.id = canvasId;

    if (chartInstances[canvasId]) {
      chartInstances[canvasId].destroy();
      delete chartInstances[canvasId];
    }

    var maxVal = Math.max.apply(null, Object.values(alpha2Data).concat([1]));

    getWorld().then(function(wd) {
      var countries = ChartGeo.topojson.feature(wd, wd.objects.countries);

      var chartData = countries.features.map(function(f) {
        var a2 = N2A[String(f.id)];
        return { feature: f, value: a2 ? (alpha2Data[a2] || 0) : 0 };
      });

      var labels = countries.features.map(function(f) {
        var a2 = N2A[String(f.id)];
        if (!a2) return f.properties && f.properties.name || String(f.id);
        // find the name from our data or fall back to code
        var found = Object.keys(NAME_TO_A2).find(function(n) { return NAME_TO_A2[n] === a2; });
        return found || a2;
      });

      chartInstances[canvasId] = new Chart(canvas, {
        type: 'choropleth',
        data: {
          labels: labels,
          datasets: [{
            label: 'Items',
            data: chartData,
            backgroundColor: function(ctx) {
              var v = ctx.raw ? ctx.raw.value : 0;
              if (!v) return 'rgba(55,65,81,0.4)';
              var t = v / maxVal;
              // indigo gradient
              var r = Math.round(99  + (1 - t) * 80);
              var g = Math.round(102 + (1 - t) * 50);
              var b = Math.round(241 - (1 - t) * 60);
              return 'rgba(' + r + ',' + g + ',' + b + ',0.9)';
            },
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(ctx) {
                  var v = ctx.raw ? ctx.raw.value : 0;
                  return v ? v + ' item' + (v !== 1 ? 's' : '') : 'No items';
                },
              },
            },
          },
          scales: {
            projection: { axis: 'x', projection: 'naturalEarth1' },
            color: { display: false },
          },
        },
      });
    });
  }

  // Load chartjs-chart-geo from CDN (Chart.js is already loaded as a local static)
  function loadGeo(cb) {
    if (window.ChartGeo) { cb(); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/chartjs-chart-geo@4/build/index.umd.min.js';
    s.onload = cb;
    document.head.appendChild(s);
  }

  document.addEventListener('DOMContentLoaded', function() {
    var mediaTypeButtons = document.querySelectorAll('[data-media-type-btn]');
    var worldMapContainer = document.getElementById('world-map-container');

    if (!mediaTypeButtons.length || !worldMapContainer) return;

    loadGeo(function() {
      function showMap(mediaType) {
        // Hide all map divs
        document.querySelectorAll('.world-map-view').forEach(function(el) {
          el.style.display = 'none';
        });

        var mapEl = document.getElementById('map-' + mediaType);
        if (!mapEl) return;
        mapEl.style.display = 'block';

        // Only build once
        if (mapEl.dataset.built) return;
        mapEl.dataset.built = '1';

        var dataEl = document.getElementById('country-data-' + mediaType);
        var countryData = {};
        if (dataEl) {
          try { countryData = JSON.parse(dataEl.textContent); } catch(e) {}
        }

        buildChoropleth(mapEl, countryData);
      }

      // Activate first tab
      var firstBtn = mediaTypeButtons[0];
      if (firstBtn) {
        firstBtn.classList.add('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
        showMap(firstBtn.dataset.mediaTypeBtn);
      }

      mediaTypeButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
          mediaTypeButtons.forEach(function(b) {
            b.classList.remove('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
          });
          btn.classList.add('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
          showMap(btn.dataset.mediaTypeBtn);
        });
      });
    });
  });
})();

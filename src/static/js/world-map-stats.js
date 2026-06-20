// World map statistics visualization — dot/bubble map (like RateYourMusic)
(function () {
  'use strict';

  // Unused N2A kept only as tombstone — bubbleMap uses lat/lon, not feature IDs
  var _N2A_UNUSED = {
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

  // English country name → ISO alpha-2
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

  // ISO alpha-2 → [latitude, longitude] country centroids
  var A2_CENTROID = {
    "AD":[42.55,1.57],"AE":[23.42,53.85],"AF":[33.94,67.71],"AG":[17.06,-61.80],
    "AL":[41.15,20.17],"AM":[40.07,45.04],"AO":[-11.20,17.87],"AR":[-38.42,-63.62],
    "AT":[47.52,14.55],"AU":[-25.27,133.78],"AZ":[40.14,47.58],"BA":[43.92,17.68],
    "BB":[13.19,-59.54],"BD":[23.68,90.36],"BE":[50.50,4.47],"BF":[12.36,-1.56],
    "BG":[42.73,25.49],"BH":[26.00,50.55],"BI":[-3.37,29.92],"BJ":[9.31,2.32],
    "BN":[4.54,114.73],"BO":[-16.29,-63.59],"BR":[-14.24,-51.93],"BS":[25.03,-77.40],
    "BT":[27.51,90.43],"BW":[-22.33,24.68],"BY":[53.71,27.95],"BZ":[17.19,-88.50],
    "CA":[56.13,-106.35],"CD":[-4.04,21.76],"CF":[6.61,20.94],"CG":[-0.23,15.83],
    "CH":[46.82,8.23],"CI":[7.54,-5.55],"CL":[-35.68,-71.54],"CM":[3.85,11.50],
    "CN":[35.86,104.20],"CO":[4.57,-74.30],"CR":[9.75,-83.75],"CU":[21.52,-77.78],
    "CV":[16.54,-23.04],"CY":[35.13,33.43],"CZ":[49.82,15.47],"DE":[51.17,10.45],
    "DJ":[11.83,42.59],"DK":[56.26,9.50],"DM":[15.41,-61.37],"DO":[18.74,-70.16],
    "DZ":[28.03,1.66],"EC":[-1.83,-78.18],"EE":[58.60,25.01],"EG":[26.82,30.80],
    "ER":[15.18,39.78],"ES":[40.46,-3.75],"ET":[9.15,40.49],"FI":[61.92,25.75],
    "FJ":[-17.71,178.07],"FR":[46.23,2.21],"GA":[-0.80,11.61],"GB":[55.38,-3.44],
    "GD":[12.12,-61.68],"GE":[42.32,43.36],"GH":[7.95,-1.02],"GM":[13.44,-15.31],
    "GN":[9.95,-11.61],"GQ":[1.65,10.27],"GR":[39.07,21.82],"GT":[15.78,-90.23],
    "GW":[11.80,-15.18],"GY":[4.86,-58.93],"HN":[15.20,-86.24],"HR":[45.10,15.20],
    "HT":[18.97,-72.29],"HU":[47.16,19.50],"ID":[-0.79,113.92],"IE":[53.41,-8.24],
    "IL":[31.05,34.85],"IN":[20.59,78.96],"IQ":[33.22,43.68],"IR":[32.43,53.69],
    "IS":[64.96,-19.02],"IT":[41.87,12.57],"JM":[18.11,-77.30],"JO":[30.59,36.24],
    "JP":[36.20,138.25],"KE":[-0.02,37.91],"KG":[41.20,74.77],"KH":[12.57,104.99],
    "KI":[-3.37,-168.73],"KM":[-11.88,43.87],"KN":[17.36,-62.78],"KP":[40.34,127.51],
    "KR":[35.91,127.77],"KW":[29.31,47.48],"KZ":[48.02,66.92],"LA":[19.86,102.50],
    "LB":[33.85,35.86],"LC":[13.91,-60.97],"LI":[47.17,9.56],"LK":[7.87,80.77],
    "LR":[6.43,-9.43],"LS":[-29.61,28.23],"LT":[55.17,23.88],"LU":[49.82,6.13],
    "LV":[56.88,24.60],"LY":[26.34,17.23],"MA":[31.79,-7.09],"MC":[43.75,7.40],
    "MD":[47.41,28.37],"ME":[42.71,19.37],"MG":[-18.77,46.87],"MH":[7.13,171.18],
    "MK":[41.61,21.75],"ML":[17.57,-3.99],"MM":[21.91,95.96],"MN":[46.86,103.85],
    "MR":[21.01,-10.94],"MT":[35.94,14.38],"MU":[-20.35,57.55],"MV":[3.20,73.22],
    "MW":[-13.25,34.30],"MX":[23.63,-102.55],"MY":[4.21,101.98],"MZ":[-18.67,35.53],
    "NA":[-22.96,18.49],"NE":[17.61,8.08],"NG":[9.08,8.68],"NI":[12.87,-85.21],
    "NL":[52.13,5.29],"NO":[60.47,8.47],"NP":[28.39,84.12],"NR":[-0.52,166.93],
    "NZ":[-40.90,174.89],"OM":[21.51,55.92],"PA":[8.54,-80.78],"PE":[-9.19,-75.02],
    "PG":[-6.31,143.96],"PH":[12.88,121.77],"PK":[30.38,69.35],"PL":[51.92,19.15],
    "PT":[39.40,-8.22],"PW":[7.52,134.58],"PY":[-23.44,-58.44],"QA":[25.35,51.18],
    "RO":[45.94,24.97],"RS":[44.02,21.01],"RU":[61.52,105.32],"RW":[-1.94,29.87],
    "SA":[23.89,45.08],"SB":[-9.65,160.16],"SC":[-4.68,55.49],"SD":[12.86,30.22],
    "SE":[60.13,18.64],"SG":[1.35,103.82],"SI":[46.15,14.99],"SK":[48.67,19.70],
    "SL":[8.46,-11.78],"SM":[43.94,12.46],"SN":[14.50,-14.45],"SO":[5.15,46.20],
    "SR":[3.92,-56.03],"SS":[6.88,31.31],"ST":[0.19,6.61],"SV":[13.79,-88.90],
    "SY":[34.80,38.99],"SZ":[-26.52,31.47],"TD":[15.45,18.73],"TG":[8.62,0.82],
    "TH":[15.87,100.99],"TJ":[38.86,71.28],"TL":[-8.87,125.73],"TM":[38.97,59.56],
    "TN":[33.89,9.54],"TO":[-21.18,-175.20],"TR":[38.96,35.24],"TT":[10.69,-61.22],
    "TV":[-7.11,177.65],"TZ":[-6.37,34.89],"UA":[48.38,31.17],"UG":[1.37,32.29],
    "US":[37.09,-95.71],"UY":[-32.52,-55.77],"UZ":[41.38,64.59],"VA":[41.90,12.45],
    "VC":[12.98,-61.29],"VE":[6.42,-66.59],"VN":[14.06,108.28],"VU":[-15.38,166.96],
    "WS":[-13.76,-172.10],"YE":[15.55,48.52],"ZA":[-30.56,22.94],"ZM":[-13.13,27.85],
    "ZW":[-19.02,29.15]
  };

  var worldCache = null;

  function getWorld() {
    if (worldCache) return Promise.resolve(worldCache);
    return fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
      .then(function(r) { return r.json(); })
      .then(function(d) { worldCache = d; return d; });
  }

  var chartInstances = {};

  function showCountryList(container) {
    var mediaType = container.id.replace(/^map-/, '');
    var list = document.getElementById('country-list-' + mediaType);
    container.innerHTML = '';
    if (list) list.classList.remove('hidden');
  }

  function hideCountryLists() {
    document.querySelectorAll('[id^="country-list-"]').forEach(function(el) {
      el.classList.add('hidden');
    });
  }

  function buildDotMap(container, countryNameData) {
    // Convert name-keyed data → alpha-2 keyed
    var alpha2Data = {};
    Object.keys(countryNameData).forEach(function(name) {
      var code = NAME_TO_A2[name];
      if (code) alpha2Data[code] = (alpha2Data[code] || 0) + countryNameData[name];
    });

    if (!Object.keys(alpha2Data).length) {
      showCountryList(container);
      return;
    }

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
      if (!window.ChartGeo || !window.ChartGeo.topojson) {
        showCountryList(container);
        return;
      }

      var outline = ChartGeo.topojson.feature(wd, wd.objects.countries);

      var labels = [];
      var dataPoints = [];

      Object.keys(alpha2Data).forEach(function(code) {
        var centroid = A2_CENTROID[code];
        if (!centroid) return;
        var count = alpha2Data[code];
        // resolve display name from NAME_TO_A2 reverse lookup
        var name = code;
        var allNames = Object.keys(NAME_TO_A2);
        for (var i = 0; i < allNames.length; i++) {
          if (NAME_TO_A2[allNames[i]] === code) { name = allNames[i]; break; }
        }
        labels.push(name);
        dataPoints.push({
          latitude: centroid[0],
          longitude: centroid[1],
          value: count,
          name: name,
          r: Math.max(4, Math.round(4 + 18 * Math.sqrt(count / maxVal)))
        });
      });

      if (!dataPoints.length) {
        showCountryList(container);
        return;
      }

      chartInstances[canvasId] = new Chart(canvas, {
        type: 'bubbleMap',
        data: {
          labels: labels,
          datasets: [{
            label: 'Items',
            outline: outline,
            showOutline: true,
            // dark-mode country fill / border matching the app palette
            outlineBackgroundColor: 'rgba(42,47,53,0.85)',
            outlineStrokeColor: 'rgba(255,255,255,0.07)',
            outlineStrokeWidth: 0.5,
            // indigo dots
            backgroundColor: 'rgba(99,102,241,0.65)',
            borderColor: 'rgba(165,180,252,0.9)',
            borderWidth: 1.5,
            hoverBackgroundColor: 'rgba(129,140,248,0.9)',
            hoverBorderColor: 'rgba(199,210,254,1)',
            data: dataPoints
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          animation: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: function() { return ''; },
                label: function(ctx) {
                  var name = (ctx.raw && ctx.raw.name) || ctx.label || '';
                  var v = ctx.raw && ctx.raw.value != null ? ctx.raw.value : 0;
                  return name + ': ' + v + ' item' + (v !== 1 ? 's' : '');
                }
              }
            }
          },
          scales: {
            projection: { axis: 'x', projection: 'naturalEarth1' }
          }
        }
      });
    }).catch(function() {
      showCountryList(container);
    });
  }

  // Load chartjs-chart-geo from CDN (Chart.js is already loaded as a local static)
  function loadGeo(cb) {
    if (window.ChartGeo) { cb(); return; }
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/chartjs-chart-geo@4/build/index.umd.min.js';
    s.onload = cb;
    s.onerror = cb;
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
        hideCountryLists();

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

        buildDotMap(mapEl, countryData);
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

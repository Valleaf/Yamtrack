from pathlib import Path

p = Path(r"C:\yamtrack-fork\src\templates\app\statistics.html")
text = p.read_text(encoding="utf-8")

# Step 1: cut everything after {% endblock js %}
marker = "{% endblock js %}"
idx = text.find(marker)
if idx == -1:
    raise SystemExit("ERROR: endblock js not found")
clean = text[:idx + len(marker)] + "\n"
print(f"  OK  Stripped {len(text) - len(clean)} chars of junk after endblock js")

# Step 2: inject world map card before {% endblock content %}
CARD = '''
    {% if world_map.combined %}
    <div class="bg-[#2a2f35] rounded-lg p-6" x-data="{ wmTab: 'combined' }">
      <h2 class="text-xl font-semibold mb-4">Media World Map</h2>
      <div class="flex flex-wrap gap-2 mb-4">
        <button @click="wmTab = 'combined'"
                :class="wmTab === 'combined' ? 'bg-indigo-600 text-white' : 'bg-[#39404b] text-gray-300 hover:bg-[#434b57]'"
                class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors cursor-pointer">All</button>
        {% for mt in world_map.media_types %}
        <button @click="wmTab = '{{ mt }}'"
                :class="wmTab === '{{ mt }}' ? 'bg-indigo-600 text-white' : 'bg-[#39404b] text-gray-300 hover:bg-[#434b57]'"
                class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors cursor-pointer">{{ mt|title }}</button>
        {% endfor %}
      </div>
      <div style="min-height:320px;">
        <canvas id="worldmap-combined" x-show="wmTab === 'combined'" class="w-full" style="max-height:440px;"></canvas>
        {% for mt in world_map.media_types %}
        <canvas id="worldmap-{{ mt }}" x-show="wmTab === '{{ mt }}'" class="w-full" style="max-height:440px;"></canvas>
        {% endfor %}
      </div>
    </div>
    {% endif %}
'''

ENDBLOCK_CONTENT = "{% endblock content %}"
pos = clean.rfind(ENDBLOCK_CONTENT)
if pos == -1:
    raise SystemExit("ERROR: endblock content not found")
clean = clean[:pos] + CARD + clean[pos:]
print("  OK  Injected world map card inside block content")

# Step 3: inject world map scripts before {% endblock js %}
SCRIPTS = '''
  {% if world_map.combined %}
  {{ world_map.combined|json_script:"wm-combined" }}
  {{ world_map.by_type|json_script:"wm-by-type" }}
  {{ world_map.country_names|json_script:"wm-names" }}
  {{ world_map.media_types|json_script:"wm-types" }}
  <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-geo@4/build/index.umd.min.js"></script>
  <script>
  (function () {
    var combined = JSON.parse(document.getElementById('wm-combined').textContent);
    var byType   = JSON.parse(document.getElementById('wm-by-type').textContent);
    var names    = JSON.parse(document.getElementById('wm-names').textContent);
    var N2A = {"4":"AF","8":"AL","12":"DZ","24":"AO","32":"AR","36":"AU","40":"AT","50":"BD","56":"BE","68":"BO","76":"BR","100":"BG","104":"MM","116":"KH","120":"CM","124":"CA","140":"CF","144":"LK","152":"CL","156":"CN","170":"CO","180":"CD","188":"CR","191":"HR","192":"CU","196":"CY","203":"CZ","208":"DK","214":"DO","218":"EC","818":"EG","222":"SV","233":"EE","231":"ET","246":"FI","250":"FR","266":"GA","276":"DE","288":"GH","300":"GR","320":"GT","324":"GN","332":"HT","340":"HN","348":"HU","356":"IN","360":"ID","364":"IR","368":"IQ","372":"IE","376":"IL","380":"IT","388":"JM","392":"JP","400":"JO","398":"KZ","404":"KE","408":"KP","410":"KR","414":"KW","418":"LA","422":"LB","430":"LR","434":"LY","440":"LT","442":"LU","450":"MG","454":"MW","458":"MY","484":"MX","504":"MA","508":"MZ","516":"NA","524":"NP","528":"NL","554":"NZ","558":"NI","562":"NE","566":"NG","578":"NO","586":"PK","591":"PA","598":"PG","600":"PY","604":"PE","608":"PH","616":"PL","620":"PT","642":"RO","643":"RU","646":"RW","682":"SA","686":"SN","694":"SL","706":"SO","710":"ZA","724":"ES","729":"SD","752":"SE","756":"CH","760":"SY","764":"TH","792":"TR","800":"UG","804":"UA","784":"AE","826":"GB","840":"US","858":"UY","860":"UZ","862":"VE","704":"VN","887":"YE","894":"ZM","716":"ZW","51":"AM","31":"AZ","112":"BY","70":"BA","795":"TM","762":"TJ","496":"MN","498":"MD","703":"SK","705":"SI","688":"RS","807":"MK"};
    var worldCache = null;
    function getWorld() {
      if (worldCache) return Promise.resolve(worldCache);
      return fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then(function(r){return r.json();}).then(function(d){worldCache=d;return d;});
    }
    function buildMap(canvasId, data) {
      var canvas = document.getElementById(canvasId);
      if (!canvas || canvas._wm) return;
      canvas._wm = true;
      getWorld().then(function(wd) {
        var countries = ChartGeo.topojson.feature(wd, wd.objects.countries);
        var vals = Object.values(data);
        var maxVal = vals.length ? Math.max.apply(null, vals.concat([1])) : 1;
        var chartData = countries.features.map(function(f) {
          var a = N2A[String(f.id)];
          return {feature: f, value: a ? (data[a] || 0) : 0};
        });
        new Chart(canvas, {
          type: 'choropleth',
          data: {
            labels: countries.features.map(function(f) {
              var a = N2A[String(f.id)];
              return a ? (names[a] || a) : (f.properties && f.properties.name || String(f.id));
            }),
            datasets: [{
              label: 'Items',
              data: chartData,
              backgroundColor: function(ctx) {
                var v = ctx.raw ? ctx.raw.value : 0;
                if (!v) return 'rgba(55,65,81,0.5)';
                var t = v / maxVal;
                var r = Math.round(99  + (1-t)*60);
                var g = Math.round(102 + (1-t)*40);
                var b = Math.round(241 - (1-t)*60);
                return 'rgba('+r+','+g+','+b+',0.85)';
              }
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: {display: false},
              tooltip: {callbacks: {label: function(ctx) {
                var v = ctx.raw ? ctx.raw.value : 0;
                return v ? v + ' item' + (v !== 1 ? 's' : '') : 'No items tracked';
              }}}
            },
            scales: {
              projection: {axis: 'x', projection: 'naturalEarth1'},
              color: {display: false}
            }
          }
        });
      });
    }
    window.__wmBuild   = buildMap;
    window.__wmByType  = byType;
    buildMap('worldmap-combined', combined);
    document.addEventListener('alpine:initialized', function() {
      document.querySelectorAll('[id^="worldmap-"]').forEach(function(canvas) {
        canvas.addEventListener('x-show-changed', function() {
          if (!canvas.hidden) {
            var mt = canvas.id.replace('worldmap-', '');
            buildMap(canvas.id, byType[mt] || {});
          }
        });
      });
    });
  })();
  </script>
  {% endif %}
'''

pos2 = clean.rfind("{% endblock js %}")
clean = clean[:pos2] + SCRIPTS + clean[pos2:]
print("  OK  Injected world map scripts inside block js")

p.write_text(clean, encoding="utf-8")
print("  OK  File written")

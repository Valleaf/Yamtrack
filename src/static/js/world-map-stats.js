// World map statistics visualization
document.addEventListener("DOMContentLoaded", function() {
  const mediaTypeButtons = document.querySelectorAll('[data-media-type-btn]');
  const worldMapContainer = document.getElementById('world-map-container');
  
  if (!mediaTypeButtons.length || !worldMapContainer) {
    return;
  }

  // Initialize with first available media type
  const firstButton = mediaTypeButtons[0];
  if (firstButton) {
    showMediaTypeMap(firstButton.dataset.mediaTypeBtn);
    firstButton.classList.add('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
  }

  // Add click handlers
  mediaTypeButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      mediaTypeButtons.forEach(btn => {
        btn.classList.remove('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
      });
      // Add active class to clicked button
      this.classList.add('bg-indigo-600/20', 'text-indigo-400', 'border-indigo-500');
      // Show map for this media type
      showMediaTypeMap(this.dataset.mediaTypeBtn);
    });
  });

  function showMediaTypeMap(mediaType) {
    // Hide all maps
    document.querySelectorAll('.world-map-view').forEach(map => {
      map.style.display = 'none';
    });
    
    const mapElement = document.getElementById(`map-${mediaType}`);
    if (!mapElement) return;
    
    mapElement.style.display = 'block';

    // Get country data for this media type
    const dataElement = document.getElementById(`country-data-${mediaType}`);
    let countryData = {};
    
    if (dataElement) {
      try {
        countryData = JSON.parse(dataElement.textContent);
      } catch (e) {
        console.warn('Failed to parse country data for', mediaType);
      }
    }

    // Create world map visualization
    if (Object.keys(countryData).length > 0 && mapElement.innerHTML === '') {
      createWorldMap(mapElement, countryData, mediaType);
    }
  }

  function createWorldMap(container, countryData, mediaType) {
    if (!Object.keys(countryData).length) {
      container.innerHTML = `
        <div class="flex flex-col items-center justify-center py-16">
          <div class="bg-[#39404b] rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 003 16.382V5.618a1 1 0 011.553-.894L9 7m0 0l6-3m-6 3v13m6-13l5.447-2.724A1 1 0 0021 5.618v10.764a1 1 0 01-1.553.894L15 13"></path>
            </svg>
          </div>
          <h3 class="text-lg font-medium mb-2">No geographic data available</h3>
          <p class="text-gray-400 text-center max-w-md">Country metadata will appear here as media is tracked from providers.</p>
        </div>
      `;
      return;
    }

    // Create a list showing country distribution sorted by count
    const countryList = Object.entries(countryData)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 25); // Show top 25 countries

    const maxCount = Math.max(...countryList.map(([_, count]) => count));

    let html = '<div class="space-y-3">';
    countryList.forEach(([country, count], index) => {
      const percentage = ((count / maxCount) * 100);
      const width = Math.max(percentage, 5);
      
      // Color gradient based on rank
      let colorClass = 'from-indigo-600 to-indigo-400';
      if (index < 3) {
        colorClass = index === 0 ? 'from-yellow-500 to-yellow-400' : index === 1 ? 'from-gray-300 to-gray-200' : 'from-orange-600 to-orange-500';
      }
      
      html += `
        <div class="space-y-1">
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-2">
              <span class="text-xs font-semibold text-gray-500 w-6 text-right">#${index + 1}</span>
              <span class="text-gray-300 font-medium truncate">🌍 ${country}</span>
            </div>
            <span class="text-gray-400 bg-[#39404b] px-2 py-0.5 rounded text-xs font-semibold whitespace-nowrap ml-2">${count}</span>
          </div>
          <div class="h-2 bg-[#39404b] rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r ${colorClass} rounded-full transition-all duration-300" style="width: ${width}%"></div>
          </div>
        </div>
      `;
    });
    html += '</div>';

    container.innerHTML = html;
  }
});


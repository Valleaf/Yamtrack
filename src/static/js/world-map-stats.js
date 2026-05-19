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
    firstButton.classList.add('active');
  }

  // Add click handlers
  mediaTypeButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Remove active class from all buttons
      mediaTypeButtons.forEach(btn => btn.classList.remove('active'));
      // Add active class to clicked button
      this.classList.add('active');
      // Show map for this media type
      showMediaTypeMap(this.dataset.mediaTypeBtn);
    });
  });

  function showMediaTypeMap(mediaType) {
    const mapElement = document.getElementById(`map-${mediaType}`);
    if (!mapElement) return;

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

    // Create SVG-based world map with simple color coding
    createWorldMap(mapElement, countryData, mediaType);
  }

  function createWorldMap(container, countryData, mediaType) {
    container.innerHTML = '';
    
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

    // Create a table showing country distribution
    const countryList = Object.entries(countryData)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20);

    const maxCount = Math.max(...countryList.map(([_, count]) => count));

    let html = '<div class="space-y-3">';
    countryList.forEach(([country, count]) => {
      const percentage = ((count / maxCount) * 100);
      const width = Math.max(percentage, 5); // Minimum 5% for visibility
      
      html += `
        <div class="space-y-1">
          <div class="flex justify-between text-sm">
            <span class="text-gray-300 font-medium">🌍 ${country}</span>
            <span class="text-gray-400 bg-[#39404b] px-2 py-0.5 rounded text-xs">${count}</span>
          </div>
          <div class="h-2 bg-[#39404b] rounded-full overflow-hidden">
            <div class="h-full bg-gradient-to-r from-indigo-500 to-indigo-400 rounded-full" style="width: ${width}%"></div>
          </div>
        </div>
      `;
    });
    html += '</div>';

    container.innerHTML = html;
  }
});

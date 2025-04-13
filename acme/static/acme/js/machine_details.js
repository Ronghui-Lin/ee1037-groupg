function showMachineDetails(button) {
    const card = button.closest('.product-card');
    const title = card.querySelector('h3').innerText;
    const shortDesc = card.querySelector('p').innerText;
    const longDesc = card.dataset.longDescription;
    const specs = card.dataset.specs?.split('\n') || [];
    const features = card.dataset.features?.split('\n') || [];
    const imageSrc = card.querySelector('img').src;
  
    // Set basic content
    document.getElementById('machineModalLabel').innerText = title;
    document.getElementById('machineModalImage').src = imageSrc;
    document.getElementById('machineModalDescription').innerHTML = `
      <strong>Overview:</strong> ${shortDesc}<br><br>
      ${longDesc}
    `;
  
    // Populate specifications
    const specsList = document.getElementById('machineModalSpecs');
    specsList.innerHTML = specs.map(spec => {
      const [label, value] = spec.split('|');
      return value ? `<li><strong>${label.trim()}:</strong> ${value.trim()}</li>` : '';
    }).join('');
  
    // Populate features
    const featuresList = document.getElementById('machineModalFeatures');
    featuresList.innerHTML = features.map(feature => 
      `<li>${feature.trim()}</li>`
    ).join('');
  
    new bootstrap.Modal(document.getElementById('machineModal')).show();
  }
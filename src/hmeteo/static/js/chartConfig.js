function getTemperatureAxisConfig(temp) {
    return {
        min: Math.round(temp.min),
        max: Math.ceil(temp.max),
        ticks: {
            color: 'red',
            font: {
                size: 14,
                weight: 'bold',
            },
        },
        title: {
            display: true,
            text: 'Temperature (°C)',
            color: 'red',
            font: {
                size: 16,
                weight: 'bold',
            },
        },

    };
}
function getXAxisConfig() {
    return {
    ticks: {
        color: 'white', // Tick color
        font: {
            size: 14, // Tick font size
            weight: 'bold', // Tick font weight
        },
    },
    title: {
        display: true,
        text: 'Dates', // Horizontal axis title
        color: 'white', // Title color
        font: {
            size: 16, // Title font size
            weight: 'bold', // Title font weight
        },
    },
}
}

function getRainfallAxisConfig() {
     return {
        position: 'right',
        ticks: {
          color: 'blue',
          font: {
              size: 14,
              weight: 'bold',
          },
      },
      title: {
          display: true,
          text: 'Rainfall (mm)',
          color: 'blue',
          font: {
              size: 16,
              weight: 'bold',
          },
      },
    }
}
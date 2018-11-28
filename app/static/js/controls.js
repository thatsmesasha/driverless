function drive(direction, foldername, label) {
  const url = '/control/drive'

  const data = { direction }
  if (foldername) {
    data.foldername = foldername
  }
  if (label) {
    data.label = label
  }

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    }
  }).then(res => res.json())
  .then(response => {
    if (response !== true && response.error) {
      addAlert(response.error)
    }
  })
  .catch(error => console.error('Error:', error))
  setTimeout(updateFolderStats, 1000)
}

document.onkeydown = (e) => {
  e = e || window.event

  const directions = {
    32: 'stop',
    37: 'left',
    38: 'forward',
    39: 'right',
    40: 'back',
  }

  const direction = directions[e.keyCode]
  if (direction) {
    let foldername = null
    let label = null

    if (document.getElementById('button-folder').getAttribute('aria-pressed') === 'true') {
      foldername = document.getElementById('foldername').value
    }
    if (document.getElementById('button-label').getAttribute('aria-pressed') === 'true') {
      label = document.getElementById('labelname').value
    }
    drive(direction, foldername, label)
  }
}

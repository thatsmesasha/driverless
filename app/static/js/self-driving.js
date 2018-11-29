function selfDrive(on) {
  const url = '/control/self-drive'

  const data = { on }

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
}

$("#button-self-driving").click(function () {
  const on = document.getElementById('button-self-driving').getAttribute('aria-pressed') !== 'true'
  selfDrive(on)
})

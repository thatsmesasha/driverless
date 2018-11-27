$('#update-settings').submit(function (evt) {
  evt.preventDefault(); //prevents the default action

  const url = '/control/update-settings'

  fetch(url, {
    method: 'POST',
    body: $('#update-settings').serialize(),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  }).then(res => res.json())
  .then(response => {
    if (response === true) {
      addAlert('Updated car settings', error=false)
    } else {
      addAlert(response.error)
    }
  })
  .catch(error => console.error('Error:', error))
})

function drive(direction) {
  var url = '/control/drive'
  var data = { direction }

  fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
  .then(response => {
    if (response !== true && response.error) {
      addAlert(response.error)
      console.error(response.detailed_error)
    }
  })
  .catch(error => console.error('Error:', error))
}

document.onkeydown = (e) => {

}

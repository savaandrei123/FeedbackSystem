var selected_faculty_id = 0

function getProgrammes(){
    const url = 'http://127.0.0.1:5000/facultyprogrammes?' + new URLSearchParams({
      id:selected_faculty_id
    }) 
    fetch(url)
    .then(function(response){
      return response.json()
  })
    .then(function(complete_response){
      data=``
      complete_response.response.forEach(programme => {
        data += `<a href="#">${programme.name}</a>`
        option = document.createElement('option');
        option.value = option.text = programme.name;
        select.add(option);
      }); 
      document.getElementById("programmes").innerHTML=data 
    })
  }
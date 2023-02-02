function getFaculties(){
  const url = 'http://127.0.0.1:5000/faculties' 
  fetch(url)
  .then(function(response){
    return response.json()
})
  .then(function(complete_response){
    console.log(complete_response.response)
    data=``
    complete_response.response.forEach(faculty => {
      data += `<button onclick='redirect(${faculty.id})' class="box">${faculty.name}</div>`
    }); 
    document.getElementById("faculties").innerHTML=data
  })
}


function redirect(id){
  selected_faculty_id = id
  window.location.href = "./courses.html";
}
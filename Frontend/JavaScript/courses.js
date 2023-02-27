courses_list=[]

function getProgrammes(){
    selectProgramme = document.getElementById('programmes');
    option = document.createElement('option');
    option.text = option.value = "Toate";
    selectProgramme.add(option);
    const url = 'http://127.0.0.1:5000/facultyprogrammes?' + new URLSearchParams({
      id:localStorage.getItem('selected_faculty_id')
    }) 
    fetch(url)
    .then(function(response){ 
      return response.json()
  })
    .then(function(complete_response){
      complete_response.forEach(programme => {
        option = document.createElement('option');
        option.text =  programme.name 
        option.value = programme.abbreviation
        selectProgramme.add(option);
      }); 

    })
  }


function getCourses(){
  const url = 'http://127.0.0.1:5000/facultycourses?' + new URLSearchParams({
    id:localStorage.getItem('selected_faculty_id')
  }) 
  fetch(url)
  .then(function(response){
    return response.json()
})
  .then(function(complete_response){
    data=``
    courses_list=[]
    complete_response.forEach(course => {
      courses_list.push(course)
      data += `<button onclick='redirect()' class="box">${course.name}</button>`
      })
      document.getElementById("courses").innerHTML=data
    })
  }


  function filterCourses(){
    data=``
    programme_name = document.getElementById("programmes").value
    selected_year = document.getElementById("years").value
    if(selected_year == 0 && programme_name == "Toate"){
      courses_list.forEach(course => {
        data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    if(selected_year == 0 && programme_name != "Toate"){
      courses_list.forEach(course => {
        course.programmes.forEach(programme => {
          if(programme.name==programme_name)
          data += `<button onclick='redirect()' class="box">${course.name}</button>`
        });
      });
    }
    if(selected_year != 0 && programme_name == "Toate"){
      courses_list.forEach(course => {
        if(course.year == selected_year)
        data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    if(selected_year != 0 && programme_name != "Toate"){
      courses_list.forEach(course => {
        course.programmes.forEach(programme => {
          if(programme.name === programme_name && course.year == selected_year)
          data += `<button onclick='redirect()' class="box">${course.name}</button>`
        });
      });
    }
    document.getElementById("courses").innerHTML=data
  }


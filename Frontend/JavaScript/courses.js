courses_list=[]

function getProgrammes(){
    selectProgramme = document.getElementById('programmes');
    option = document.createElement('option');
    option.value = 0
    option.text = "Toate";
    selectProgramme.add(option);
    const url = 'http://127.0.0.1:5000/facultyprogrammes?' + new URLSearchParams({
      id:localStorage.getItem('selected_faculty_id')
    }) 
    fetch(url)
    .then(function(response){
      return response.json()
  })
    .then(function(complete_response){
      complete_response.response.forEach(programme => {
        option = document.createElement('option');
        option.value = programme.id
        option.text = programme.name;
        selectProgramme.add(option);
      }); 

    })
  }
function getYear(){
    selectYear = document.getElementById('years');
    option = document.createElement('option');
    option.value = 0
    option.text = "Toti"
    selectYear.add(option);

    const url = 'http://127.0.0.1:5000/facultyyears?' + new URLSearchParams({
      id:localStorage.getItem('selected_faculty_id')
    }) 
    fetch(url)
    .then(function(response){
      return response.json()
  })
    .then(function(complete_response){
      for(i=1;i<=complete_response.response;i++){
      option = document.createElement('option');
      option.value = option.text = i
      selectYear.add(option);
      }
      }); 
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
    // console.log(complete_response.response)
    courses_list=[]
    complete_response.response.forEach(course => {
      courses_list.push(course)
      data += `<button onclick='redirect()' class="box">${course.name}</button>`
      })
      document.getElementById("courses").innerHTML=data
    })
  }

function getCourses2(id,year){
  const url = 'http://127.0.0.1:5000/programmecourses?' + new URLSearchParams({
    id:id,
    year:year
  }) 
  fetch(url)
  .then(function(response){
    return response.json()
})
  .then(function(complete_response){

    
    courses_list=[]
    complete_response.response.forEach(course => {
      courses_list.push(course)
    })
    console.log(courses_list)
    })

  }


  function filterCourses(){
    // console.log(courses_list)
    data=``
    programme_id = document.getElementById("programmes").value
    selected_year = document.getElementById("years").value
    if(selected_year == 0 && programme_id == 0){
      courses_list.forEach(course => {
        data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    if(selected_year == 0 && programme_id != 0){
      getCourses2(programme_id,selected_year)
      courses_list.forEach(course => {
      data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    if(selected_year != 0 && programme_id == 0){
      courses_list.forEach(course => {
        if(course.year == selected_year)
        data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    if(selected_year != 0 && programme_id != 0){
      getCourses2(programme_id,selected_year)
      courses_list.forEach(course => {
      data += `<button onclick='redirect()' class="box">${course.name}</button>`
      });
    }
    document.getElementById("courses").innerHTML=data
  }


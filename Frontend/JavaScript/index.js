
function redirect(id){
  localStorage.setItem('selected_faculty_id',id)
  window.location.href = "./courses.html";
}
document.addEventListener('DOMContentLoaded', function() {
  let buttonSend = document.querySelector('#sendInf')
  let new_type = document.querySelector('#new_type')
  let add_data = document.querySelector('#add_data')
  let collect_info = document.querySelector('#collect_info')
  let x_tbl = document.querySelector('#new_x')
  let y_tbl = document.querySelector('#new_y')
  let get_corr = document.querySelector('#get_corr')
  let get_corr_button = document.querySelector('#get_corr_button')
  buttonSend.addEventListener('click', function(e){ 
    fetchDataPost('calculate/', collect_data());
  })

  add_data.addEventListener('click', function(e){
    add_data_func(x_tbl, 'x')
    add_data_func(y_tbl, 'y')
  })

  get_corr_button.addEventListener('click', async function(e){
    try {

      let x_type = document.querySelector('#x_data_type').value;
      let y_type = document.querySelector('#y_data_type').value;
      let answ = document.querySelector('#answer_1');
      let user_id_get = document.querySelector('#user_id_get').value;
      const response = await fetch(`/correlation?x_data_type=${x_type}&y_data_type=${y_type}&user_id=${user_id_get}`);
      const json = await response.json();
      answ.innerHTML = JSON.stringify(json.answer);
      console.log(json, 'json')
    } catch (e) {
        console.error(e);
    }
  })

  collect_info.addEventListener('click', function(e){
    collect_data()
  })


})

function collect_arr(side){
  let arr = [];

  for(let elem of document.querySelectorAll(`.${side}_obj_class`)){
    console.log(elem, 'elem')
    let tempObj = {
      'date': elem.firstElementChild.value,
      'value': elem.lastElementChild.value
    }
    arr.push(tempObj)
  }
  return arr;
}

function collect_data(){
  let user_id = document.querySelector('#user_id').value;
  let x_str = document.querySelector('#x_str').value;
  let y_str = document.querySelector('#y_str').value;
  let result_show = document.querySelector('#result');
  let x_data_arr = collect_arr('x');
  let y_data_arr = collect_arr('y');
  let result = {
    'user_id': user_id,
    'data': {
      'x_data_type': x_str,
      'y_data_type': y_str,
      'x': x_data_arr,
      'y': y_data_arr
    },
  }

  result_show.innerHTML = JSON.stringify(result)
  return result;
}

function add_data_func(elem, side){
  elem.insertAdjacentHTML('beforeend', `
    <p class=${side}_obj_class>
      <input  class="date_class" placeholder='date'>
      <input  class="value_class" placeholder='value'>
    </p>

  `)
}


async function fetchDataGet() {
    try {
      const response = await fetch('/get_all_hours/');
      const json = await response.json();
      booking_info = json.bookings;
      my_bookings = json.filtered;
    } catch (e) {
        console.error(e);
    }
};

async function fetchDataPost(url, obj){
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  try{
    let response = await fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        "Content-type": "application/json"
      },
      body: JSON.stringify(obj)
    });
    console.log(url, 'answ')
  } catch(e){
    console.error(e);
  }
  window.location.reload(false);
}



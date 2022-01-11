document.addEventListener('DOMContentLoaded', function() {
  let buttonSend = document.querySelector('#sendInf')
  buttonSend.addEventListener('click', function(e){ 
    e.preventDefault()
    send_info()})

})

function send_info(e){
  let obj = {
    "user_id": 1,
    "data": {
        "x_data_type": "steps",
        "y_data_type": "pulse",
        "x":[
            {
                "date": "2022-01-01",
                "value": 0.5
            },
            {
                "date": "2022-01-01",
                "value": 1.5
            },
            {
                "date": "2022-01-01",
                "value": 2.5
            },
        ],
        "y":[
            {
                "date": "2022-01-01",
                "value": 3.5
            },
            {
                "date": "2022-01-01",
                "value": 4.5
            },
            {
                "date": "2022-01-01",
                "value": 5.5
            },
        ]
    }
}

  fetchDataPost('calculate/', obj);
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



const red = "hsl(0, 100%, 50%)";  //red
const green = "hsl(120, 100%, 45%)";  //green
const white = "hsl(0, 100%, 100%)";  //white
const grid_color = "hsl(0, 0%, 50%)";  //grey

const income_color_list = [
    'hsl(130, 80%, 50%)','hsl(90, 100%, 50%)', 
    'hsl(170, 70%, 40%)', 'hsl(210, 70%, 40%)',
    'hsl(240, 60%, 35%)','hsl(60, 100%, 50%)',
];

const expense_color_list = [
    'hsl(0, 100%, 50%)', 'hsl(330, 100%, 50%)',
    'hsl(40, 100%, 50%)', 'hsl(20, 100%, 50%)',
    'hsl(300, 100%, 50%)', 'hsl(280, 100%, 50%)',
    'hsl(260, 100%, 50%)', 'hsl(240, 100%, 50%)',
];

//Charts
function income_expense_chart(ctx1) {
    fetch(ctx1.dataset.url)
    .then((response) => response.json())
    .then((chart_data) => {
        new Chart(ctx1, {
            type: "line",
            data: {
                labels: chart_data.labels,
                datasets: [{
                    label: `Income (Average: $${chart_data.income_mean})`,
                    data: chart_data.income_data,
                    backgroundColor: green,
                    borderColor: white,
                },{
                    label: `Expense (Average: $${chart_data.expense_mean})`,
                    data: chart_data.expense_data,
                    backgroundColor: red,
                    borderColor: white,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  //displaying the graph dynamically among different devices.
                elements:{
                    point:{
                        radius:5
                    }
                },
                scales: {
                    y: {  
                        ticks: {
                            color: white, 
                            //beginAtZero: true
                        },
                        grid: {
                            color: grid_color
                        }
                    },
                    x: {  
                        ticks: {
                            color: white,
                            //beginAtZero: true
                        },
                        grid: {
                            color: grid_color
                        }
                    }
                },
                plugins:{
                    legend: {
                        labels: {
                            color: white,
                        }
                    },
                },
            },
            // increase spacing between legend and graph
            plugins: [{
                id: 'legendMargin',
                beforeInit(chart, legend, options) {
                    const fitValue = chart.legend.fit

                    chart.legend.fit = function fit(){
                        fitValue.bind(chart.legend)()
                        return this.height += 10  //
                    }
                }
            }]
        });
    })
};


function bank_account_chart(ctx2) {
    fetch(ctx2.dataset.url)
    .then((response) => response.json())
    .then((chart_data) => {
        const colours = chart_data.balance.map((value) => value < 0 ? red : green);
        new Chart(ctx2, {
            type: "bar",
            data: {
                labels: chart_data.label,
                datasets: [{
                    axis: 'y',
                    data: chart_data.balance,
                    borderColor: colours,
                    backgroundColor: colours,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  //displaying the graph dynamically among different devices.
                plugins: {
                    legend: {
                        display: false
                    }
                },
                indexAxis: 'y',
                scales: {
                    y: {
                        ticks: {
                            minRotation : 25,
                            color: white, 
                            font: {
                                size: 10
                            }
                        }
                    },
                    x: {
                        ticks: {
                            color: white, 
                        }
                    }
                }
            }
        });
    })
};


function category_chart(ctx3, ctx4) {
    fetch(ctx3.dataset.url)
    .then((response) => response.json())
    .then((chart_data) => {
        new Chart(ctx3, {
            type: "doughnut",
            data: {
                labels: chart_data.income_label,
                datasets: [{
                    label: 'Amount',
                    data: chart_data.income_amount,
                    backgroundColor: income_color_list,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  //displaying the graph dynamically among different devices.
                plugins:{
                    legend:{
                        position: 'right',
                        labels: {
                            color: white,
                        }
                    },
                },
            },
        });
        new Chart(ctx4, {
            type: "doughnut",
            data: {
                labels: chart_data.expense_label,
                datasets: [{
                    label: 'Amount',
                    data: chart_data.expense_amount,
                    backgroundColor: expense_color_list,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  //displaying the graph dynamically among different devices.
                plugins:{
                    legend:{
                        position: 'right',
                        labels: {
                            color: white,
                        }
                    },
                },
            },
        });
    })
};

const ctx1 = document.getElementById('income-expense');
if (ctx1) {
    income_expense_chart(ctx1);
}

const ctx2 = document.getElementById('bank-accounts');
if (ctx2) {
    bank_account_chart(ctx2);
}

const ctx3 = document.getElementById('income-category');
const ctx4 = document.getElementById('expense-category');
if (ctx3 && ctx4) {
    category_chart(ctx3, ctx4);
}

//sidebar
function set_sidebar_active_item(){
    let sidebar = document.getElementById('sidebar');
    let sidebar_items = sidebar.querySelectorAll('.nav-item');
    let path = window.location.pathname.replaceAll('/', '');

    sidebar_items.forEach(item => {
        if (item.id == path){
            item.className += ' active';
        } else {
            item.className = item.className.replace('active', '');
        }
    })
}
set_sidebar_active_item();

//hamburger sticker
function toggle_sidebar(){
    let sidebar = document.querySelector('.sidebar');
    let content = document.querySelector('.content');
    sidebar.classList.toggle('open');
    content.classList.toggle('open');
}
let hambergers = document.querySelectorAll('.sidebar-toggler');
hambergers.forEach(function(hamberger){
    hamberger.addEventListener("click", toggle_sidebar);
})

//modal
function pass_url_to_modal(remove_modal){
    remove_modal.addEventListener("show.bs.modal", function (event) {
        let button = event.relatedTarget; // Button that triggered the modal
        let remove_url = button.dataset.url; // Extract info from data-* attributes
        
        const confirm_remove = document.getElementById('confirm-remove');
        //console.log(confirm_remove)
        confirm_remove.action = remove_url;
    });
};

const remove_transaction_modal = document.getElementById('remove-transaction-Modal');
if (remove_transaction_modal) {
    pass_url_to_modal(remove_transaction_modal);
}

const remove_account_modal = document.getElementById('remove-account-Modal');
if (remove_account_modal) {
    pass_url_to_modal(remove_account_modal);
}

//confirmation before deleting records.
let delete_text =  document.getElementById('delete-text');
if (delete_text){
    delete_text.addEventListener('input', (event) => {
        let delete_button =  document.getElementById('delete-button');
        delete_button.disabled = (delete_text.value == 'DELETE')? false: true;
    });
}


//traffic tracking related
//get csrf token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//post request with csrf token
async function traffic_tracker(url = '', data = {}) {
    let csrftoken = getCookie('csrftoken');
    let response = await fetch(url, {
        method: 'POST', 
        mode: 'same-origin', 
        credentials: 'same-origin', 
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data) 
    });
}

//track the session
window.onload = (event) => {
    height = window.screen.height;
    width = window.screen.width;
    url = '/on_load'
    data = {
        height,
        width
    }
    traffic_tracker(url, data)
}

onbeforeunload = (event) => {
    url = '/on_close'
    traffic_tracker(url)
}

//track on click event for every buttons and a tag
button = document.querySelectorAll('button')
button.forEach(element => {
    element.addEventListener('click', (event) =>{
        detail = element.innerHTML
        url = '/on_click_button'
        data = { detail }
        traffic_tracker(url, data)
    })
});

a_tag = document.querySelectorAll('a')
a_tag.forEach(element => {
    element.addEventListener('click', (event) =>{
        detail = element.href  
        url = '/on_click_button'
        data = { detail }
        traffic_tracker(url, data)
    })
});

//used django user.is_authenticated template tag to handle this problem.
//remove summary statistics section in login and register pages
/* const summary_statistics = document.getElementById('Summary-Statistic');
const user_login = document.getElementById('user-login');
const user_register = document.getElementById('user-register');
if (user_login || user_register) {
    summary_statistics.style.display = 'none';
} */
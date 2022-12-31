const red = "hsl(0, 100%, 50%)"  //red
const green = "hsl(120, 100%, 25%)"  //green
const white = "hsl(0, 100%, 100%)"  //white
const grid_color = "hsl(0, 0%, 50%)"  //grey

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


function income_category_chart(ctx3, ctx4) {
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
                    //backgroundColor: green,
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
                    //backgroundColor: red,
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
    income_expense_chart(ctx1)
}

const ctx2 = document.getElementById('bank-accounts');
if (ctx2) {
    bank_account_chart(ctx2)
}

const ctx3 = document.getElementById('income-category');
const ctx4 = document.getElementById('expense-category');
if (ctx3 && ctx4) {
    income_category_chart(ctx3, ctx4)
}

//sidebar
function set_sidebar_active_item(){
    var sidebar = document.getElementById('sidebar')
    var sidebar_items = sidebar.getElementsByClassName('nav-item')
    var path = window.location.pathname.replaceAll('/', '')

    for (var i=0; i < sidebar_items.length; i++){
        if (sidebar_items[i].id == path){
            sidebar_items[i].className += ' active'
        } else {
            sidebar_items[i].className = sidebar_items[i].className.replace('active', '')
        }
    }
}
set_sidebar_active_item()

//hamberger sticker
let hamberger = document.getElementsByClassName('sidebar-toggler')[0];
hamberger.addEventListener("click", function(event){
    let sidebar = document.getElementsByClassName('sidebar')[0];
    let content = document.getElementsByClassName('content')[0];
    sidebar.classList.toggle('open');
    content.classList.toggle('open');
})

//modal
function pass_url_to_modal(remove_modal){
    remove_modal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var remove_url = button.dataset.url; // Extract info from data-* attributes
        
        const confirm_remove = document.getElementById('confirm-remove');
        //console.log(confirm_remove)
        confirm_remove.action = remove_url;
    });
};

const remove_transaction_modal = document.getElementById('remove-transaction-Modal')
if (remove_transaction_modal) {
    pass_url_to_modal(remove_transaction_modal)
}

const remove_account_modal = document.getElementById('remove-account-Modal')
if (remove_account_modal) {
    pass_url_to_modal(remove_account_modal)
}

//confirmation before deleting records.
delete_text =  document.getElementById('delete-text');
delete_text.addEventListener('input', (event) => {
    delete_button =  document.getElementById('delete-button');
    delete_button.disabled = (delete_text.value == 'DELETE')? false: true;
});


//used django user.is_authenticated template tag to handle this problem.
//remove summary statistics section in login and register pages
/* const summary_statistics = document.getElementById('Summary-Statistic');
const user_login = document.getElementById('user-login');
const user_register = document.getElementById('user-register');
if (user_login || user_register) {
    summary_statistics.style.display = 'none';
} */
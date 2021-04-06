
const reportBtn = document.getElementById('report-btn');
const reportImg = document.getElementById('report-img');
const modal = document.getElementById('modal-body');

const reportName = document.getElementById('id_name');
const reportRemark = document.getElementById('id_remark');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
// const modal = document.getElementById('report-img');
const reportForm = document.getElementById('report-form');

if(reportImg) {
    reportBtn.classList.remove('not-visible');
}

const alertBox = document.getElementById('alert-box');

handleAlert = (type, message) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${message}
        </div>
    `;
}

reportBtn.addEventListener('click', () => {
    reportImg.setAttribute('class', 'w-100');
    modal.prepend(reportImg);

    reportForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData();

        formData.append('csrfmiddlewaretoken', csrf);
        formData.append('name', reportName.value);
        formData.append('remark', reportRemark.value);
        formData.append('image', reportImg.src);

        // console.log('report in process');

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                // console.log(response);
                handleAlert('success', 'Report saved successfully!');
                reportForm.reset();
            },
            error: function(error){
                // console.log(error);
                handleAlert('danger', 'oops... Somthing went wrong!')
            },
            processData: false,
            contentType: false,
        })
        // console.log('report save');
    })
});

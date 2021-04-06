const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
const alertBox = document.getElementById('alert-box');

// console.log(csrf);

Dropzone.autoDiscover = false;

const myDropzone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init: function () {
        this.on('sending', (file, xhr, formData) => {
            console.log('Sending');
            formData.append('csrfmiddlewaretoken', csrf);
        })
        this.on('success', (file, res) => {
            const exist = res.exist;

            if (exist) {
                alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                        File already exist!
                                    </div>`;
            } else {
                alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                                        File has been uploaded successfully!
                                    </div>`;
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 5,
    acceptedFiles: '.csv',
    addRemoveLinks: true,
})
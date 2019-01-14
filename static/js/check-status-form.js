$(function() {
    var $form = $('#form-check');
    var $phone = $form.find('#phone');
    var $phone_raw = $form.find('[name=phone]');
    var phone_cleave;

    $form.find('.form-group').removeClass('is-filled');
    $phone.one('click', function() {
        phone_cleave = new Cleave(this, {
            prefix: '+7',
            delimiter: ' ',
            numericOnly: true,
            blocks: [2, 0, 3, 0, 3, 2, 2],
            delimiters: [" ", "(", ")", " ", "-", "-"]
        });
    });
    $phone.on('change', function() {
        $phone_raw.val(phone_cleave && phone_cleave.getRawValue());
    });
    $form.on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        var $form = $(this);
        $form.find('.has-error').removeClass('has-error').find('.bmd-help').remove();
        $.ajax({
            processData: false,
            enctype: 'multipart/form-data',
            contentType: false,
            data: formData,
            type: $form.attr('method'),
            url: $form.attr('action'),
            success: function(response) {
                if (response.status) {
                    var $modal = $('#check_modal').modal('show');
                    $modal.find('.modal-body').html('');
                    if (response.data.id) {
                        var statusBlock = $('<div>').text('Статус заявки: ').append($('<b>').text(response.data.status))
                        var dateBlock = $('<div>');
                        if (response.data.finish_date) dateBlock.text('Окончание работы: ').append($('<b>').text(response.data.finish_date));
                        $modal.find('.modal-body').append(statusBlock).append(dateBlock);
                    } else {
                        var emptyBlock = $('<div>').text('Данной заявки не существует/');
                        $modal.find('.modal-body').append(emptyBlock);
                    }
                } else {
                    Object.keys(response.data).forEach(function(key) {
                        var input = $form.find('[name='+key+']');
                        var group = input.parents('.form-group').addClass('has-error');
                        var errors = response.data[key];
                        errors.forEach(function(error){
                            var block = $('<span>').addClass('bmd-help').text(error);
                            group.append(block);
                        })
                    });
                }
            }
        })
    });

});
$(function() {
    var $form = $('#form-request');
    var $car_brand = $form.find('#car_brand');
    var $car_model = $form.find('#car_model');
    var $car_generation = $form.find('#car_generation');
    var $work_type = $form.find('#work_type');
    var $date = $form.find('#date');
    var $time = $form.find('#time');
    var $first_name = $form.find('#first_name');
    var $phone = $form.find('#phone');
    var $phone_raw = $form.find('[name=phone]');
    var phone_cleave;

    function loadOptions($select, url, data) {
        $select.find('option').remove();
        $.ajax({
            url: url,
            data: data,
            success: function(response) {
                if (response.status) {
                    setOptions($select, response.result);
                }
            }
        })
    }

    function setOptions($select, result) {
        $select.attr('disabled', false);
        result = result || [];
        $select[0].add(new Option(' ', ''))
        result.forEach(function (option) {
           $select[0].add(new Option(option.label, option.id))
        });
    }
    $form.find('.form-group').removeClass('is-filled');
    loadOptions($car_brand, 'ajax/search-car-brand');
    $car_brand.on('change', function(){
        loadOptions($car_model, 'ajax/search-car', {brand: $(this).val()});
    });
    $car_model.on('change', function(){
        loadOptions($work_type, 'ajax/search-work-type', {car: $(this).val()});
        loadOptions($car_generation, 'ajax/search-car-generation', {car: $(this).val()});
    });
    $work_type.on('change', function(){
        loadOptions($date, 'ajax/search-date', {work: $(this).val()});
        $form.find('.price_text')
            .show()
            .find('.price').text($(this).val());
    });
    $date.on('change', function(){
        loadOptions($time, 'ajax/search-time', {work: $work_type.val(), date: $(this).val()});
    });
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
                    var $modal = $('#success_modal').modal('show');
                    $modal.find('.request_number').text(response.data);
                    $modal.find('.request_name').text($first_name.val());
                    $modal.find('.request_date').text($date.val());
                    $modal.find('.request_time').text($time.val());
                    $modal.find('.request_car_brand').text($car_brand.val());
                    $modal.find('.request_car_brand').text($car_brand.val());
                    $modal.find('.request_car').text($car_model.val());
                } else {
                    Object.keys(response.data).forEach(function(key) {
                        var input = $form.find('[name='+key+']');
                        var group = input.parent('.form-group').addClass('has-error');
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

    // show work modal
    $('.show-works').on('click', function() {
        var title = $(this).data('title');
        var category = $(this).data('id');
        $.ajax({
            url: 'ajax/work-info',
            data: { category: category },
            success: function(response) {
                if (response.status) {
                    var $modal = $('#work_description_modal').modal('show');
                    $modal.find('.work_title').html(title);
                    $modal.find('.table').find('tbody').html('');
                    response.result.forEach(function(work_info){
                        var row = $('<tr>');
                        var label = $('<td>').html(work_info['label']);
                        var price = $('<td>').html((work_info['is_range'] ? 'от ' : '') + work_info['price'] + ' руб.');
                        row.append(label).append(price);
                        $modal.find('.table').find('tbody').append(row);
                    });
                }
            }
        });
    })
});
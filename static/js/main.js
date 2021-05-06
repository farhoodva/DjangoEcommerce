
//tooltips
 $('[data-toggle="tooltip"]').tooltip();
 $('.fa-heart').on('click', function () {
 $(this).tooltip('hide')
                         })

//end tooltips

// home page scripts
    $(document).on('click', '.wish', function (e) {
        e.preventDefault()
        const url = $(this).attr('href')
        const itemId = $(this).attr('id')
        $.ajax({
                url: url,
                success: function (data) {

                if (data.added_to_wishlist === true) {
                    $('#'+itemId).html(`<i data-toggle="tooltip" data-trigger="hover" data-placement="top" title="Remove from wishlist" class="fa fa-heart text-danger "></i>`)
                    $('[data-toggle="tooltip"]').tooltip();
                    $('.fa-heart').on('click', function () {
                        $(this).tooltip('hide')
                         })
                                }
                else if (data.added_to_wishlist === false){
                    $('#'+itemId).html(`<i data-toggle="tooltip" data-trigger="hover" data-placement="top" title="Add to wishlist" class="far fa-heart text-dark  "></i>`)
                 $('[data-toggle="tooltip"]').tooltip();
                 $('.fa-heart').on('click', function () {
                        $(this).tooltip('hide')
                        })
                }
                else {
                    $('#modalLogin').modal('show')

                }
            }

        }
    )
})

// // {#product laoder with back-end function#}
//         let display = 8 //initial loaded number of items
//     //  $.ajax({
//     //     type: 'GET',
//     //     url: `/ajax_load_products/${display}`,
//     //     // data:{
//     //     //     'display':display
//     //     // },
//     //     success: function(data) {
//     //         $('#productlist').html(data)
//     //     }
//     // })
//         const loadMoreButton = $('#pr-loadmore')
//         const item_count = '{{item_count}}'
//         loadMoreButton.on('click',()=>{
//         loadMoreButton.text("Loading...")
//
//         $.ajax({
//         type: 'GET',
//         url: `/ajax_load_products/${display}`,
//         // data:{
//         //     'display':display
//         // },
//             success: function(data) {
//             if(display < item_count){
//                 console.log(display,item_count)
//                 $('#productlist').append(data)
//                 loadMoreButton.text('Load More')
//                 display += 4
//                 }
//             else {
//                 console.log(item_count)
//                 loadMoreButton.text('End')
//             }
//             }
//     })
//
//     })

// home page scripts end


 // navbar modal scripts
    $('#login').on('click', (e) => {
        e.preventDefault()
        $('#modalLogin').modal('show')
    })

      $('#logOut').on('click', (e)=> {
        e.preventDefault()
        $('#modalLogout').modal('show')
    })


    //live search
    $('#search').on('keyup focus ', function () {
        const searchBtn =  $('#searchBtn')
        const searchResults =  $('#search-results')
        let searchTxt = $(this).val().trim()
        const url = $('#searchForm').attr('url')
        if (searchTxt !== '') {
        searchBtn.removeAttr('disabled')
        searchBtn.removeClass('alert-primary')
        searchBtn.addClass('btn-primary')
        searchResults.fadeIn()
        $('#search').css({"outline": "none", "border-color": "white", "box-shadow": "0 0 4px grey"})
            $.ajax({
                type: 'GET',
                url: url,
                data: {
                    searchTxt: searchTxt,
                },
                success: function (data) {
                    $('#spinner').hide()
                    searchResults.html(data)
                    searchResults.css({"outline": "none", "border-color": "white", "border-top-style": "none"})
                    searchTxt = ''
                }
            })
        } else {
            searchResults.fadeOut()
            searchBtn.attr('disabled',true)
            searchBtn.removeClass('btn-primary')
            searchBtn.addClass('alert-primary')
        }
    })

    $(document).click(function (e) {
        const container = $(".result");
// if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            $('#search-results').fadeOut();
            $('#search').css({"outline": "", "border-color": "", "box-shadow": ""})
        }
    })

// {#    $(document).click(function (e) {#}
// {#        const container1 = $(".modal")#}
// {#        const container2 = $('#login')#}
// {#// if the target of the click isn't the container nor a descendant of the container#}
// {#        if (!container1.is(e.target) && container1.has(e.target).length === 0 && container2.is(e.target)) {#}
// {#            $('.modal').fadeOut();#}
// {#        }#}
// {#    })#}

// navbar scripts end


// profile and checkout city loader ajax
    $('#id_state').change(function () {
        const url = $('#form').attr('cities-url')
        const state_id = $('#id_state').val()

        $.ajax({
                url: url,
                data:{
                    'state': state_id
                       },
                success: function (data) {
                    $('#id_city').html(data)


            }
        }
    )
})

// profile and checkout city loader ajax end



// detail page scripts

    //wishlist
    $('#wishlist').on('click', function (e) {
        e.preventDefault()
        const url = $(this).attr('href')
        $.ajax({

            url:url,
            success:function (data){
            if(data.added_to_wishlist===true){
            $('#wishlist').html(`<i class="fa fa-heart text-danger mr-2"></i> Remove from wishlist`)

            }
            else if(data.added_to_wishlist===false){
            $('#wishlist').html('<i class="far fa-heart  mr-2"></i> Add to wishlist')
            }
            else {
                $('#modalLogin').modal('show')
            }
              },


        })
    })
    const ReviewForm = $('#reviewForm')
    const Toggle = $('#reviewFormToggle')
    ReviewForm.hide()
    Toggle.on('click',(e)=>{
        e.preventDefault()
        ReviewForm.slideDown('slow')
        Toggle.hide()
    })


// detail page scripts end


// form style
        $('.form-control').on('focus',(e)=>{
            const fieldId = $(e.target).attr('id')
            // {#$('#label'+fieldId).removeClass('text-dark')#}
            $('#label'+fieldId).addClass('font-weight-bold')
            $('#'+fieldId).css({'outline' :'none', "box-shadow": "1px 1px 4px grey", 'border':0})
        })
        $('.form-control').on('blur',(e)=>{
            const fieldId = $(e.target).attr('id')
            $('#label'+fieldId).removeClass('font-weight-bold')
            $('#'+fieldId).css({'outline' :'', "box-shadow": "none", 'border':''})
        })
        $('.form-select').on('focus',(e)=>{
            const fieldId = $(e.target).attr('id')
            // {#$('#label'+fieldId).removeClass('text-dark')#}
            $('#label'+fieldId).addClass('font-weight-bold')
            $('#'+fieldId).css({'outline' :'none', "box-shadow": "1px 1px 4px grey", 'border':0})
        })
        $('.form-select').on('blur',(e)=>{
            const fieldId = $(e.target).attr('id')
            $('#label'+fieldId).removeClass('font-weight-bold')
            $('#'+fieldId).css({'outline' :'', "box-shadow": "none", 'border':''})
        })
        $('.no-border').on('focus',()=>{
        // {#$('.no-border').css({"box-shadow": "none"})#}
        $('.no-border').addClass("rounded")
            })
// form style end


//shop variants

    const changeDisplayLarger = $("#largeDisplay")
    const changeDisplaySmaller = $("#smallDisplay")
    const productDisplay = $(".prods")
    changeDisplayLarger.on('click',()=>{
        productDisplay.removeClass('col-lg-4 col-xl-4 col-sm-6')
        productDisplay.addClass('col-6')
    })
    changeDisplaySmaller.on('click',()=>{
        productDisplay.removeClass('col-6')
        productDisplay.addClass('col-lg-4 col-xl-4 col-sm-6')
    })


// home page scripts
    $(document).on('click', '.wish', function (e) {
        e.preventDefault()
        const url = $(this).attr('href')
        const item_id = $(this).attr('id')
        $.ajax({
                url: url,
                success: function (data) {

                if (data.added_to_wishlist === true) {
                    $('#'+item_id).html(`<i class="fa fa-heart text-danger "></i>`)

                }
                else if (data.added_to_wishlist === false){
                    $('#'+item_id).html(`<i class="far fa-heart text-dark  "></i>`)
                    }
                else {
                    $('#modal').fadeIn()
                    // {#const login =  window.confirm('YOU MUST BE LOGGED IN, LOGIN NOW?')#}
                    // {#if(login) {#}
                    // {#  window.location.href = 'accounts/login'#}
                    // {#    }#}

                }
            }

        }
    )
})


// {#product laoder with back-end function#}
        let display = 8 //initial loaded number of items
     $.ajax({
        type: 'GET',
        url: `/ajax_load_products/${display}`,
        data:{
            'display':display
        },
        success: function(data) {
            $('#productlist').html(data)
        }
    })


        $('#pr-loadmore').on('click',()=>{
        display += 4
        $.ajax({
        type: 'GET',
        url: `/ajax_load_products/${display}`,
        data:{
            'display':display
        },
            success: function(data) {
                $('#productlist').html(data)
            }
    })

    })
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
        $('#search-results').fadeIn()
        $('#search').css({"outline": "none", "border-color": "white", "box-shadow": "0 0 4px grey"})

        const url = $('#searchForm').attr('url')
        const searchTxt = $(this).val().trim()
        // {#console.log(searchTxt)#}
        if (searchTxt !== '') {
            $.ajax({
                url: url,
                data: {
                    searchTxt: searchTxt,
                },
                success: function (data) {
                    $('#search-results').html(data)
                    $('#search-results').css({"outline": "none", "border-color": "white", "border-top-style": "none"})
                }
            })
        } else {
            $('#search-results').fadeOut()
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
    $(document).ready(function (){

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

 })

// profile and checkout city loader ajax end


// detail page scripts
 $(document).ready(function (){

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
                $('#modal').fadeIn()
            }
              }
        })
    })

 })

// detail page scripts end

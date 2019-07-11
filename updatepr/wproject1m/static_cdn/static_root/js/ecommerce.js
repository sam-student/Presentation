$(document).ready(function () {

    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action") // /abc/


    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }

    }

    contactForm.submit(function (event) {
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset()
                $.alert({
                    title: "Success!",
                    content: data.message,
                    theme: "modern",
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function (error) {
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function (key, value) { // key, value  array index / object
                    msg += key + ": " + value[0].message + "<br/>"
                })
                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern",
                })
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            }
        })
    })


    //In Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='video']")
    var typingTimer;
    var typingInterval = 500
    var searchbtn = searchForm.find("[type=\"submit\"]")

    searchInput.keyup(function (event) {

        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function () {
        clearTimeout(typingTimer)
    })

    function displaySearching() {
        searchbtn.addClass("disabled")
        searchbtn.html("Searching <i class=\"fa fa-spinner fa-spin\"></i>")
    }

    function performSearch() {
        displaySearching()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = '/search/?q=' + query
        }, 1000)

    }


    // In cart
    var productForm = $(".form-product-ajax")

    productForm.submit(function (event) {
        event.preventDefault()
        var thisForm = $(this)
        var action = thisForm.attr("action")
        var method = thisForm.attr("method")
        var formData = thisForm.serialize()

        $.ajax({
            url: action,
            method: method,
            data: formData,
            success: function (data) {
                var submitSpan = thisForm.find(".submit-span")
                if (data.added) {
                    submitSpan.html("<button type='submit' class='btn btn-link'>Remove?</button>")
                }
                else {
                    submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
                }
                $(".navbar-cart-count").text(data.navbarCount)
                if (window.location.href.indexOf("cart") != -1) {
                    refreshCart()
                }

            },
            error: function (errorData) {
                $.alert({
                    title: 'Caution!',
                    content: 'An Error Accourd!',
                    theme: 'modern'
                });


                console.log("error")
                console.log(errorData)

            }

        })

    })

    function refreshCart() {
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        {
            cartBody.html("Refresh")

        }
        var cartProduct = cartBody.find(".cart-product")
        var total = cartTable.find(".total")
        var subTotal = $(".sub-total")
        var currentLocation = window.location.href
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

        var refreshCartURL = '/api/cart/'
        var method = 'GET'
        var data = {}

        $.ajax({
            url: refreshCartURL,
            method: method,
            data: data,

            success: function (data) {
                console.log("Success")
                console.log(data)
                var i = data.products.length
                console.log(window.location.href)
                if (data.products.length > 0) {
                    cartProduct.html(" ")

                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th>" + i + "</th><td><a href=\"" + value.url + "\">" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })
                    cartBody.find(".sub-total").text(data.subTotal)
                    cartBody.find(".total").text(data.total)
                } else {
                    window.location.href = currentLocation
                }


            },

            error: function (errorData) {
                console.log("errorData")
                console.log(errorData)
            }

        })
    }

})
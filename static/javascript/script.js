var payandreturn = document.getElementById('payandreturn');
var showModal = document.getElementById('showModal');

var borrowerName = document.getElementById('borrowerName');
var borrowedBooks = document.getElementById('borrowedBooks');
var totalAmount = document.getElementById('totalAmount');

var borrowerAvailable = document.getElementById('borrowerAvailable');
var borrowerNotAvailable = document.getElementById('borrowerNotAvailable');

async function borrow() {

    var borrower_name = document.getElementById('name').value;
    var borrower_email = document.getElementById('email').value;
    var book1 = document.getElementById('book_1');
    var book2 = document.getElementById('book_2');
    var book3 = document.getElementById('book_3');


    var books = [];
    var bookid1 = book1.name;
    bookid1 = bookid1.split('_')[1];

    var bookid2 = book2.name;
    bookid2 = bookid2.split('_')[1];

    var bookid3 = book3.name;
    bookid3 = bookid3.split('_')[1];

    if (book1.value != "" && book1.value >= 0) {
        temp = {
            book_id: bookid1,
            book_qty: book1.value
        }
        books.push(temp);
    }

    if (book2.value != "" && book2.value >= 0) {
        temp = {
            book_id: bookid2,
            book_qty: book2.value
        }
        books.push(temp);
    }

    if (book3.value != "" && book3.value >= 0) {
        temp = {
            book_id: bookid3,
            book_qty: book3.value
        }
        books.push(temp);
    }

    var borrowerDetails = {
        borrower_name: borrower_name,
        borrower_email: borrower_email,
        books: books
    }

    formData = new FormData();
    formData.append("borrowerDetails", JSON.stringify(borrowerDetails));

    $.ajax({
        url: '/borrowbooks',
        type: 'POST',
        data: formData,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            data = response;
            if (data.flag == 1) {
                location.reload();
            } else if (data.flag == 0) {
                //Handle data.Exception
            }
        },
        error: function() {

        }
    });
    // console.log(borrower_name, borrower_email, book1.value, bookid1, book2.value, bookid2, book3.value, bookid3);
}

var bookIds = [];
var bookQuantities = [];

async function returnUser() {
    var borrower_email = document.getElementById('email2').value;
    var borrowerDetails = {
        borrower_email: borrower_email
    }
    formData = new FormData();
    formData.append("borrowerDetails", JSON.stringify(borrowerDetails));

    $.ajax({
        url: '/returnbooks',
        type: 'POST',
        data: formData,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            data = response;

            if (data.no != undefined) {
                borrowerAvailable.style.display = "none";
                borrowerNotAvailable.style.display = "block";
                borrowerNotAvailable.innerHTML = data.no;
            } else {
                borrowerName.innerHTML = data.borrower_name;
                totalAmount.innerHTML = "$ " + data.total_price;
                var idx = 0;
                data.books.forEach(element => {
                    bookIds.push(data.book_ids[idx]);
                    bookQuantities.push(data.book_qty[idx]);
                    borrowedBooks.innerHTML += `<li>${element}  <span class="label label-success">${data.book_qty[idx]}</span></li>`;
                    idx = idx + 1;
                });
                borrowerNotAvailable.style.display = "none";
                borrowerAvailable.style.display = "block";
            }
        },
        error: function() {

        }
    });
}

async function returnBook() {
    var bookDetails = {
        book_id: bookIds,
        book_qty: bookQuantities
    };
    var borrower_email = document.getElementById('email2').value;

    var borrowerDetails = {
        borrower_email: borrower_email,
        books: bookDetails
    }

    formData = new FormData();
    formData.append("borrowerDetails", JSON.stringify(borrowerDetails));
    $.ajax({
        url: '/returnbookUser',
        type: 'POST',
        data: formData,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            data = response;
            if (data.flag == 1) {
                showModal.click();
            } else if (data.flag == 0) {
                //Handle data.Exception
            }
        },
        error: function() {

        }
    });
}

$(document).ready(function() {

    var start = document.getElementById("start");
    start.click();

});

$('li > a').click(function() {
    $('li').removeClass();
    $(this).parent().addClass('active');
});

var oldsec;

function myFunction(div) {

    if (oldsec == undefined) {} else {
        oldsec.style.display = "none";
    }

    var x = div.href.split('#')[1];
    console.log(x);

    var sec = document.getElementById(`${x}`);
    sec.style.display = "block";
    oldsec = sec;
}

// $('#borrow').on('click', function() {



// });
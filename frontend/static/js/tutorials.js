
/*
* 1)
*How to POST request in a Python Website using AJAX ? [Flask & Django]
*JimShapedCoding
*URL: https://www.youtube.com/watch?v=UmC26YXExJ4&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=12
Summary: Basic Flask + AJAX (jQuery)
*/

// function performPost() {
//     $.ajax ({
//         type: "POST",
//         url: "/create_file",
//         data: {"name":"Jim"},
//     })
// }

/*
* 2)
*Flask & the Fetch API (AJAX?) - Python on the web - Learning Flask Series Pt. 10
*Julian Nash
*URL: https://www.youtube.com/watch?v=QKcVjdLEX_s&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=14
Summary: Flask + Fetch
*/
// function submit_entry(){

//     var name = document.getElementById("name");
//     var message = document.getElementById("message");
    
//     var entry = {
//         name: name.value,
//         message: message.value,
//     }

//     console.log(entry)

//     //fetch(`${window.location}/guestbook/create-entry`, {
//     fetch(`${window.origin}/guestbook/create-entry`, {
//         method: "POST",
//         credentials: "include",
//         body: JSON.stringify(entry),
//         cache: "no-cache",
//         headers: new Headers({
//             'content-type':"application/JSON"
//         })
//     })
//     .then (function (response){
//         if (response.status !== 200){
//             console.log(`Reponse status was not 200: ${response.status}`);
//             return ;
//         }
//         response.json().then(function (data){
//             console.log(data)
//         })
//     })
// }


/*
* 3)
*GET Data from API & Display in HTML with JavaScript Fetch API
*ByteGrad Tips
*URL: https://www.youtube.com/watch?v=zUcc4vW-jsI&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=6
Summary: Useful Fetch trick
*/

// fetch('https://jsonplaceholder.typicode.com/users')
// .then(res => {
//     return res.json();
// })
// .then(data => {
//     console.log(data);
//     data.forEach(user => {
//         const markup = `<li>${user.name}</li>`;

//         document.querySelector('ul').insertAdjacentHTML('beforeend', markup);
//     })
// })
// .catch(error => console.log(error));



/*
* 4)
*How to use fetch in JavaScript: GET, POST, PUT and DELETE requests
*OpenJavaScript
*URL:https://www.youtube.com/watch?v=hOXWY9Ng_KU&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=7
Summary: Very basic Fetch for HTTP REQUEST & Error Handling
*/

var API = 'https://reqres.in/api/users';

// 1. GET
// console.log(fetch(API)); // return a Promise
// fetch(API)
//     .then(res => {
//         if (res.ok) {
//             console.log("GET request successful");
//         } else {
//             console.log("GET request unsuccessful");
//         }
//         return res;
//     })
//     .then(res => res.json())
//     //.then(data => console.log(data))
//     .then(data => handleData(data))
//     .catch(error => console.log(error))

// function handleData(data) {
//         console.log(data)
// }

// 2. POST
// fetch(API, {
//     method: 'POST',
//     headers: {
//         'content-type':'application/json' // tell the server its JSON data
//     }, 
//     body: JSON.stringify({
//         "name": "jimmy",
//         "job": "developer"
//     })
// })
//     //.then(res => console.log(res))
//     .then(res => {
//                 if (res.ok) {console.log("POST request successful");}
//                 else {console.log("POST request unsuccessful");}
//                 return res;
//             })
//     .then(res => res.json())
//     .then(data => console.log(data))
//     .catch(error => console.log(error))

// 3. PUT

// fetch(`${API}/2`, {
//     method: 'PUT',
//     headers: {
//         'content-type':'application/json' // tell the server its JSON data
//     }, 
//     body: JSON.stringify({
//         "name": "jimmy",
//         "job": "developer"
//     })
// })
//     //.then(res => console.log(res))
//     .then(res => {
//                 if (res.ok) {console.log("PUT request successful");}
//                 else {console.log("PUT request unsuccessful");}
//                 return res;
//             })
//     .then(res => res.json())
//     .then(data => console.log(data))
//     .catch(error => console.log(error))

// //4. DELETE

// fetch(`${API}/2`, {
//     method: 'DELETE',
//     headers: {
//         'content-type':'application/json'
//     }, 
// })
//     .then(res => {
//                 if (res.ok) {console.log("DELETE request successful");}
//                 else {console.log("DELETE request unsuccessful");}
//                 return res;
//             })
//     .then(res => res.json())
//     .then(data => console.log(data))
//     .catch(error => console.log(error))




/*
* 5)
*Sending POST requests using AJAX (via JavaScript)to a Python Backend (via Flask)
*ZeroLife
*URL:https://www.youtube.com/watch?v=-XchxUQTcfQ&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=5
Summary: POST Request using XMLHttpRequest()
*/

// function func(){
//     var xml = new XMLHttpRequest();
//     xml.open("POST", "{{ url_for(func.func) }}", true);
//     xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     xml.onload = function() {
//         var dataReply = JSON.parse(this.responseText);
//         alert(dataReply);
//     }; //endfunction

//     dataSend = {
//         "somedata": "data",
//         "moredata": "moredata"
// };
//     xml.send(JSON.stringify(dataSend))
// }




/*

Basic JavaScript Operations

*/



// ========= jQuery =========  //

/*
*jQuery Tutorial #2 - Event Binding - jQuery Tutorial for Beginners
*URL: https://www.youtube.com/watch?v=G-POtu9J-m4&t=0s
*/

// $(document).ready(function (){
//     $('.select-btn').hide(300).show(1000);
// })

// $('#panel1').html('my panel <strong></strong>');
// $('#btn1').on('click', function() {
//     //$('#panel1').toggle()
//     //$('#panel1').slideToggle(200);
//     //$('#panel1').fadeToggle(200);
// });
// $('#btn1').on('mouseover', function() {
//     //$('#panel1').fadeout(200);
// });

// $(function() {

//     var content  = "My new panel content";
//     $('.panel-button').on('click', function(){
//         var panelID = $(this).attr('data-pandelid');
//         $('#'+panelID).toggle();
//         $('#'+panelID+ '.panel-body').html(content);
//     })
// })



// ========= HTML DOM =========  //
/*
*JavaScript DOM Manipulation – Full Course for Beginners
*URL: https://www.youtube.com/watch?v=5fb2aPlgoys&list=PL8JJphmL_ggGf-9DfLhI9n6wbst8QlFKF&index=30&t=3117s
*/


// // Declare variable
// // let name='Mosh';
// // const interesRate=0.3;


// 1. Print
// console.log('Hello World');
// document.write('<h1>Hello World 1<h1>');


// 2. Select elements
// const li =document.getElementById('header')
// const li = document.querySelector('header')

// li.setAttribute('id', 'test');
// li.removeAttribute('id')
// li.classList().add('list-items');
// li.classList().remove('list-items');

// li.remove()


// 3. Modify the value of HTML elements
// document.getElementById('header').innerHTML
// document.getElementById('header').innerHTML = 'Header1';

// document.getElementById('header').TextContent = 'Header1';
// document.getElementById('header').innerText = 'Header1';
// document.getElementById('inp').value = 'Hello';

// document.getElementsByName('inp').value = 'Hello';


// // ========= if-else; swicth; =========  //
// function pressed1(){
//     var text = document.getElementById('inp').value;
//     switch (text) {
//         case "red":
//             document.getElementById('header').style.color = 'red';
//             break;
//         default:
//             document.getElementById('header').style.color = 'black';
//             break;
//     }
// }

// function pressed2(){
//     var text = parseInt(document.getElementById('inp').value);
//     var output = document.getElementById('output');

//     if (text > 18){
//         output.innerHTML = "You are an adult";
//     } else if (text == 18) {
//         output.innerHTML = "You are 18";
//     } else {
//         output.innerHTML = "You are an child";
//     }
// }
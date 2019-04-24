
// Responsible for fetching and populating the drop down for makes of cars!
function addMakesOfCars(){
    var makesUrl = '/makes';
    var makeData;
    // load makes dropdown from Flask Route - '/makes'
    // Ajax call through d3.
    Plotly.d3.json(makesUrl,function(error,makeData){
    if (error) {
        return console.warn(error);
    };

        makeData[0].Makes.forEach(function(make) {
        Plotly.d3
            .select("#mark")
            .append('option')
            .attr('value', make)
            .text(make)
        });
    });
}

// Responsible for fetching and populating the drop down for years of cars!
function addYears(){

    var yearsUrl = '/years';
    var yearData;

    // load year dropdown from Flask Route - '/years'
    Plotly.d3.json(yearsUrl,function(error,yearData){
    if (error) {
        return console.warn(error);
    };

        yearData[0].Years.forEach(function(year) {
        Plotly.d3
            .select("#year_model")
            .append('option')
            .attr('value', year)
            .text(year)
        });
    });
}

// Responsible for validating user inputs!
function validateForm() {
    var mileage = document.forms["form_pred"]["mileage"].value;

    if ( !isNaN(mileage) && mileage > 0 && mileage <400000)
    {
        return true;
    }
    else if (isNaN(mileage)) {
        
        // Display the sweet alert!
        swal({
            type: 'error',
            title: 'Please enter numeric data only in the mileage field.',
            text: 'Format error!' //,
            // footer: '<a href>Why do I have this issue?</a>'
          });
        return false;
    }
    else
    {
        // Display the sweet alert!
        swal({
            type: 'error',
            title: 'Please enter data in the range of 0 - 400,000 only',
            text: 'Incorrect range!' //,
            // footer: '<a href>Why do I have this issue?</a>'
          });

        
        return false;
    }
}


function makePrediction() {
    // get a button whose id is 'predict'
    $("button#predict").click(function(e){
        e.preventDefault();

        // Prevent errors in the inputs
        if (validateForm()) {
            // Ajax call through jQuery.
            $.ajax({
                method : "POST",
                url : window.location.href + 'api',
                data : $('form').serialize(),
                success : function(result){
                    var json_result = JSON.parse(result);
                    var price = json_result['Price'];
                
                    var text = "";
                    var message ="";
                    if (price !=-1)
                        {
                            message = 'Estimated price is: $'+price.toLocaleString();
                            // Display the sweet alert!
                            swal({
                                type: 'success',
                                title: message,
                            });
                        }
                    else
                        {
                            var message = 'We are currently not supporting the make that you have requested in our inventory.';
                            // Display the sweet alert!
                            swal({
                                type: 'error',
                                title: message,
                            });
                        }
                     // Notify voice message to the user!   
                     TextToSpeech(message);   
                },
                error : function(){
                    console.log("error")
                }
            })
        }
    })
}


function TextToSpeech(text) {
    speechSynthesis.speak(
        new SpeechSynthesisUtterance(text)
      );
}


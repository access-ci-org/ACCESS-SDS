/*/////////////////////////////////////////////////
    Display a Bootstrap Alert Message on webpage //
    Args:                                        //
        alertMsg: Message to be Displayed        //
        alertType: Type of Alert                 //
*//////////////////////////////////////////////////
export function showAlert(alertMsg, alertType)
{
    $("#alert-div").append(     // Appends new alert to html element with ID: alert-div
        `<div class="alert alert-${alertType} alert-dismissible fade show" id="alert" role="alert">
            ${alertMsg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
        // Dynamic Bootstrap Alert based on ${alertType}
        // alert-dismissible: allows alert to be closed
        // fade show: Fade-in effect on appearance
        // ${alertMsg}: Inserts message into the alert div
        // <button type>: Creates a button to manually close the alert
        // <span>: Creates the (x)
    )
    /* Previous functionality, no longer required, but kept here in case we want this again later

    $("#alert").fadeTo(10000, 500).slideUp(1000, function()
        // fadeTo(10000, 500): After 10 seconds, fade to 50% opacity
        // slideUp(1000, function(){...}):
        {
            $("#alert").slideUp(1000);  // Alert Div shrinks upward in 1 second
            $("#alert").alert('close')  // Closes the Alert
        });
    */
    $('html,body').animate({scrollTop:0},'slow')    // Snaps the Page to the Top (Presumably to see the alert)
}

/*/////////////////////////////////////
    Hide Alert when no longer needed //
*//////////////////////////////////////
export function hideAlert()
{
    $("#alert").alert('close')
}
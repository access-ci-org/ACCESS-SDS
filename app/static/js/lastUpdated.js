/*//////////////////////////////////////////////////////////////////////////////
    This is a small script to display on the website when it was last updated //
*///////////////////////////////////////////////////////////////////////////////

$(document).ready(function()
{
    // Fetch the last modified date of the website
    var lastModified = document.lastModified;

    // Format the date
    var options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit'};
    var formattedDate = new Date(lastModified).toLocaleDateString(undefined, options);

    // Display the formatted date on the website
    document.getElementById("lastUpdated").innerHTML = formattedDate;
});
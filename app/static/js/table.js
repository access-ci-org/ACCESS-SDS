var issueReport = {}
$(document).ready(function(){
    $("#app_content").removeClass()
    $("#app_content").addClass('col')

    // Function to make URLs clickable
    function makeLinkClickable(data) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return data.replace(urlRegex, function(url) {
            // Insert zero-width space after slashes or dots, as an example
            var spacedUrl = url.replace(/(\/|\.)+/g, '$&\u200B');
            return '<a href="' + url + '" target="_blank">' + spacedUrl + '</a>';
        });
    }

    var staticTable = $('#softwareTable').DataTable({
        "sScrollX": "100%",
        "autoWidth": true,
        searchBuilder: {
            conditions: {
                string: {
                    '=': null,
                    'null':null,
                    '!null':null,
                    '!=':null,
                    'starts':null,
                    '!starts':null,
                    'ends':null,
                    '!ends':null,
                    '!contains':null,
                },
            }
        },
        dom:'Qlfrtip',
        columnDefs: 
            [
                {
                    searchBuilder: {
                        defaultCondition: 'contains'
                    },
                    targets:[0,1,2,3,4,5,6,7,8,9],
                },
                {   // Direct URL columns
                    targets: [6,7,8,9], 
                    render: function(data, type, row) {
                        if (type === 'display' && data) {
                            return makeLinkClickable(data);
                        }
                        return data;
                    },
                    createdCell:function(td){
                        $(td).css('word-wrap', 'break-all'); // Enable word-wrap
                        $(td).css('max-width', '300px'); // Ensure max-width is applied
                    }
                },
                {
                    targets: 6,
                    width:"700px"
                },
                {
                    targets:5,
                    width:"50px"
                }
            ],
        layout:{
            top1:"searchBuilder"
        }
    });

    var dynamicTable = $('#softwareTableDynamic').DataTable({
        "sScrollX": "100%",
        "autoWidth": true,
        searchBuilder: {
            conditions: {
                string: {
                    '=': null,
                    'null':null,
                    '!null':null,
                    '!=':null,
                    'starts':null,
                    '!starts':null,
                    'ends':null,
                    '!ends':null,
                    '!contains':null,
                },
            },
            
        },
        dom:'Qlfrtip',
        columnDefs:[
            {
                searchBuilder:{
                    defaultCondition:'contains'
                },
                targets:[0,1,2,3,4,5,6,7,8,9,10,11,12]
            },
            {   // show use case
                targets:10,
                render: function(data, type, row){
                    return '<button class="btn btn-info example-use-btn" type="button">Use Example</button>';
                }
            },
            {   // columns with links
                targets: [10,11,12,13],
                render: function(data, type, row){
                    if (type=='display' && data){
                        return makeLinkClickable(data);
                    }
                    return data;
                },
                createdCell:function(td){
                    $(td).css('word-wrap', 'break-all'); // Enable word-wrap
                    $(td).css('max-width', '400px'); // Ensure max-width is applied
                }
            },
            {   // description column
                targets:2,
                width:"700px",
            },
            {
                targets:3,
                width:"300px"
            }
        ],
        layout:{
            top1:"searchBuilder"
        }
    });

    // Initialize a Showdown converter with the Highlight.js extension
    var converter = new showdown.Converter({
        extensions: [highlightExtension]
    });


    dynamicTable.on('click','.example-use-btn', function(e){
        let rowData = dynamicTable.row(e.target.closest('tr')).data();
        var softwareName = rowData[0];
        var encodedSoftwareName = encodeURIComponent(softwareName);
        $.ajax({
            url: "/example_use/"+encodedSoftwareName,
            type:"GET",
            success: function(response){

                var useHtml = converter.makeHtml(response.use)
                $("#modal-title").text('Use Case for '+softwareName)
                $('#useCaseBody').html(useHtml);

                document.querySelectorAll('#useCaseBody pre Code').forEach((block)=>{
                    hljs.highlightElement(block)
                })

                $('#useCase-modal').modal('show');
            },
            error: function(xhr, status, error){
                console.error("Error fetching example use: ", error);
            }
        })
    })

    var $scrollBody = $('.dataTables_scrollBody');
    var scrollSensitivity = 100; // Distance from edge in pixels.
    var scrollSpeed = 7; // Speed of the scroll step in pixels.
    var scrollInterval;
    var scrollDirection;
  
    function startScrolling(direction) {
      if (scrollInterval) {
        clearInterval(scrollInterval);
      }
      scrollDirection = direction;
      scrollInterval = setInterval(function() {
        var currentScroll = $scrollBody.scrollLeft();
        $scrollBody.scrollLeft(currentScroll + scrollSpeed * scrollDirection);
      }, 10); // Interval in milliseconds
    }
  
    function stopScrolling() {
      clearInterval(scrollInterval);
    }
  
    // Event listener for mouse movement in the scroll body.
    $scrollBody.mousemove(function(e) {
      var $this = $(this);
      var offset = $this.offset();
      var scrollWidth = $this.get(0).scrollWidth;
      var outerWidth = $this.outerWidth();
      var x = e.pageX - offset.left;
  
      // Right edge of the table.
      if (scrollWidth > outerWidth && x > outerWidth - scrollSensitivity) {
        startScrolling(1); // Scroll right
      }
      // Left edge of the table.
      else if (x < scrollSensitivity) {
        startScrolling(-1); // Scroll left
      } else {
        stopScrolling();
      }
    });
  
    $scrollBody.mouseleave(stopScrolling);

    function checkScrollEdges(){
        let scrollLeft = $scrollBody.scrollLeft();
        var scrollWidth = $scrollBody.get(0).scrollWidth;
        var outerWidth = $scrollBody.outerWidth();

        if (scrollLeft+outerWidth >= (scrollWidth-1)){
            $scrollBody.parent().addClass('no-right-shadow');
        }else{
            $scrollBody.parent().removeClass('no-right-shadow');
        }

        if (scrollLeft===0){
            $scrollBody.parent().addClass('no-left-shadow');
        }else{
            $scrollBody.parent().removeClass('no-left-shadow');
        }
    }
    checkScrollEdges();
    $scrollBody.on('scroll',checkScrollEdges);


    // report issue

    var reportingIssue = false;
    var selectedElement = null;

    $("#reportIssueBtn").on('click',function(){
        event.stopPropagation();
        reportingIssue = !reportingIssue;
        
        if (reportingIssue){
            var alertDivMessage = "Click on where you see the issue"
            var alertType = 'info'
            showAlert(alertDivMessage,alertType);
        }

        if (reportingIssue) {
            $(this).text('Cancel');
            $('body').css('cursor', 'crosshair');
            $('body').on('click', handleIssueReportClick);
            $('body').on('mousemove',handleMouseMove);

        } else {
            $(this).text('Report Issue');
            $('body').css('cursor', 'default');
            $('body').off('click', handleIssueReportClick);
            $('body').off('mousemove',handleMouseMove);
            

            if (selectedElement){
                selectedElement.classList.remove('hovered');
                selectedElement = null;
            }
        }
    });

    function handleMouseMove(event){
        var target = event.target;

        if (selectedElement && selectedElement !== target){
            selectedElement.classList.remove('hovered');
        }

        // Add a red outline to the currently hovered element
        target.classList.add('hovered');
        selectedElement = target;
    }

    function handleIssueReportClick(event){
        if (reportingIssue && event.target !== $("#reportIssueBtn")[0]){
            var target = event.target;

            // Remove the event listener for mouse move
            $('body').off('mousemove', handleMouseMove);

            var pageUrl = window.location.href;
            var elementType = target.tagName.toLowerCase();
            var elementId = target.id;
            var elementClass = target.className;
            var elementText = $(target).text().trim();

            // Check if the clicked element is a table cell
            var tableCellInfo = {};
            if (elementType == 'td'){
                var $cell = $(target);
                var $row = $cell.closest('tr');
                var $table = $row.closest('table');
                var rowIndex = $row.index();
                var columnIndex = $cell.index();
                var tableId = $table.attr('id');

                tableCellInfo = {
                    tableId: tableId,
                    rowIndex: rowIndex,
                    columnIndex: columnIndex

                };
            }

            // Capture a screenshot of the website
            html2canvas(document.body).then(function(canvas){
                var captureDataUrl = canvas.toDataURL('image/png');
                
                // Create an object with the issue reporting data
            issueReport = {
                pageUrl: pageUrl,
                elementType: elementType,
                elementId: elementId,
                elementClass: elementClass,
                elementText: elementText,
                tableCellInfo: tableCellInfo,
                captureDataUrl: captureDataUrl
            };

            // Create a formatted string for the report details
            var reportDetails = "Page URL: " + issueReport.pageUrl + "\n" +
                                "Element Type: " + issueReport.elementType + "\n" +
                                "Element ID: " + issueReport.elementId + "\n" +
                                "Element Class: " + issueReport.elementClass + "\n" +
                                "Element Text: " + issueReport.elementText + "\n" +
                                "Table Cell Info: " + JSON.stringify(issueReport.tableCellInfo, null, 2);

                $("#reportDetails").text(reportDetails);

                // Show the modal
                $("#report-modal").modal('show');
                
                // Reset the report state
                reportingIssue = false;
                $('#reportIssueBtn').text('Report Issue');
                $('body').css('cursor','default');
                $('body').off('click',handleIssueReportClick);
                $('body').off('mousemove',handleMouseMove);
                
                if (selectedElement){
                    selectedElement.classList.remove('hovered');
                    selectedElement = null;
                }
            });
        }
    }

    $("#sendReportBtn").on('click', function() {
        var feedback = $('#reportFeedback').val();
    
        $.ajax({
            url: '/report-issue',
            type: 'POST',
            data: JSON.stringify({ feedback: feedback, reportDetails: issueReport }),
            contentType: 'application/json',
            success: function(response) {
                $('#report-modal').modal('hide');
                let message = 'Issue reported successfully!';
                showAlert(message,'success')
            },
            error: function(xhr, status, error) {
                console.error('Error reporting issue:', error);
                alert('Failed to report issue. Please try again.');
            }
    });

    $('#report-modal').on('hidden.bs.modal', function (e) {
        issueReport = {}
    });

        
    })
});

// Define the Highlight.js extension for Showdown
function highlightExtension() {
    return [{
        type: 'output',
        filter: function (text, converter, options) {
            var left = '<pre><code\\b[^>]*>',
                right = '</code></pre>',
                flags = 'g',
                replacement = function (wholeMatch, match, left, right) {
                    match = match.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
                    return left + hljs.highlightAuto(match).value + right;
                };
            return showdown.helper.replaceRecursiveRegExp(text, replacement, left, right, flags);
        }
    }];
}

function showAlert(alertMsg, alertType){
    $("#alert-div").append(
        `<div class="alert alert-${alertType} alert-dismissible fade show" id="alert" role="alert">
            ${alertMsg}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
    )
    $("#alert").fadeTo(2000, 500).slideUp(1000, function(){
        $("#alert").slideUp(1000);
        $("#alert").alert('close')
    });
    $('html,body').animate({scrollTop:0},'fast')
}
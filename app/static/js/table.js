import {header, siteMenus, footer, footerMenus, universalMenus} from "https://esm.sh/@access-ci/ui@0.2.0"

const siteItems =[
    {
        name: "ACCESS Resource Advisor",
        href: "https://access-ara.ccs.uky.edu:8080/"
    }
]

$(document).ready(function(){

    universalMenus({
        loginUrl: "/login",
        logoutUrl: "/logout",
        siteName: "Allocations",
        target: document.getElementById("universal-menus"),
    });
    header({
        siteName: "Support",
        target: document.getElementById("header")
    });
    siteMenus({
        items: siteItems,
        siteName: "Allocations",
        target: document.getElementById("site-menus"),
      });

    footerMenus({
        items: siteItems,
        target: document.getElementById("footer-menus"),
    });
    footer({ target: document.getElementById("footer") });

    const NavShadowHost = document.getElementById('universal-menus');
    const shadowRoot = NavShadowHost.shadowRoot;
    const loginButton = shadowRoot.querySelector('li:last-child button');
    loginButton.remove();

    $("#app_content").removeClass()
    $("#app_content").addClass('col')

    var currentUrl = window.location.href

    if (currentUrl.includes("ai-generated")){
        $("#ai-generated-link").addClass("active")
        $("#curated-link").removeClass("active")
    } else{
        $("#ai-generated-link").removeClass("active")
        $("#curated-link").addClass("active")
    }

    // Function to make URLs clickable
    function makeLinkClickable(data) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return data.replace(urlRegex, function(url) {
            // Insert zero-width space after slashes or dots, as an example
            var spacedUrl = url.replace(/(\/|\.)+/g, '$&\u200B');
            return '<a href="' + url + '" target="_blank">' + spacedUrl + '</a>';
        });
    }

    //Custom Search Logic
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            var api = new $.fn.dataTable.Api(settings);
            var visibleColumns = api.columns(':visible').indexes().toArray();
            var searchTerm = api.search();
    
            // Check if any visible column contains the search term
            for (var i = 0; i < visibleColumns.length; i++) {
                var columnIndex = visibleColumns[i];
                if (data[columnIndex].toLowerCase().includes(searchTerm.toLowerCase())) {
                    return true; // Match found in visible column
                }
            }
            return false; // No match found
        }
    );
    

    var staticTable = $('#softwareTable').DataTable({
        "sScrollX": "100%",
        "autoWidth": true,
        pageLength: 50,
        pagingType: 'full_numbers',     // 'First', 'Previous', 'Next', 'Last', with page numbers.
        lengthMenu: [
            [50, 250, 500, -1],
            [50, 250, 500, 'All']
        ],
        dom: 'Q<"d-flex flex-column flex-md-row justify-content-between"<"d-flex flex-column flex-md-row"<"d-flex mb-3 mb-md-0"l><"d-flex px-3"B>>f>rt<"d-flex justify-content-between"ip>', 
        language:
        {
            paginate:
            {
                // Change Arrows (< and >) into Word Equivalents
                previous: "Prev",
                next: "Next",
                first: "First",
                last: "Last"
            },

        },
        buttons: [
            'colvis',
        ],
        stateSave: true,
        stateDuration:-1,
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
    });

    var dynamicTable = $('#softwareTableDynamic').DataTable({
        "sScrollX": "100%",
        "autoWidth": true,
        "pageLength": 50,
        pagingType: 'full_numbers',     // 'First', 'Previous', 'Next', 'Last', with page numbers.
        lengthMenu: [
            [50, 250, 500, -1],
            [50, 250, 500, 'All']
        ],
        dom: 'Q<"d-flex flex-column flex-md-row justify-content-between"<"d-flex flex-column flex-md-row"<"d-flex mb-3 mb-md-0"l><"d-flex px-3"B>>f>rt<"d-flex justify-content-between"ip>',
        language:
        {
            paginate:
            {
                // Change Arrows (< and >) into Word Equivalents
                previous: "Prev",
                next: "Next",
                first: "First",
                last: "Last"
            },

        },
        buttons: [
            'colvis',
        ],
        stateSave: true,
        stateDuration:-1,
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
    });

    //Event Listener for Column Visibility
    staticTable.on('column-visibility.dt', function(e, settings, column, state) {
        staticTable.draw(); // Redraw the table
    });
    
    dynamicTable.on('column-visibility.dt', function(e, settings, column, state) {
        dynamicTable.draw(); // Redraw the table
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

    var $scrollBody = $('.dt-scroll-body');
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
    $('.dt-scroll-body').mousemove(function(e) {
      var $this = $(this);
    //   console.log($this);
    //   console.log($this[0].scrollWidth)
      var offset = $this.offset();
      var scrollWidth = $this[0].scrollWidth;
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
        var scrollWidth = $scrollBody[0].scrollWidth;
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
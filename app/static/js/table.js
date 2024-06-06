import {header, siteMenus, footer, footerMenus, universalMenus} from "https://esm.sh/@access-ci/ui@0.2.0"

const siteItems =[
    {
        name: "ACCESS Resource Advisor",
        href: "https://access-ara.ccs.uky.edu:8080/"
    }
]


$(document).ready(function()
{

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
        select: true,
        fixedHeader: true,  // Makes column headers 'fixed' to the top of the table when scrolling
        "sScrollX": "100%",
        autoWidth: true,
        pageLength: 25,
        pagingType: 'full_numbers',     // 'First', 'Previous', 'Next', 'Last', with page numbers
        lengthMenu: [
            [25, 50, 250, 500, -1],
            [25, 50, 250, 500, 'All']
        ],
        dom: 'PQ<"d-flex flex-column flex-md-row justify-content-between"<"d-flex flex-column flex-md-row"<"d-flex mb-3 mb-md-0"l><"d-flex px-3"B>>f>rt<"d-flex justify-content-between"ip>', 
        searchPanes: {
            cascadePanes: false,    // Can't use this until we optimize the table's performance
            dtOpts: {
                select: {
                    style: 'multi'
                }, 
            },
            combiner: 'or'
        },
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
        stateSave: false,
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
        columnDefs: [
            {
                searchPanes: {
                    show: true,
                    options: [                   
                        {
                            label: 'Aces',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('aces');
                            }
                        },
                        {
                            label: 'Anvil',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('anvil');
                            }
                        },
                        {
                            label: 'Bridges-2',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('bridges-2');
                            }
                        },
                        {
                            label: 'DARWIN',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('darwin');
                            }
                        },
                        {
                            label: 'Delta',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('delta');
                            }
                        },
                        {
                            label: 'Expanse',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('expanse');
                            }
                        },
                        {
                            label: 'Faster',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('faster');
                            }
                        },
                        {
                            label: 'Jetstream',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('jetstream');
                            }
                        },
                        {
                            label: 'Kyric',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('kyric');
                            }
                        },
                        {
                            label: 'Ookami',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('ookami');
                            }
                        },
                        {
                            label: 'Stampede-3',
                            value: function(rowData, rowIdx) {
                                return rowData[1].toLowerCase().includes('stampede3');
                            }
                        }
                    ]
                },
                targets: [1]
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'API',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('api');
                            }
                        },
                        {
                            label: 'Application',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('application');
                            }
                        },
                        {
                            label: 'Language',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('language');
                            }
                        },
                        {
                            label: 'Library',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('library');
                            }
                        },
                        {
                            label: 'Package',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('package');
                            }
                        },
                        {
                            label: 'Service',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('service');
                            }
                        },
                        {
                            label: 'Toolkit',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('toolkit');
                            }
                        },
                        {
                            label: 'Utility',
                            value: function(rowData, rowIdx) {
                                return rowData[2].toLowerCase().includes('utility');
                            }
                        },
                    ]
                },
                targets: [2]
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Climate/Weather',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('climate');
                            }
                        },
                        {
                            label: 'Computer Science',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('computer science');
                            }
                        },
                        {
                            label: 'Data Management',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('data management');
                            }
                        },
                        {
                            label: 'Engineering',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('engineering');
                            }
                        },
                        {
                            label: 'General Use',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('general');
                            }
                        },
                        {
                            label: 'Sciences',
                            value: function(rowData, rowIdx) {
                                return rowData[4].toLowerCase().includes('sciences');
                            }
                        },
                    ]
                },
                targets: [4]

            },
            {
                searchPanes: {
                    show: false
                },
                targets: '_all'

            },

            {
                // Enable Search Function On All Columns   
                targets:[0,1,2,3,4,5,6,7,8,9,10,11],
                searchBuilder: 
                    { 
                        defaultCondition: 'contains'
                    },    
            },

            {
                // Columns with clickable URLs
                targets: [6,7,8,9,10], 
                render: function(data, type, row) 
                {
                    if (type === 'display' && data) 
                    {
                        return makeLinkClickable(data);
                    }
                    return data;
                },
                
                createdCell:function(td)
                {
                    $(td).css('word-wrap', 'break-all'); // Enable word-wrap
                    $(td).css('max-width', '300px'); // Ensure max-width is applied
                }
                
            },
            { width: '500px', targets: 6 },     // Software Description
            { width: '400px', targets: [8, 9, 10] },     // Links
            { width: '100px', targets: 11 },     // Version Info
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

    var $scrollBody = $('div.dt-scroll-body').eq(3)
    var scrollSensitivity = 100; // Distance from edge in pixels.
    var scrollSpeed = 7; // Speed of the scroll step in pixels.
    var scrollInterval;
    var scrollDirection;

    // Event listener for mouse movement in the scroll body.
    $scrollBody.mousemove(function(e) 
    {
        var $this = $(this);
        var offset = $this.offset();
        var scrollWidth = $this[0].scrollWidth;
        var outerWidth = $this.outerWidth();
        var x = e.pageX - offset.left;
  
        // Right edge of the table.
        if (scrollWidth > outerWidth && x > outerWidth - scrollSensitivity) 
        {
            startScrolling(1); // Scroll right
        }
        // Left edge of the table.
        else if (x < scrollSensitivity) 
        {
            startScrolling(-1); // Scroll left
        } 
        else 
        {
            stopScrolling();
        }
    });
  
    $scrollBody.mouseleave(stopScrolling);

    checkScrollEdges();
    $scrollBody.on('scroll',checkScrollEdges);

    // Scrolling Behaviors
    function startScrolling(direction) 
    {
        if (scrollInterval) 
        {
            clearInterval(scrollInterval);
        }
        scrollDirection = direction;
        scrollInterval = setInterval(function() 
        {
        var currentScroll = $scrollBody.scrollLeft();
        $scrollBody.scrollLeft(currentScroll + scrollSpeed * scrollDirection);
        }, 10); // Interval in milliseconds
    }


    function checkScrollEdges()
    {
        let scrollLeft = $scrollBody.scrollLeft();
        var scrollWidth = $scrollBody[0].scrollWidth;
        var outerWidth = $scrollBody.outerWidth();

        if (scrollLeft+outerWidth >= (scrollWidth - 1))
        {
            $scrollBody.parent().addClass('no-right-shadow');
        }
        else
        {
            $scrollBody.parent().removeClass('no-right-shadow');
        }

        if (scrollLeft == 0)
        {
            $scrollBody.parent().addClass('no-left-shadow');
        }else
        {
            $scrollBody.parent().removeClass('no-left-shadow');
        }
    }

    function stopScrolling() 
    {
        clearInterval(scrollInterval);
    }
    
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
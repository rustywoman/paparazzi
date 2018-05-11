$(function(){
  var reportLinkRoot = $('#l_content__report_table');
  var loadingHandlerIns = new LoadingHandler($('#loading__bg'), $('#loading__status'));
  var reportResultEmptyDOM = document.createDocumentFragment();
  var markerHandlerIns = new MarkerHandler();
  // Init
  $.ajax(
    {
      url      : '/index.json',
      type     : 'GET',
      dataType : 'json',
    }
  ).then(
    function(result){
      loadingHandlerIns
        .init(60)
        .then(
          function(){
            var tmpResultInfo = null;
            for(var i = 0, il = result.length; i < il; i++){
              tmpResultInfo = result[i];
              reportResultEmptyDOM.appendChild(
                $(
                  [
                    '<div class="m_content__report_table__row">',
                      '<div class="m_content__report_table__cell">',
                        '<a class="marker" href="' + tmpResultInfo['path'] +  '" target="_blank">',
                          '<span>' + tmpResultInfo['name'] + '</span>',
                        '</a>',
                      '</div>',
                      '<div class="m_content__report_table__cell">' + tmpResultInfo['date'] + '</div>',
                    '</div>'
                  ].join('')
                ).get(0)
              );
            }
            reportLinkRoot.get(0).appendChild(reportResultEmptyDOM);
            loadingHandlerIns
              .init(80)
              .then(
                function(){
                  markerHandlerIns.reset();
                  loadingHandlerIns
                    .init(100)
                    .then(
                      function(){
                        markerHandlerIns
                          .init()
                          .then(
                            function(){
                              console.info('ALL DONE');
                            }
                          );
                      }
                    );
                }
              );
          }
        );
    },
    function(){
      // ToDo
    }
  );
});
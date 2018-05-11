(function(){
  // -----------------------------------
  // Marker Handler Class
  // -----------------------------------
  class MarkerHandler{
    constructor(){
      this.markerDOM = null;
      this.overlayDOM = [];
    }
    update(elm, status){
      var dfd = new $.Deferred();
      setTimeout(
        function(){
          elm.addClass('___visible');
          dfd.resolve();
        },
        200 * status
      );
      return dfd.promise();
    };
    reset(){
      this.markerDOM = $('.marker');
      var tmpOverlayDOM = null;
      var _this = this;
      this.markerDOM.each(
        function(idx, marker){
          tmpOverlayDOM = $('<span class="overlay"></span>');
          _this.overlayDOM.push(tmpOverlayDOM);
          $(marker).append(tmpOverlayDOM);
        }
      );
    };
    init(){
      var dfd = new $.Deferred();
      var defs = [];
      for(var i = 1, il = this.overlayDOM.length; i <= il; i++){
        defs.push(this.update($(this.overlayDOM[i - 1]), i));
      }
      $.when.apply($, defs).done(
        function(){
          dfd.resolve();
        }
      );
      return dfd.promise();
    }
  };
  // -----------------------------------
  // Loading Handler Class
  // -----------------------------------
  class LoadingHandler{
    constructor(loadingDOM, loadingStatusDOM){
      this.loadingDOM = loadingDOM;
      this.loadingStatusDOM = loadingStatusDOM;
      this.currentLoadingStatus = 0;
    };
    update(status){
      var dfd = new $.Deferred();
      var buffer = status * 30;
      var visibleStatus = status + '%';
      var _this = this;
      setTimeout(
        function(){
          _this.loadingStatusDOM.text(visibleStatus).attr('data-text', visibleStatus);
          dfd.resolve();
        },
        buffer
      );
      return dfd.promise();
    };
    init(status){
      var dfd = new $.Deferred();
      var defs = [];
      var _this = this;
      if(this.currentLoadingStatus !== 0){
        for(var i = this.currentLoadingStatus; i <= status; i++){
          defs.push(this.update(i));
        }
      }else{
        for(var i = 1; i <= status; i++){
          defs.push(this.update(i));
        }
      }
      $.when.apply($, defs).done(
        function(){
          _this.currentLoadingStatus = status;
          if(_this.currentLoadingStatus === 100){
            setTimeout(
              function(){
                _this.loadingDOM.addClass('___loaded');
                dfd.resolve();
              },
              800
            );
          }else{
            dfd.resolve();
          }
        }
      );
      return dfd.promise();
    };
  };
  // Export
  window.LoadingHandler = LoadingHandler;
  window.MarkerHandler = MarkerHandler;
})();
export default class MarkerHandler{
  linkMarker : string;
  overlayDOM : Array<HTMLElement>;
  constructor(linkMarker:string){
    this.linkMarker = linkMarker;
    this.overlayDOM = [];
  };
  update(markerDOM:HTMLElement, status:number){
    return new Promise(
      (resolve:any, reject:any) => {
        setTimeout(
          function(){
            markerDOM.classList.add('___visible');
            resolve();
          },
          200 * status
        );
      }
    );
  };
  reset(){
    let markerDOM = document.querySelectorAll('.' + this.linkMarker);
    for(let i = 0, il = markerDOM.length; i < il; i++){
      let tmpOverlayDOM = document.createElement('span');
      tmpOverlayDOM.classList.add('overlay');
      this.overlayDOM.push(tmpOverlayDOM);
      markerDOM[i].appendChild(tmpOverlayDOM);
    }
  };
  init(){
    let defs: Array<any> = [];
    for(let i = 1, il = this.overlayDOM.length; i <= il; i++){
      defs.push(this.update(this.overlayDOM[i - 1], i));
    }
    return new Promise(
      (resolve:any, reject:any) => {
        Promise.all(defs)
          .then(
            () => {
              resolve();
            }
          )
      }
    );
  }
}
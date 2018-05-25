export default class MarkerHandler{
  overlayMarker : string;
  overlayDOM : Array<HTMLElement>;
  constructor(overlayMarker:string){
    this.overlayMarker = overlayMarker;
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
    this.overlayDOM = [].slice.call(document.querySelectorAll('.' + this.overlayMarker));
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
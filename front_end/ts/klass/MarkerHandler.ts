/**
 * @classdesc   MarkerHandler
 * @author      rustywoman
 * @description Handle Custom Marker Layer
 */
export default class MarkerHandler{
  overlayMarker : string;
  overlayDOM    : Array<HTMLElement>;
  /**
   * @constructor MarkerHandler
   * @param    {string} overlayMarker - Overlayed Marker
   * @property {string} overlayMarker - Overlayed Marker
   * @property {object} overlayDOM    - Array of raw DOM
   */
  constructor(overlayMarker:string){
    this.overlayMarker = overlayMarker;
    this.overlayDOM = [];
  }
  /**
   * Update
   * @description Update Marker raw DOM with Promise
   * @param  {object} markerDOM - Target raw DOM
   * @param  {number} status    - Target raw DOM Index
   * @return {object} Promise
   */
  update(markerDOM:HTMLElement, status:number):any{
    return new Promise(
      (resolve:any, reject:any) => {
        setTimeout(
          () => {
            markerDOM.classList.add('___visible');
            resolve();
          },
          200 * status
        );
      }
    );
  }
  /**
   * Reset
   * @description Reset Array of Target raw DOM
   * @return {void}
   */
  reset():void{
    this.overlayDOM = [].slice.call(document.querySelectorAll('.' + this.overlayMarker));
  }
  /**
   * Init
   * @description Initialize Marker with Promise
   * @return {object} Promise
   */
  init():any{
    let defs:Array<any> = [];
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
          );
      }
    );
  }
}

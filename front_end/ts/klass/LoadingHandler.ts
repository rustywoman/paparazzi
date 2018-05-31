/**
 * @classdesc   LoadingHandler
 * @author      rustywoman
 * @description Handle Custom Loading Layer
 */
export default class LoadingHandler{
  loadingDOM           : HTMLElement;
  loadingStatusDOM     : HTMLElement;
  loadedMarker         : string;
  currentLoadingStatus : number;
  /**
   * @constructor LoadingHandler
   * @param    {object} loadingDOM           - Loading Root raw DOM
   * @param    {object} loadingStatusDOM     - Loading Status raw DOM
   * @param    {string} loadedMarker         - Loaded Marker
   * @property {object} loadingDOM           - Loading Root raw DOM
   * @property {object} loadingStatusDOM     - Loading Status raw DOM
   * @property {string} loadedMarker         - Loaded Marker
   * @property {number} currentLoadingStatus - Loading Real-time Status
   */
  constructor(loadingDOM:HTMLElement, loadingStatusDOM:HTMLElement, loadedMarker='___loaded'){
    this.loadingDOM = loadingDOM;
    this.loadingStatusDOM = loadingStatusDOM;
    this.loadedMarker = loadedMarker;
    this.currentLoadingStatus = 0;
  };
  /**
   * Update
   * @description Update Loading Status with Promise
   * @param  {number} status - Loading Current Status
   * @return {any} Promise
   */
  update(status:number):any{
    let buffer = status * 10;
    let visibleStatus = status + '%';
    return new Promise(
      (resolve:any, reject:any) => {
        setTimeout(
          () => {
            this.loadingStatusDOM.innerHTML = visibleStatus;
            this.loadingStatusDOM.setAttribute('data-text', visibleStatus);
            resolve();
          },
          buffer
        );
      }
    );
  };
  /**
   * Reset
   * @description Reset Loading Status
   * @return {void}
   */
  reset():void{
    this.currentLoadingStatus = 0;
    let visibleStatus = this.currentLoadingStatus + '%';
    this.loadingStatusDOM.innerHTML = visibleStatus;
    this.loadingStatusDOM.setAttribute('data-text', visibleStatus);
    this.loadingDOM.classList.remove(this.loadedMarker);
  };
  /**
   * Init
   * @description Initialize Loading with Promise
   * @param  {number} status - Loading Current Status
   * @return {any} Promise
   */
  init(status:number):any{
    let defs: Array<any> = [];
    if(this.currentLoadingStatus !== 0){
      for(let i = this.currentLoadingStatus; i <= status; i++){
        defs.push(this.update(i));
      }
    }else{
      for(let i = 1; i <= status; i++){
        defs.push(this.update(i));
      }
    }
    return new Promise(
      (resolve:any, reject:any) => {
        Promise.all(defs)
          .then(
            () => {
              this.currentLoadingStatus = status;
              if(this.currentLoadingStatus === 100){
                setTimeout(
                  () => {
                    this.loadingDOM.classList.add(this.loadedMarker);
                    resolve();
                  },
                  1000
                );
              }else{
                resolve();
              }
            }
          )
      }
    );
  };
};
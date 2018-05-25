export default class LoadingHandler{
  loadingDOM : HTMLElement;
  loadingStatusDOM : HTMLElement;
  loadedMarker : string;
  currentLoadingStatus : number;
  constructor(loadingDOM:HTMLElement, loadingStatusDOM:HTMLElement, loadedMarker='___loaded'){
    this.loadingDOM = loadingDOM;
    this.loadingStatusDOM = loadingStatusDOM;
    this.loadedMarker = loadedMarker;
    this.currentLoadingStatus = 0;
  };
  update(status:number){
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
  reset(){
    this.currentLoadingStatus = 0;
    let visibleStatus = this.currentLoadingStatus + '%';
    this.loadingStatusDOM.innerHTML = visibleStatus;
    this.loadingStatusDOM.setAttribute('data-text', visibleStatus);
    this.loadingDOM.classList.remove(this.loadedMarker);
  };
  init(status:number){
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
}
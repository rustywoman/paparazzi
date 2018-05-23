// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Original Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import CONSTANT from 'conf/CONSTANT';
import STATUS from 'conf/STATUS';
import LoadingHandler from 'klass/LoadingHandler';
import MarkerHandler from 'klass/MarkerHandler';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Init
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
document.addEventListener(
  'DOMContentLoaded',
  () => {
    let customLoadingIns = new LoadingHandler(
      document.querySelector('#loading__bg'),
      document.querySelector('#loading__status'),
      CONSTANT.LOADED_MARKER
    );
    let markerHandlerIns = new MarkerHandler('marker');
    customLoadingIns
      .init(80)
      .then(
        () => {
          markerHandlerIns.reset();
          customLoadingIns
            .init(100)
            .then(
              () => {
                markerHandlerIns
                  .init()
                  .then(
                    () => {
                      console.warn('>>> Done <<<');
                    }
                  );
              }
            );
        }
      );
  },
  false
);
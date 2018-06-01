// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Definition
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/**
 * @author      rustywoman
 * @description Constant - [ delay, marker, base64ed image ]
 * @type        {enum}
   @property    {number} DOM_DEFAULT_BUFFER     - Default Buffer for DOM
   @property    {number} DEFAULT_DELAY          - Default Delay for `setTimeout`
   @property    {number} ERROR_DELAY            - Error Delay for `setTimeout`
   @property    {string} HIDDEN_MARKER          - Hidden Marker for DOM and SCSS
   @property    {string} ERROR_MARKER           - Error Marker for DOM and SCSS
   @property    {string} LOADED_MARKER          - Loaded Marker for DOM and SCSS
   @property    {string} COMMON_MARKER          - Common Marker for DOM and SCSS
   @property    {string} DUMMY_IMAGE_BASE64_SRC - Custom 404 Image
 */
enum CONSTANT {
  DOM_DEFAULT_BUFFER     = 40,
  DEFAULT_DELAY          = 800,
  ERROR_DELAY            = 5000,
  HIDDEN_MARKER          = '___hidden',
  ERROR_MARKER           = '___error',
  LOADED_MARKER          = '___loaded',
  COMMON_MARKER          = '___marker',
  DUMMY_IMAGE_BASE64_SRC = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACAAQMAAAD58POIAAAABlBMVEUAAAAAFx8t7DCsAAAAAXRSTlMAQObYZgAAACdJREFUSMdj+A8EDEjkqMCoADI5ClDAoImXUYHBKTAKRvPLqADRAgAGUnu9KI2EPgAAAABJRU5ErkJggg=='
};


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Export
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
export default CONSTANT;
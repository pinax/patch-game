const BASE_URL = 'http://pinaxproject.com/pinax-design/patches/';
const WIDTH = 170;
const HEIGHT = 186;
const MARGIN = 20;
const PADDING = 20;

const position = (row, index) => {
  // assume row and index are 0 based indicies telling us the current row and
  // item in the row, in the tessellation.
  let x;
  let y;
  const evenRow = (row + 1) % 2 === 0;

  x = (index * (WIDTH + MARGIN)) + PADDING;
  y = row * (HEIGHT - PADDING);

  if (evenRow) {
    // even rows will have one more on each row so we shift left a bit the first one
    x -= (WIDTH + MARGIN) / 2;
  }
  return { x, y };
};

const loadTessellations = () => {
  const $tess = $('#tessellations');
  if ($tess.data('apps') === undefined) {
    return;
  }
  const apps = $tess.data('apps').split(' ');
  const itemsPerRow = parseInt($tess.data('perRow'));
  const coupletLength = (itemsPerRow * 2) + 1;
  const coupletCount = Math.floor(apps.length / coupletLength);
  let coupletExtra = apps.length % coupletLength;
  const couplet = [...Array((itemsPerRow * 2) + 1).keys()];

  // Build rows of indexes
  const rows = [];
  for (let i = 0; i < coupletCount; i++) {
    rows.push(couplet.slice(0, itemsPerRow));
    rows.push(couplet.slice(itemsPerRow));
  }
  if (coupletExtra > itemsPerRow) {
    rows.push(couplet.slice(0, itemsPerRow));
    rows.push(couplet.slice(itemsPerRow, coupletExtra));
  } else {
    rows.push(couplet.slice(0, coupletExtra));
  }
  for (let i = 0; i < rows.length; i++) {
    const indexMultiple = Math.floor(i / 2) * coupletLength;
    for (let j = 0; j < rows[i].length; j++) {
      rows[i][j] += indexMultiple;
    }
  }

  for (let i = 0; i < rows.length; i++) {
    for (let j = 0; j < rows[i].length; j++) {
      const app = apps[rows[i][j]].trim();
      if (app === '') continue;
      const pos = position(i, j);
      const srcUrl = `${BASE_URL}${app}.svg`;
      const $img = $('<img>');
      $img.css({
        left: `${pos.x}px`,
        top: `${pos.y}px`
      });
      $img.attr('src', srcUrl);
      $tess.append($img);
    }
  }

  $tess.css({
    width: `${(PADDING * 2) + ((WIDTH + MARGIN) * itemsPerRow) - MARGIN}px`,
    height: `${(PADDING * 2) + ((HEIGHT) * rows.length) - ((HEIGHT / 8) * (rows.length - 1)) - 3}px`  // don't get the -3px
  });
};

export default loadTessellations;

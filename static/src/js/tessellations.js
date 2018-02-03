const BASE_URL = 'http://pinaxproject.com/pinax-design/patches/';
const WIDTH = 170;
const HEIGHT = 186;
const MARGIN = 20;
const PADDING = 20;

const calcPosition = (index, perRow, currentRow, currentY) => {
  let row = currentRow;
  let my = currentY;
  let mx = (index % perRow) * (WIDTH + MARGIN) + PADDING;

  if (index > 0 && index % perRow === 0) {
    row += 1;
    my += (HEIGHT + MARGIN) - (HEIGHT / 4);
  }
  if (row % 2 === 0) {
    mx += (WIDTH + MARGIN) / 2;
  }
  return { mx, my, row };
};

const loadTessellations = () => {
  const $tess = $('#tessellations');
  if ($tess.data('apps') === undefined) {
    console.warn('There are no data-apps defined in #tessellations');
    return;
  }
  const apps = $tess.data('apps').split(' ');
  const itemsPerRow = parseInt($tess.data('perRow'));
  let row = 1;
  let y = 0 + PADDING;

  for (let i = 0; i < apps.length; i++) {
    const app = apps[i].trim()
    if (app === '') continue;
    const position = calcPosition(i, itemsPerRow, row, y);
    y = position.my;
    row = position.row;
    const srcUrl = `${BASE_URL}${app}.svg`;
    const $img = $('<img>');
    $img.css({
      left: `${position.mx}px`,
      top: `${position.my}px`
    });
    $img.attr('src', srcUrl);
    $tess.append($img);
  }
  $tess.css({
    width: `${(PADDING * 2) + ((WIDTH + MARGIN) * itemsPerRow) - MARGIN}px`,
    height: `${(PADDING * 2) + ((HEIGHT) * row) - ((HEIGHT / 8) * (row - 1)) - 3}px`  // don't get the -3px
  });
};

export default loadTessellations;

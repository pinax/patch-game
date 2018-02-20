const BASE_URL = 'http://pinaxproject.com/pinax-design/patches/';
const WIDTH = 170;
const HEIGHT = 186;
const MARGIN = 20;
const PADDING = 20;

const position = (row, index, w=WIDTH, h=HEIGHT, m=MARGIN, p=PADDING) => {
  // assume row and index are 0 based indicies telling us the current row and
  // item in the row, in the tessellation.
  let x;
  let y;
  const evenRow = (row + 1) % 2 === 0;

  x = (index * (w + m)) + p;
  y = row * (h - p);

  if (evenRow) {
    // even rows will have one more on each row so we shift left a bit the first one
    x -= (w + m) / 2;
  }
  return { x, y };
};

const buildTessellation = (patchesCount, perRow) => {
  const coupletLength = (perRow * 2) + 1;
  const coupletCount = Math.floor(patchesCount / coupletLength);
  let coupletExtra = patchesCount % coupletLength;
  const couplet = [...Array((perRow * 2) + 1).keys()];

  const rows = [];
  for (let i = 0; i < coupletCount; i++) {
    rows.push(couplet.slice(0, perRow));
    rows.push(couplet.slice(perRow));
  }
  if (coupletExtra > perRow) {
    rows.push(couplet.slice(0, perRow));
    rows.push(couplet.slice(perRow, coupletExtra));
  } else {
    rows.push(couplet.slice(0, coupletExtra));
  }
  for (let i = 0; i < rows.length; i++) {
    const indexMultiple = Math.floor(i / 2) * coupletLength;
    for (let j = 0; j < rows[i].length; j++) {
      rows[i][j] += indexMultiple;
    }
  }
  return rows;
};

const loadTessellations = () => {
  const $tess = $('#tessellations');
  if ($tess.data('apps') === undefined) {
    return;
  }
  const apps = $tess.data('apps').split(' ');
  const itemsPerRow = parseInt($tess.data('perRow'));
  const rows = buildTessellation(apps.length, itemsPerRow);

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

export const arrangeCorrectAnswers = () => {
  const PAD = 4;
  const MAR = 4;
  const W = 30;
  const H = 32.8125;
  const $tess = $('.user-stats .correct-answers .patches');
  const $images = $tess.find('img');
  const itemsPerRow = parseInt($tess.data('perRow'));
  const rows = buildTessellation($images.length, itemsPerRow);

  for(let i = 0; i < rows.length; i++) {
    for (let j = 0; j < rows[i].length; j++) {
      const $img = $($images[rows[i][j]]);
      const pos = position(i, j, W, H, MAR, PAD);
      $img.css({
        left: `${pos.x}px`,
        top: `${pos.y}px`
      });
    }
  }
  $tess.css({
    width: `${(PAD * 2) + ((W + MAR) * itemsPerRow) - MAR}px`,
    height: `${(PAD * 2) + ((H) * rows.length) - ((H / 8) * (rows.length - 1)) - 3}px`  // don't get the -3px
  });
}

export default loadTessellations;

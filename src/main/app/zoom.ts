import type { BrowserWindow } from "electron";

const MAX_ZOOM_FACTOR = 1.25;
const MIN_PAGE_WIDTH = 900;

let autoZoomFactor: number | undefined;

export function fitZoomFactor(contentWidth: number): number {
  const factor = contentWidth / MIN_PAGE_WIDTH;
  if (factor <= 1) return 1;
  if (factor >= MAX_ZOOM_FACTOR) return MAX_ZOOM_FACTOR;
  return factor;
}

export function fitZoomToWindow(win: BrowserWindow): void {
  const current = win.webContents.getZoomFactor();
  const zoomedByHand =
    autoZoomFactor !== undefined && Math.abs(current - autoZoomFactor) > 0.01;
  if (zoomedByHand) return;

  const { width } = win.getContentBounds();
  autoZoomFactor = fitZoomFactor(width);
  win.webContents.setZoomFactor(autoZoomFactor);
}

export function resetZoomToFit(win: BrowserWindow): void {
  autoZoomFactor = undefined;
  fitZoomToWindow(win);
}

class Solution {
    public boolean checkOverlap(int radius, int xc, int yc,int x1, int y1, int x2, int y2) {
        int closestX = Math.max(x1, Math.min(xc, x2));
        int closestY = Math.max(y1, Math.min(yc, y2));
        int dx = xc - closestX;
        int dy = yc - closestY;
        return dx * dx + dy * dy <= radius * radius;
    }
}
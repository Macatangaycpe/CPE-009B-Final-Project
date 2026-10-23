"""Halloween background art and logo helper (save as frontend/components/halloween_art.py)."""
 
import math
import random
from pathlib import Path
 
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QBrush, QColor, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap,
    QPolygonF, QRadialGradient,
)
from PyQt6.QtWidgets import QLabel
 
# Put your logo at <project root>/assets/digicash_logo.png
ASSETS = Path(__file__).resolve().parents[2] / "assets"
 
 
def _bat(painter, cx, cy, s):
    """Draw one bat silhouette centered at (cx, cy) with wingspan about 2*s."""
    wings = QPainterPath()
    wings.moveTo(cx, cy - s * 0.25)
    wings.cubicTo(cx + s * 0.2, cy - s * 0.6, cx + s * 0.7, cy - s * 0.5, cx + s, cy - s * 0.2)
    wings.quadTo(cx + s * 0.8, cy - s * 0.1, cx + s * 0.7, cy + s * 0.15)
    wings.quadTo(cx + s * 0.5, cy, cx + s * 0.4, cy + s * 0.2)
    wings.quadTo(cx + s * 0.25, cy + s * 0.05, cx, cy + s * 0.35)
    wings.quadTo(cx - s * 0.25, cy + s * 0.05, cx - s * 0.4, cy + s * 0.2)
    wings.quadTo(cx - s * 0.5, cy, cx - s * 0.7, cy + s * 0.15)
    wings.quadTo(cx - s * 0.8, cy - s * 0.1, cx - s, cy - s * 0.2)
    wings.cubicTo(cx - s * 0.7, cy - s * 0.5, cx - s * 0.2, cy - s * 0.6, cx, cy - s * 0.25)
    painter.drawPath(wings)
    for side in (-1, 1):  # ears
        painter.drawPolygon(QPolygonF([
            QPointF(cx + side * s * 0.05, cy - s * 0.2),
            QPointF(cx + side * s * 0.12, cy - s * 0.42),
            QPointF(cx + side * s * 0.22, cy - s * 0.2),
        ]))
 
 
def _cobweb(painter, x, y, radius, flip_x=False):
    """Draw a faint cobweb fanning out from the corner at (x, y)."""
    sx = -1 if flip_x else 1
    spokes = 5
    angles = [i * (math.pi / 2) / (spokes - 1) for i in range(spokes)]
    painter.setPen(QPen(QColor(243, 230, 208, 50), 1))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    for a in angles:
        painter.drawLine(
            QPointF(x, y),
            QPointF(x + sx * radius * math.cos(a), y + radius * math.sin(a)),
        )
    for ring in (0.3, 0.55, 0.8, 1.0):
        r = radius * ring
        pts = [QPointF(x + sx * r * math.cos(a), y + r * math.sin(a)) for a in angles]
        for p1, p2 in zip(pts, pts[1:]):
            mid = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
            ctrl = QPointF(x + (mid.x() - x) * 0.88, y + (mid.y() - y) * 0.88)
            path = QPainterPath(p1)
            path.quadTo(ctrl, p2)
            painter.drawPath(path)
 
 
def paint_background(painter, rect):
    """Paint a night sky with stars, a pumpkin-orange moon, bats, and cobwebs."""
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    w, h = rect.width(), rect.height()
 
    sky = QLinearGradient(0, 0, 0, h)
    sky.setColorAt(0.0, QColor("#2a1245"))
    sky.setColorAt(0.55, QColor("#17101f"))
    sky.setColorAt(1.0, QColor("#0d0912"))
    painter.fillRect(rect, sky)
 
    # Stars (seeded so they do not shimmer on every repaint)
    rng = random.Random(7)
    painter.setPen(Qt.PenStyle.NoPen)
    for _ in range(35):
        r = rng.uniform(0.6, 1.6)
        painter.setBrush(QColor(243, 230, 208, rng.randint(50, 140)))
        painter.drawEllipse(QPointF(rng.uniform(0, w), rng.uniform(0, h * 0.5)), r, r)
 
    # Moon with glow
    moon, mr = QPointF(w * 0.84, h * 0.15), 30
    glow = QRadialGradient(moon, mr * 3)
    glow.setColorAt(0.0, QColor(255, 154, 77, 90))
    glow.setColorAt(1.0, QColor(255, 154, 77, 0))
    painter.setBrush(QBrush(glow))
    painter.drawEllipse(moon, mr * 3, mr * 3)
    painter.setBrush(QColor("#ffb36b"))
    painter.drawEllipse(moon, mr, mr)
 
    # Bats, placed in the empty middle of the login screen
    painter.setBrush(QColor(8, 5, 12, 235))
    for fx, fy, size in ((0.18, 0.64, 18), (0.72, 0.70, 14), (0.45, 0.76, 11), (0.88, 0.62, 10)):
        _bat(painter, w * fx, h * fy, size)
 
    _cobweb(painter, 0, 0, 110)
    _cobweb(painter, w, 0, 110, flip_x=True)
 
 
def make_logo(filename="digicash_logo.png", width=200):
    """Return a centered logo label, or a text fallback if the image is missing."""
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap(str(ASSETS / filename))
    if pixmap.isNull():
        label.setText("DIGICASH")
        label.setObjectName("titleLabel")
    else:
        label.setPixmap(pixmap.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation))
    return label
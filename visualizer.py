
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

class NoteVisualizer:
    """
    Visualizes annotations preserving color and pressure sensitivity.
    """

    def __init__(self, annotations: List[Dict[str, Any]]):
        self.annotations = annotations

    def render(self) -> Dict[int, str]:
        """
        Creates color visualizations per page of annotations.

        Returns:
            Dict where key: page_number, value: path to saved image visualization
        """
        visualizations = {}

        # Group annotations by page
        pages = {}
        for ann in self.annotations:
            pages.setdefault(ann["page_number"], []).append(ann)

        for page_num, anns in pages.items():
            fig, ax = plt.subplots()
            fig.set_size_inches(8.27, 11.69)  # A4 size as typical ebook page approx

            ax.set_xlim(0, 612)  # typical PDF page width in points (8.5in * 72)
            ax.set_ylim(0, 792)  # typical PDF page height in points (11in * 72)
            ax.invert_yaxis()   # PDF origin is bottom-left; invert for top-left origin in matplotlib

            ax.axis("off")

            # Draw annotations
            for ann in anns:
                color = ann["color"]
                pressure = ann["pressure"] if isinstance(ann["pressure"], (float, int)) else 1.0
                bbox = ann["bbox"]
                ann_type = ann["annotation_type"]

                if ann_type == "Ink" and ann.get("points"):
                    pts = ann["points"]
                    if pts and len(pts) >= 2:
                        xs = [p[0] for p in pts]
                        ys = [p[1] for p in pts]
                        ax.plot(xs, ys, color=color, linewidth=pressure * 3, solid_capstyle='round')
                else:
                    # For other annotation types, draw bounding box with some transparency
                    rect = patches.Rectangle(
                        (bbox[0], bbox[1]),
                        bbox[2]-bbox[0],
                        bbox[3]-bbox[1],
                        linewidth=pressure * 1.5,
                        edgecolor=color,
                        facecolor=color,
                        alpha=0.3
                    )
                    ax.add_patch(rect)

            img_filename = f"page_{page_num}_visualization.png"
            img_path = os.path.join("temp_vis", img_filename)
            os.makedirs("temp_vis", exist_ok=True)
            plt.savefig(img_path, dpi=150, bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            visualizations[page_num] = img_path

        return visualizations

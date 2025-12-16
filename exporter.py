
from typing import List, Dict, Any
import os
import json
import shutil

class NoteExporter:
    """
    Exports structured notes and their visualizations.
    """

    def __init__(self, annotations: List[Dict[str, Any]], visual_notes: Dict[int, str], output_path: str):
        self.annotations = annotations
        self.visual_notes = visual_notes
        self.output_path = output_path

    def export(self):
        """
        Export notes as JSON and copy visualization images to output directory.
        """
        notes_per_page = {}
        for ann in self.annotations:
            page = ann["page_number"]
            notes_per_page.setdefault(page, []).append({
                "annotation_type": ann["annotation_type"],
                "color": ann["color"],
                "pressure": ann["pressure"],
                "content": ann["content"],
                "bbox": ann["bbox"],
                "points": ann.get("points"),
            })

        # Export JSON notes
        notes_json_path = os.path.join(self.output_path, "notes.json")
        with open(notes_json_path, 'w', encoding='utf-8') as f:
            json.dump(notes_per_page, f, indent=4, ensure_ascii=False)

        # Copy visualizations
        vis_dir = os.path.join(self.output_path, "visualizations")
        os.makedirs(vis_dir, exist_ok=True)

        for page_num, vis_path in self.visual_notes.items():
            base_name = os.path.basename(vis_path)
            dest_path = os.path.join(vis_dir, base_name)
            shutil.copyfile(vis_path, dest_path)

        # Clean temp visualization folder
        temp_vis_dir = os.path.dirname(next(iter(self.visual_notes.values()), ""))
        if temp_vis_dir and os.path.exists(temp_vis_dir):
            try:
                shutil.rmtree(temp_vis_dir)
            except Exception:
                pass

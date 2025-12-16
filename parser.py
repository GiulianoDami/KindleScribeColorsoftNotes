
import os
from typing import List, Dict, Any
import fitz  # PyMuPDF

class AnnotationParser:
    """
    Parses color and pressure sensitive handwritten annotations from Kindle Scribe Colorsoft ebooks.
    """

    def __init__(self, ebook_path: str):
        self.ebook_path = ebook_path

    def parse(self) -> List[Dict[str, Any]]:
        """
        Extract annotations from the ebook file.

        Returns:
            List of dicts representing annotations with keys:
            - page_number: int
            - annotation_type: str
            - color: str (hex)
            - pressure: float (0.0 to 1.0)
            - content: str or image data
            - bbox: tuple (x0, y0, x1, y1)
        """
        annotations = []
        if os.path.isdir(self.ebook_path):
            # Possibly a folder with one or more PDFs or annotation data files
            for root, _, files in os.walk(self.ebook_path):
                for file in files:
                    path = os.path.join(root, file)
                    if file.lower().endswith('.pdf'):
                        annotations.extend(self._parse_pdf(path))
        elif self.ebook_path.lower().endswith('.pdf'):
            annotations = self._parse_pdf(self.ebook_path)
        else:
            raise ValueError(f"Unsupported input file type or path: {self.ebook_path}")

        return annotations

    def _parse_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        doc = fitz.open(pdf_path)
        annotations = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            annot = page.firstAnnot
            while annot:
                subtype = annot.info.get("Subtype", "")
                if subtype in ("Ink", "Highlight", "Squiggly", "Underline", "StrikeOut", "FreeText", "Stamp"):
                    color = annot.colors.get("stroke") or annot.colors.get("fill")
                    if color:
                        # convert color float tuple (r,g,b) to hex string
                        color_hex = '#{:02x}{:02x}{:02x}'.format(
                            int(color[0]*255), int(color[1]*255), int(color[2]*255)
                        )
                    else:
                        color_hex = "#000000"

                    # Pressure is not standard in PDF annotations; we fake as 1.0 or read custom data if available
                    pressure = annot.info.get("Pressure", 1.0)

                    content = annot.info.get("Contents", "")
                    bbox = annot.rect

                    annotations.append({
                        "page_number": page_num + 1,
                        "annotation_type": subtype,
                        "color": color_hex,
                        "pressure": pressure,
                        "content": content,
                        "bbox": (bbox.x0, bbox.y0, bbox.x1, bbox.y1),
                        "points": self._extract_ink_points(annot) if subtype == "Ink" else None,
                    })
                annot = annot.next

        doc.close()
        return annotations

    def _extract_ink_points(self, annot) -> List[List[float]]:
        """
        Extract ink annotation points from Ink annotation if available.

        Points are usually stored as a list of points per stroke.
        This method returns a flattened list of (x,y) tuples (or list).

        Returns:
            List of points [[x1, y1], [x2, y2], ...]
        """
        ink_list = []
        try:
            ink_list = annot.vertices
        except Exception:
            # fallback empty
            ink_list = []
        return ink_list

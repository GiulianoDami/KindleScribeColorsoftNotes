
import argparse
import os
from parser import AnnotationParser
from visualizer import NoteVisualizer
from exporter import NoteExporter

def main():
    parser = argparse.ArgumentParser(description="Parse Kindle Scribe Colorsoft ebook annotations and export notes.")
    parser.add_argument('--input', required=True, help="Path to the annotated ebook file or folder.")
    parser.add_argument('--output', required=True, help="Path to directory where exported notes will be saved.")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(input_path):
        print(f"Error: Input path {input_path} does not exist.")
        return

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    print("Starting parsing annotations...")
    parser = AnnotationParser(input_path)
    annotations = parser.parse()

    print(f"Parsed {len(annotations)} annotations.")

    print("Visualizing notes...")
    visualizer = NoteVisualizer(annotations)
    visual_notes = visualizer.render()

    print("Exporting notes...")
    exporter = NoteExporter(annotations, visual_notes, output_path)
    exporter.export()

    print(f"Notes exported successfully to {output_path}.")

if __name__ == '__main__':
    main()

from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader
from src.visualize import DataVisualizer

def run_pipeline():
    print("="*50)
    print("E-COMMERCE ANALYTICS ETL PIPELINE")
    print("="*50)
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all()
    
    transformer = DataTransformer()
    clean_data = transformer.transform_all(raw_data)
    
    loader = DataLoader()
    loader.load_all(clean_data)
    
    visualizer = DataVisualizer()
    visualizer.run_all()
    
    print("\n" + "="*50)
    print("Pipeline completed successfully!")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()

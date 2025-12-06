import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.analysis.statistical_analysis import StatisticalAnalyzer
from src.analysis.ml_models import MachineLearningAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 80)
    logger.info("STARTING COMPLETE ANALYSIS PIPELINE")
    logger.info("=" * 80)
    
    try:
        logger.info("\n[PHASE 1/2] Statistical Analysis...")
        stat_analyzer = StatisticalAnalyzer()
        stat_results = stat_analyzer.run_complete_analysis()
        
        logger.info("\n[PHASE 2/2] Machine Learning Analysis...")
        ml_analyzer = MachineLearningAnalyzer()
        ml_results = ml_analyzer.run_complete_ml_analysis()
        
        logger.info("\n" + "=" * 80)
        logger.info("ANALYSIS COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        logger.info("\nStatistical Analysis Results:")
        for key in stat_results.keys():
            logger.info(f"  ✓ {key}")
            
        logger.info("\nMachine Learning Results:")
        for key in ml_results.keys():
            logger.info(f"  ✓ {key}")
            
    except Exception as e:
        logger.error(f"Analysis pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



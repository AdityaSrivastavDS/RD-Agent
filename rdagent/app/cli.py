"""
CLI entrance for all RD-Agent applications.

This will:
- Make rdagent a clean entry point
- Automatically load dotenv.
"""
import subprocess
from importlib.resources import path as rpath
import fire
import logging
from dotenv import load_dotenv, find_dotenv

from rdagent.app.data_mining.model import main as med_model
from rdagent.app.general_model.general_model import (
    extract_models_and_implement as general_model,
)
from rdagent.app.kaggle.loop import main as kaggle_main
from rdagent.app.qlib_rd_loop.factor import main as fin_factor
from rdagent.app.qlib_rd_loop.factor_from_report import main as fin_factor_report
from rdagent.app.qlib_rd_loop.model import main as fin_model
from rdagent.app.utils.info import collect_info

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file in the current directory or find it automatically
load_dotenv(find_dotenv())
logger.info("Environment variables loaded successfully.")

def start_ui(port=80, log_dir="", debug=False):
    """
    Start the web app to show the log traces.
    
    Args:
        port (int): The port to run the UI on.
        log_dir (str): Directory to store log files.
        debug (bool): Flag to run in debug mode.
    """
    try:
        with rpath("rdagent.log.ui", "app.py") as app_path:
            cmds = ["streamlit", "run", app_path, f"--server.port={port}"]
            if log_dir or debug:
                cmds.append("--")
            if log_dir:
                cmds.append(f"--log_dir={log_dir}")
            if debug:
                cmds.append("--debug")
            
            logger.info(f"Starting UI with command: {' '.join(cmds)}")
            subprocess.run(cmds)
    except Exception as e:
        logger.error(f"Error starting UI: {e}")

def run_app():
    """
    Fire-based CLI to execute various tasks.
    """
    try:
        fire.Fire(
            {
                "fin_factor": fin_factor,
                "fin_factor_report": fin_factor_report,
                "fin_model": fin_model,
                "med_model": med_model,
                "general_model": general_model,
                "ui": start_ui,
                "collect_info": collect_info,
                "kaggle": kaggle_main,
            }
        )
    except Exception as e:
        logger.error(f"Error running application: {e}")

if __name__ == "__main__":
    run_app()

import subprocess
import time

import wandb

from .common import parameters

MODES = [
    "selenium",
    "playwright",
    "selenium_single",
    # "selenium_multi",
    "selenium_dagster",
    "playwright_dagster",
]

counts = [1, 3, 5, 10, 15, 25, 50, 75, 100]

replicas = 5

if __name__ == "__main__":

    image_path = str(parameters.DATA_PATH / "richest.png")

    mode = "selenium"
    for count in counts:
        run = wandb.init(project="web_scraper", reinit=True)
        run.config["Method"] = mode
        run.config["ATTEMPS"] = parameters.MAX_ATTEMPS
        run.config["LATLONG_URL"] = parameters.LATLONG_URL
        run.config["PROFILE_COUNT"] = count

        start_time = time.perf_counter()

        completed = subprocess.run(f"python -m app {mode} {count}")
        success = "SUCCESS" if completed.returncode == 0 else "FAILURE"

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        try:
            map_ = wandb.Image(image_path)
        except FileNotFoundError:
            map_ = None

        log_metrics = {
            "execution_time": elapsed_time,
            "map": map_,
            "success": success,
        }

        wandb.log(log_metrics)

        run.finish()

    for count in counts:
        for mode in MODES:
            for _ in range(replicas):
                run = wandb.init(project="web_scraper", reinit=True)
                run.config["Method"] = mode
                run.config["ATTEMPS"] = parameters.MAX_ATTEMPS
                run.config["LATLONG_URL"] = parameters.LATLONG_URL
                run.config["PROFILE_COUNT"] = count

                start_time = time.perf_counter()

                completed = subprocess.run(f"python -m app {mode} {count}")
                success = "SUCCESS" if completed.returncode == 0 else "FAILURE"

                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                try:
                    map_ = wandb.Image(image_path)
                except FileNotFoundError:
                    map_ = None

                log_metrics = {
                    "execution_time": elapsed_time,
                    "map": map_,
                    "success": success,
                }

                wandb.log(log_metrics)

                run.finish()

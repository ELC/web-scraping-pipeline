import subprocess
import time

import neptune.new as neptune

from .common import parameters

MODES = [
    "selenium",
    "selenium_multi",
    "selenium_dagster",
    "playwright",
    "playwright_dagster",
]

counts = [1, 3, 5, 10, 15, 25, 50, 75, 100]

if __name__ == "__main__":

    mode = "selenium"
    for count in counts:
        api_token = parameters.NEPTUNE_KEY
        run = neptune.init(project="elc/web-scrapping", api_token=api_token)
        run["Method"] = mode
        run["LATLONG_URL"] = parameters.LATLONG_URL
        run["PROFILE_COUNT"] = count

        start_time = time.perf_counter()

        subprocess.run(f"python -m app {mode} {count}")

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        run["execution_time"].log(elapsed_time)
        run.stop()

    for count in counts:
        for mode in MODES:
            for _ in range(5):
                api_token = parameters.NEPTUNE_KEY
                run = neptune.init(project="elc/web-scrapping", api_token=api_token)
                run["Method"] = mode
                run["LATLONG_URL"] = parameters.LATLONG_URL
                run["PROFILE_COUNT"] = count

                start_time = time.perf_counter()

                subprocess.run(f"python -m app {mode} {count}")

                end_time = time.perf_counter()

                elapsed_time = end_time - start_time

                run["execution_time"].log(elapsed_time)
                run.stop()

import sys
import time
import asyncio

from .common import parameters

MODES = [
    "playwright",
    "selenium",
    "selenium_multi",
    "selenium_dagster",
    "playwright_dagster",
]

if __name__ == "__main__":
    mode = sys.argv[1]

    if len(sys.argv) >= 3:
        parameters.PROFILE_COUNT = int(sys.argv[2])

    if mode not in MODES:
        raise ValueError(f"Mode: {mode} should be in {MODES}")

    if mode == "playwright":
        from .imperative.playwright_runner import runner as playwright_run

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        asyncio.run(playwright_run())
        end_time = time.perf_counter()

    elif mode == "selenium":
        from .imperative.selenium_runner import runner as selenium_single

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        selenium_single()
        end_time = time.perf_counter()

    elif mode == "selenium_multi":
        from .imperative.selenium_multi_runner import runner as selenium_multi

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        selenium_multi()
        end_time = time.perf_counter()

    elif mode == "selenium_single":
        from .imperative.selenium_singleton_runner import runner as selenium_single

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        selenium_single()
        end_time = time.perf_counter()
        
        from .imperative.selenium_singleton_runner import close_driver
        close_driver()


    elif mode == "selenium_dagster":
        from .pipeline.selenium import selenium_pipeline
        from dagster import execute_pipeline, reconstructable, DagsterInstance

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        execute_pipeline(
            reconstructable(selenium_pipeline),
            run_config={"execution": {"multiprocess": {}}},
            instance=DagsterInstance.local_temp(),
        )
        end_time = time.perf_counter()

    elif mode == "playwright_dagster":
        from .pipeline.playwright import playwright_pipeline
        from dagster import execute_pipeline, reconstructable, DagsterInstance

        print(f"PROCESS STARTED: {mode}")
        start_time = time.perf_counter()
        execute_pipeline(
            reconstructable(playwright_pipeline),
            run_config={"execution": {"multiprocess": {}}},
            instance=DagsterInstance.local_temp(),
        )
        end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time:.2f}s")

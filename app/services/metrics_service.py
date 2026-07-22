import json
from pathlib import Path


FILE = Path("data/metrics.json")


class MetricsService:

    def __init__(self):

        FILE.parent.mkdir(exist_ok=True)

        if not FILE.exists():
            FILE.write_text(
                json.dumps({
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0
                })
            )


    def _read(self):

        return json.loads(
            FILE.read_text()
        )


    def _write(self, data):

        FILE.write_text(
            json.dumps(
                data,
                indent=4
            )
        )


    def success(self):

        data = self._read()

        data["total_requests"] += 1
        data["successful_requests"] += 1

        self._write(data)


    def failed(self):

        data = self._read()

        data["total_requests"] += 1
        data["failed_requests"] += 1

        self._write(data)


    def get(self):

        return self._read()



metrics_service = MetricsService()
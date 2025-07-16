from datetime import datetime, timezone
import time
from time import sleep

from halo import Halo

from cli.api_client import HonulabsAPIClient
from cli.schema import HonulabsJob, JobStatus
from cli.utils.token import HonulabsToken


LOADING_BAR = {
    "interval": 160,
    "frames": [
        "(       )",
        "(     🐢)",
        "(    🐢 )",
        "(   🐢  )",
        "(  🐢   )",
        "( 🐢    )",
        "(🐢     )",
        "(       )",
    ],
}


class JobManager:
    FINISHED_STATES = {JobStatus.SUCCESS, JobStatus.FAILED}

    def __init__(self, job: HonulabsJob):
        self.job = job
        self.started_at = self.job.started_at.replace(tzinfo=timezone.utc)

        self.spinner = None

    @property
    def client(self):
        token = HonulabsToken()
        return HonulabsAPIClient(token.token)

    @property
    def _message(self) -> str:
        if self.job.status == JobStatus.PENDING:
            return 'Initialising'
        elif self.job.status in self.FINISHED_STATES:
            return 'Finished'
        else:
            if self.job.message is None:
                return 'Running'
            return self.job.message

    @property
    def elapsed_time(self):
        elapsed_seconds = (datetime.now(timezone.utc) - self.started_at).seconds
        return time.strftime("%H:%M:%S", time.gmtime(elapsed_seconds))

    def await_job_completion(self, retry=True) -> HonulabsJob:
        # Loop requests to the API, give status message from the Job while it's still running
        self.spinner = Halo(text=self._message, spinner=LOADING_BAR)
        self.spinner.start()

        # Send an api request to fetch the job status
        while self.job.status not in self.FINISHED_STATES:
            try:
                self.job = self.client.get_job(self.job.business.business_id, self.job.job_id)
            except:
                break
            self.spinner.text = f"{self._message}\t{self.elapsed_time} elapsed."
            sleep(1)

        # Check the finished status
        self.spinner.stop()
        if self.job.status == JobStatus.SUCCESS:
            print('Job finished successfully')
        elif self.job.status == JobStatus.FAILED:
            if self.job.error is not None:
                print(f'Job failed with error message: {self.job.error}')
            else:
                print('Job was unsuccessful but had no error message')
        else:
            if retry:
                self.await_job_completion(False)
            else:
                if self.job.job_type == "delete_business":
                    print("Deleted!")
                else:
                    print('Job was unable to be read and failed')

        return self.job

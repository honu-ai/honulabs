from halo import Halo

from cli.api_client import HonulabsAPIClient
from cli.schema import HonulabsJob, JobStatus
from cli.utils.token import HonulabsToken


class JobManager:
    FINISHED_STATES = {JobStatus.SUCCESS, JobStatus.FAILED}

    def __init__(self, job: HonulabsJob):
        self.job = job
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

    def await_job_completion(self) -> HonulabsJob:
        # Loop requests to the API, give status message from the Job while it's still running
        self.spinner = Halo(text=self._message, spinner='dots')
        self.spinner.start()

        # Send an api request to fetch the job status
        while self.job.status not in self.FINISHED_STATES:
            try:
                self.job = self.client.get_job(self.job.business.business_id, self.job.job_id)
            except:
                break
            self.spinner.text = self._message

        # Check the finished status
        self.spinner.stop()
        if self.job.status == JobStatus.SUCCESS:
            print('Job finished successfully')
        else:
            if self.job.error is not None:
                print(f'Job failed with error message: {self.job.error}')
            else:
                print('Job was unsuccessful but had no error message')

        return self.job

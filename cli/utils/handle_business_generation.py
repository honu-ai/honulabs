import webbrowser
from tempfile import TemporaryDirectory

from pydantic import BaseModel

from cli.api_client import HonulabsAPIClient
from cli.schema import BusinessPlanRequirementsCreate, JobStatus, BusinessPlanRequirements, BusinessPlan, \
    BusinessNamesDomains
from cli.utils.job_manager import JobManager
from cli.utils.token import HonulabsToken


class BusinessPlanGeneration:
    REQUIREMENTS_JOB_TYPE = 'business_plan_requirements'

    def __init__(self, business_id: str, table_style: str):
        self.token = HonulabsToken()
        self.api_client = HonulabsAPIClient(self.token.token)
        self.business_id = business_id
        self.table_style = table_style

    def run(self):
        """
        Step 1: Requirements Generation
            - If there are no successful jobs already, do the generation from the start
            - Otherwise, allow the User to choose existing results
            - Render the outputs in markdown files and present to the user for validation
        """
        requirements = self._get_business_plan_requirements()
        if requirements is None:
            return
        print()
        base_business_plan = self._get_base_business_plan(requirements)
        if base_business_plan is None:
            return
        print()
        business_name = self._get_business_name(requirements)
        if business_name is None:
            return
        print()
        self._generate_full_business_plan(base_business_plan, business_name)

    def _verify_result(self, result: BaseModel) -> bool:
        with TemporaryDirectory(ignore_cleanup_errors=True) as dir_path:
            for name in result.model_fields:
                file_name = f'{dir_path}/{name}.md'
                value = getattr(result, name)
                lines = [f'# {name}']
                if isinstance(value, BaseModel):
                    # Iterate through fields and write them all out to the file
                    for sub_name in value.model_fields:
                        lines.append(f'## {sub_name}')
                        lines.append(getattr(value, sub_name))
                    lines.append('')
                else:
                    lines.append(getattr(result, name))

                with open(file_name, 'w') as f:
                    f.write('\n'.join(lines))

            print('Please take a look at the generated content to make sure you are happy with what was generated.')
            print(f'Generated files can be found in {dir_path}, and will open in a file browser as well.')
            webbrowser.open(f'file://{dir_path}')
            print()
            return input('Are you happy with the result? [y/n] ').lower().strip().startswith('y')

    def _get_business_plan_requirements(self) -> BusinessPlanRequirements | None:
        print('Step 1: Business Plan Requirements')

        # Check for in progress jobs of the matching type (TODO - later)
        # in_progress_jobs = self.api_client.get_jobs(
        #     self.business_id,
        #     self.REQUIREMENTS_JOB_TYPE,
        #     JobStatus.IN_PROGRESS,
        # )
        # if in_progress_jobs:
        #     print('Found the following jobs that are in progress. Please select one to wait for.')
        #     job = self._select_job(in_progress_jobs)
        #     if job is None:

        print('Please answer the following prompts.')
        print()

        requirements_data = {}
        for name, field in BusinessPlanRequirementsCreate.model_fields.items():
            response = input(f'{field.description} ')
            requirements_data[name] = response.strip()
            print()

        payload = BusinessPlanRequirementsCreate(**requirements_data)
        yes_no = input('Is this okay? [y/n] ').strip().lower()
        if yes_no[0] != 'y':
            print('Please re-run the command to start again')
            return

        job = self.api_client.generate_business_requirements(self.business_id, payload)
        print('Requirements Generation started successfully. Awaiting completion.')
        print('Please ensure you wait for this Job to finish as there is currently no way to continue an existing job.')
        print()
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print()
            print('Are you sure you want to skip the job? You currently cannot continue from an existing job. Press Ctrl+C again to confirm cancelling.')
            try:
                job = manager.await_job_completion()
            except (KeyboardInterrupt, EOFError):
                print('Exiting')
                return

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        requirements = BusinessPlanRequirements(**job.result)
        if self._verify_result(requirements):
            return requirements
        return None

    def _get_base_business_plan(self, requirements: BusinessPlanRequirements) -> BusinessPlan | None:
        print('Step 2: Base Business Plan Generation')
        print('We will now begin generating a basic business plan for you, please wait')

        job = self.api_client.generate_base_business_plan(self.business_id, requirements)
        print('Base Business Plan generation started successfully. Awaiting completion.')
        print('Please ensure you wait for this Job to finish as there is currently no way to continue an existing job.')
        print()
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print()
            print(
                'Are you sure you want to skip the job? You currently cannot continue from an existing job. Press Ctrl+C again to confirm cancelling.')
            try:
                job = manager.await_job_completion()
            except (KeyboardInterrupt, EOFError):
                print('Exiting')
                return

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        plan = BusinessPlan(**job.result)
        if self._verify_result(plan):
            return plan
        return None

    def _get_business_name(self, requirements: BusinessPlanRequirements, ideas: list[str] | None = None) -> str | None:
        if ideas is not None:
            print('Name Ideas:')
            for idea in ideas:
                print(f'- {idea}')
            print()
        else:
            print('Step 3: Naming your Business')

        name = input(
            'Please input an official name for your business. '
            'Alternatively, just press ENTER if you want us to generate some new ideas.',
        )
        name = name.strip()
        if name:
            return name

        # Generate some ideas and prompt again
        job = self.api_client.generate_business_name_ideas(self.business_id, requirements)
        print('Fetching name ideas.')
        print()
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print()
            print(
                'Are you sure you want to skip the job? You currently cannot continue from an existing job. Press Ctrl+C again to confirm cancelling.')
            try:
                job = manager.await_job_completion()
            except (KeyboardInterrupt, EOFError):
                print('Exiting')
                return

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        result = BusinessNamesDomains(**job.result)
        print()
        return self._get_business_name(requirements, [idea.business_name for idea in result.business_names_with_domains])

    def _generate_full_business_plan(self, business_plan: BusinessPlan, business_name: str):
        print('Full Business Plan Generation')
        print('Once this step is done, you will be able to deploy your landing page!')

        job = self.api_client.generate_full_business_plan(self.business_id, business_plan, business_name)
        print('Generation started successfully. Awaiting completion.')
        print('You can safely use Ctrl+C to stop waiting for the job, but you will not be able to deploy until it is finished.')
        print()
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print()
            print('Waiting cancelled. Use the `pending_jobs` command to check what jobs are still running.')

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        print('Now you can run `deploy_page` command to deploy your landing page.')

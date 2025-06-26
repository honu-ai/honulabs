from cli.api_client import HonulabsAPIClient
from cli.schema import BusinessPlanRequirementsCreate
from cli.utils.job_manager import JobManager
from cli.utils.token import HonulabsToken


def handle_business_generation(business_id: str):
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)

    print('Step 1, Requirements Generation.')

    # TODO - Check for jobs of the types to allow the user to skip steps they've already done
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

    job = api_client.generate_business_requirements(business_id, payload)
    print('Requirements Generation started successfully. Awaiting completion.')
    print('You can skip waiting with Ctrl+C but you will not be able to continue with this command until the job finishes.')
    print()
    manager = JobManager(job)
    try:
        manager.await_job_completion()
    except (KeyboardInterrupt, EOFError):
        manager.spinner.stop()
        print()
        print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}.')
        print('Returning to menu. When job is completed you may re-run this command and continue with its result if you wish.')
        return

    # TODO - Write out requirements markdown files and present them to the user for inspection

import os
import webbrowser
from tempfile import TemporaryDirectory

from pydantic import BaseModel
from tabulate import tabulate

from cli.api_client import HonulabsAPIClient
from cli.schema import BusinessPlanRequirementsCreate, JobStatus, BusinessPlanRequirements, BusinessPlan, \
    BusinessNamesDomains, HonulabsJob, MarketSegment
from cli.utils.job_manager import JobManager
from cli.utils.prompts import prompt_with_default
from cli.utils.token import HonulabsToken


class IdeaGeneration:
    REQUIREMENTS_JOB_TYPE = 'business_plan_requirements'

    def __init__(self, business_id: str, table_style: str):
        self.token = HonulabsToken()
        self.api_client = HonulabsAPIClient(self.token.token)
        self.business_id = business_id
        self.table_style = table_style

    def run(self):
        segment = self._market_segmentation()
        if not segment:
            return

        while True:
            new_idea = self._idea_generation(segment)
            if not new_idea:
                return
            elif new_idea == 'restart':
                # User pressed ENTER to generate new ideas - continue the loop
                continue
            else:
                # User selected a specific idea
                return new_idea

    def _idea_generation(self, segment: dict):
        # Set up the job
        job = self.api_client.idea_generation(
            self.business_id,
            segment['geography'],
            MarketSegment(**segment['segment'])
        )

        print('Deployment job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        categories = {str(i): j for i, j in enumerate(job.result['ideas'], start=1)}

        # Compute window size to wrap the table
        terminal_size_columns = int(os.get_terminal_size().columns - (os.get_terminal_size().columns*.1))
        print(
            tabulate(
                (
                    {
                        'Number': k,
                        'Challenge': v['challenge'],
                        'Saas title': v['saas_venture_title'],
                        'Saas description': v['saas_venture_description'],
                        'Feasibility': v['feasibility_rank']
                    }
                    for k, v in categories.items()
                ),
                headers='keys', tablefmt='double_grid', maxcolwidths=terminal_size_columns//5
            )
        )
        try:
            print('Please select one of the ideas, press ENTER to generate new ideas, or type "q" to cancel.')
            selected_num = input('> ').strip()
            if selected_num == '':
                # ENTER pressed - restart idea generation with same segment
                return 'restart'
            elif selected_num.lower() in ('q', 'quit', 'cancel'):
                # User wants to cancel and return to menu
                return

            while selected_num not in categories:
                print('That number is not a valid choice, please select a valid choice, press ENTER to generate new ideas, or type "q" to cancel.')
                selected_num = input('> ').strip()
                if selected_num == '':
                    # ENTER pressed - restart idea generation with same segment
                    return 'restart'
                elif selected_num.lower() in ('q', 'quit', 'cancel'):
                    # User wants to cancel and return to menu
                    return

            return categories[selected_num]
        except (KeyboardInterrupt, EOFError):
            return


    def _market_segmentation(self):
        # What segment
        try:
            print('What industry segment you like to focus on?: ')
            industry = input('> ').strip()
            if industry == '':
                return

            print('What geography would you like to focus on?: ')
            geography = input('> ').strip()
            if geography == '':
                return

            print(f"You are about to generate ideas for {industry.capitalize()} / {geography.capitalize()}")
            if not prompt_with_default("Do you want to continue?"):
                return

        except (KeyboardInterrupt, EOFError):
            return


        # Set up the job
        job = self.api_client.generate_market_segment(
            self.business_id,
            geography,
            industry,
        )
        print('Deployment job started successfully. Awaiting completion. Skip wait with Ctrl+C.')
        manager = JobManager(job)
        try:
            job = manager.await_job_completion()
        except (KeyboardInterrupt, EOFError):
            manager.spinner.stop()
            print(f'Skipping wait for job completion. Job will continue running in the background, with id {job.job_id}')

        # Put the data into files and let the user read them for verification
        if job.status == JobStatus.FAILED:
            return

        categories = {str(i): j for i, j in enumerate(job.result['ideas'], start=1)}

        # Compute window size to wrap the table
        terminal_size_columns = int(os.get_terminal_size().columns - (os.get_terminal_size().columns*.1))
        print(
            tabulate(
                (
                    {
                        'Number': k, 'Core market': v['core_market'], 'Sub-category': v['sub_category'], 'Niche': v['niche']
                    }
                    for k, v in categories.items()
                ),
                headers='keys', tablefmt='double_grid', maxcolwidths=terminal_size_columns//3
            )
        )
        try:
            print('Please select the market segment you want to use, or just press ENTER to start again.')
            selected_num = input('> ').strip()
            if selected_num == '':
                return

            while selected_num not in categories:
                print('That number is not a valid choice, please select a valid choice or press ENTER to cancel.')
                selected_num = input('> ').strip()
                if selected_num == '':
                    return

            return dict(segment=categories[selected_num], geography=geography)
        except (KeyboardInterrupt, EOFError):
            return




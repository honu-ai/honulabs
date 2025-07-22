from tabulate import tabulate

from cli.api_client import HonulabsAPIClient
from cli.schema import HonulabsBusinessPick
from cli.utils.token import HonulabsToken


def pick_business(table_style: str) -> HonulabsBusinessPick | None:
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    businesses = api_client.list_businesses()
    if not businesses:
        print('You have no projects yet! Please use `create_project` to create a new one!')
        return

    data = {
        str(num): {
            'id': biz.business_id,
            'name': biz.name,
            'model_ref': biz.model_ref
        }
        for num, biz in enumerate(businesses, start=1)
    }

    print(tabulate(
        ({'Number': num, 'Project Name': data[num]['name']} for num in sorted(data)),
        headers='keys',
        tablefmt=table_style,
    ))
    try:
        print('Please select the number of the project to interact with, or press ESC to cancel.')
        selected_num = input('> ').strip()
        if selected_num == '' or selected_num.lower() == 'esc' or selected_num == '\x1b':
            return

        while selected_num not in data:
            print('That number is not a valid choice, please select a valid choice or press ESC to cancel.')
            selected_num = input('> ').strip()
            if selected_num == '' or selected_num.lower() == 'esc' or selected_num == '\x1b':
                return

        return HonulabsBusinessPick(
            id=data[selected_num]['id'],
            model_ref=data[selected_num]['model_ref']
        )

    except (KeyboardInterrupt, EOFError):
        return

from tabulate import tabulate

from cli.api_client import HonulabsAPIClient
from cli.utils.token import HonulabsToken


def pick_business(table_style: str) -> str | None:
    token = HonulabsToken()
    api_client = HonulabsAPIClient(token.token)
    businesses = api_client.list_businesses()
    if not businesses:
        print('You have no businesses yet!')
        return

    data = {
        str(num): {
            'id': biz.business_id,
            'name': biz.name,
        }
        for num, biz in enumerate(businesses, start=1)
    }

    print(tabulate(
        ({'Number': num, 'Business Name': data[num]['name']} for num in sorted(data)),
        headers='keys',
        tablefmt=table_style,
    ))
    try:
        print('Please select the number of the business to interact with, or press ENTER to cancel.')
        selected_num = input('> ').strip()
        if selected_num == '':
            return

        while selected_num not in data:
            print('That number is not a valid choice, please select a valid choice or press ENTER to cancel.')
            selected_num = input('> ').strip()
            if selected_num == '':
                return

        return data[selected_num]['id']

    except (KeyboardInterrupt, EOFError):
        return

from backend.g4f import ChatCompletion, Model, Provider
from proxy import get_tor_session

session = get_tor_session()
request = input()
response = ChatCompletion.create(
    model=Model.gpt_35_turbo, messages=[{"role": "user", "content": request}], session=session,
)
print(response)

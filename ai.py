from backend.g4f import ChatCompletion, Model, Provider

request = input()
response = ChatCompletion.create(
    model=Model.gpt_35_turbo, messages=[{"role": "user", "content": request}]
)
print(response)
